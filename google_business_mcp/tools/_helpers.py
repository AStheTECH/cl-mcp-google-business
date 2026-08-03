"""Shared error helpers for all tool modules."""

import json

from googleapiclient.errors import HttpError

from ..logging_utils import ToolLogger
from ..schemas import ToolError


def _err(result_class, tlog, code, message, status, retriable=False, retry_after=None):
    tlog.failure(code, message)
    return result_class(
        success=False, statusCode=status, retriable=retriable,
        retry_after_seconds=retry_after,
        error=ToolError(code=code, message=message),
    )


def _handle_request_exc(result_class, tlog, exc):
    if isinstance(exc, HttpError):
        status = exc.resp.status if exc.resp is not None else 500
        data = _parse_http_error_content(exc)
        return _upstream_err(result_class, tlog, status, data)
    if isinstance(exc, ValueError):
        tlog.failure("AUTH_ERROR", str(exc))
        return result_class(success=False, statusCode=401, retriable=False,
            error=ToolError(code="AUTH_ERROR", message=str(exc)))
    tlog.failure("SERVER_ERROR", str(exc))  # log full detail internally
    return result_class(success=False, statusCode=500, retriable=False,
        error=ToolError(code="SERVER_ERROR", message="Unexpected server error"))


def _upstream_err(result_class, tlog, status, data, retry_after=None):
    retriable = status in (429, 500, 502, 503)
    tlog.failure("UPSTREAM_ERROR", f"HTTP {status}")
    msg = data.get("error") or data.get("message") or f"HTTP {status}"
    return result_class(
        success=False, statusCode=status, retriable=retriable,
        retry_after_seconds=retry_after,
        error=ToolError(code="UPSTREAM_ERROR", message=str(msg)),
    )


def _parse_http_error_content(exc: HttpError) -> dict:
    """Best-effort extraction of a plain {"error": "<message>"} dict from an
    HttpError's response body, so _upstream_err can treat it like a parsed
    JSON error payload regardless of the upstream's exact error shape."""
    try:
        details = exc.error_details
    except Exception:
        details = None
    if details:
        return {"error": str(details)}

    content = exc.content
    if isinstance(content, bytes):
        try:
            content = content.decode("utf-8")
        except Exception:
            content = str(content)

    try:
        parsed = json.loads(content)
    except Exception:
        return {}

    error = parsed.get("error")
    if isinstance(error, dict):
        message = error.get("message")
        if message:
            return {"error": message}
    elif error:
        return {"error": error}

    return {}
