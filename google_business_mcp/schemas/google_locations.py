from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class GoogleLocationEntryData(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    location: dict | None = None
    requestAdminRightsUri: str | None = None


class GoogleLocationsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    googleLocations: list[GoogleLocationEntryData] | None = None


class GoogleLocationsResult(ToolResult):
    data: GoogleLocationsData | None = None
