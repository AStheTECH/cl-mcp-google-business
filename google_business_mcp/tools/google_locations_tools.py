"""google_locations group: search_google_locations"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.google_locations import GoogleLocationsData, GoogleLocationsResult
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("google-business-mcp.tools.google_locations")


def register_google_locations_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="search_google_locations",
        description=(
            "Searches all of the possible locations on Google that are a match to the "
            "specified request and returns the matching GoogleLocation entries. "
            "Exactly one of `location` or `query` must be provided."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def search_google_locations(
        page_size: int | None = Field(
            default=None,
            description="The number of matches to return. Default is 3, maximum is 10. No pagination.",
        ),
        location: dict | None = Field(
            default=None,
            description=(
                "Union field `search_query` — exactly one of `location` or `query` is required. "
                "Location to search for; if provided, finds locations matching the provided details."
            ),
        ),
        query: str | None = Field(
            default=None,
            description=(
                "Union field `search_query` — exactly one of `location` or `query` is required. "
                "Text query to search for. Less accurate than an exact location, but can surface "
                "more inexact matches."
            ),
        ),
    ) -> GoogleLocationsResult:
        tlog = ToolLogger(logger, "search_google_locations")

        if (location is None) == (query is None):
            return _err(
                GoogleLocationsResult, tlog, "VALIDATION_ERROR",
                "Exactly one of `location` or `query` must be provided.", 400,
            )

        try:
            svc = service.get_business_information_service()

            body = {}
            if page_size is not None:
                body["pageSize"] = page_size
            if location is not None:
                body["location"] = location
            if query is not None:
                body["query"] = query

            resp = svc.googleLocations().search(body=body).execute()

            tlog.success()
            return GoogleLocationsResult(success=True, statusCode=200, data=GoogleLocationsData(**resp))
        except Exception as exc:
            return _handle_request_exc(GoogleLocationsResult, tlog, exc)
