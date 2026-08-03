"""Categories group: list_categories, batch_get_categories."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class CategoryData(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    displayName: str | None = None
    languageCode: str | None = None


class CategoriesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    categories: list[CategoryData] | None = None
    nextPageToken: str | None = None


class CategoriesResult(ToolResult):
    data: CategoriesData | None = None


class CategoryListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    categories: list[CategoryData] | None = None


class CategoryListResult(ToolResult):
    data: CategoryListData | None = None
