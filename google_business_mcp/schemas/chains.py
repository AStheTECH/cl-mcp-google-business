"""Chains group: get_chain, search_chains."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class ChainNameData(BaseModel):
    model_config = ConfigDict(extra="allow")

    displayName: str | None = None
    languageCode: str | None = None


class ChainUriData(BaseModel):
    model_config = ConfigDict(extra="allow")

    uri: str | None = None


class ChainData(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    chainNames: list[ChainNameData] | None = None
    websites: list[ChainUriData] | None = None
    locationCount: int | None = None


class ChainResult(ToolResult):
    data: ChainData | None = None


class ChainsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    chains: list[ChainData] | None = None


class ChainsResult(ToolResult):
    data: ChainsData | None = None
