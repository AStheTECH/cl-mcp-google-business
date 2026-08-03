"""Chains group: get_chain, search_chains."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.chains import ChainData, ChainResult, ChainsData, ChainsResult
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("google-business-mcp.tools.chains")


def register_chains_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_chain",
        description="Gets the specified chain, returning NOT_FOUND if the chain does not exist.",
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_chain(
        name: str = Field(description="The chain's resource name, in the format `chains/{chain_place_id}`."),
    ) -> ChainResult:
        tlog = ToolLogger(logger, "get_chain")

        try:
            svc = service.get_business_information_service()
            resp = svc.chains().get(name=name).execute()
            tlog.success()
            return ChainResult(success=True, statusCode=200, data=ChainData(**resp))
        except Exception as exc:
            return _handle_request_exc(ChainResult, tlog, exc)

    @mcp.tool(
        name="search_chains",
        description="Searches for a chain based on chain name and returns the list of matching chains.",
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def search_chains(
        chain_name: str = Field(
            description=(
                "Search for a chain by its name. Exact/partial/fuzzy/related queries are supported. "
                'Examples: "walmart", "wal-mart", "walmmmart", "沃尔玛".'
            )
        ),
        page_size: int = Field(
            default=10,
            description="The maximum number of matched chains to return from this query. Default is 10, maximum is 500.",
        ),
    ) -> ChainsResult:
        tlog = ToolLogger(logger, "search_chains")

        if page_size < 1 or page_size > 500:
            return _err(ChainsResult, tlog, "VALIDATION_ERROR", "page_size must be between 1 and 500", 400)

        try:
            svc = service.get_business_information_service()
            resp = svc.chains().search(chainName=chain_name, pageSize=page_size).execute()
            tlog.success()
            return ChainsResult(success=True, statusCode=200, data=ChainsData(**resp))
        except Exception as exc:
            return _handle_request_exc(ChainsResult, tlog, exc)
