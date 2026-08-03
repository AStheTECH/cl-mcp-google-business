"""Performance group: get_daily_metrics_time_series, fetch_multi_daily_metrics_time_series,
list_search_keyword_impressions_monthly."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class DatedValueData(BaseModel):
    model_config = ConfigDict(extra="allow")

    date: dict | None = None
    value: str | None = None


class TimeSeriesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    datedValues: list[DatedValueData] | None = None


class DailyMetricsTimeSeriesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    timeSeries: TimeSeriesData | None = None


class DailyMetricsTimeSeriesResult(ToolResult):
    data: DailyMetricsTimeSeriesData | None = None


class DailyMetricTimeSeriesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    dailyMetric: str | None = None
    dailySubEntityType: dict | None = None
    timeSeries: TimeSeriesData | None = None


class MultiDailyMetricTimeSeriesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    dailyMetricTimeSeries: list[DailyMetricTimeSeriesData] | None = None


class MultiDailyMetricsTimeSeriesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    multiDailyMetricTimeSeries: list[MultiDailyMetricTimeSeriesData] | None = None


class MultiDailyMetricsTimeSeriesResult(ToolResult):
    data: MultiDailyMetricsTimeSeriesData | None = None


class InsightsValueData(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str | None = None
    threshold: str | None = None


class SearchKeywordCountData(BaseModel):
    model_config = ConfigDict(extra="allow")

    searchKeyword: str | None = None
    insightsValue: InsightsValueData | None = None


class SearchKeywordImpressionsMonthlyData(BaseModel):
    model_config = ConfigDict(extra="allow")

    searchKeywordsCounts: list[SearchKeywordCountData] | None = None
    nextPageToken: str | None = None


class SearchKeywordImpressionsMonthlyResult(ToolResult):
    data: SearchKeywordImpressionsMonthlyData | None = None
