from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class AttributeValueMetadataData(BaseModel):
    model_config = ConfigDict(extra="allow")
    # per-value metadata entry, keep minimal — extra="allow" covers undeclared fields


class AttributeMetadataData(BaseModel):
    model_config = ConfigDict(extra="allow")

    parent: str | None = None
    valueType: str | None = None
    displayName: str | None = None
    groupDisplayName: str | None = None
    repeatable: bool | None = None
    valueMetadata: list | None = None
    deprecated: bool | None = None


class AvailableAttributesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    attributeMetadata: list[AttributeMetadataData] | None = None
    nextPageToken: str | None = None


class AvailableAttributesResult(ToolResult):
    data: AvailableAttributesData | None = None
