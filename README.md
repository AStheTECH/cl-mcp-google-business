**Manage Google Business Profile locations and performance insights — with Agents.**

A Model Context Protocol (MCP) server that exposes Google's My Business Business Information API and Business Profile Performance API for managing business location profiles, their attributes, and analyzing how those locations perform on Google Search and Maps.


## Overview

The mewcp-google-business MCP Server provides direct, OAuth-authenticated access to Google Business Profile location data and performance analytics:

- Full location lifecycle management — list, create, read, update, and delete locations and their custom attributes, with before/after records for every update
- Reference lookups against Google's category, chain, and attribute-metadata taxonomies, plus matching against Google's own location records
- Business Profile Performance analytics — daily and multi-metric time series and monthly search-keyword impression counts

The server reaches both upstream Google APIs — `mybusinessbusinessinformation` v1 and `businessprofileperformance` v1 — via OAuth: it exchanges your connected Google credential's access token for calls made through the official Google API Python Client SDK (`googleapiclient`), requesting the `https://www.googleapis.com/auth/business.manage` scope.

Perfect for:

- Agencies and business owners managing multi-location Business Profiles programmatically
- Marketing and operations teams tracking impressions, clicks, and search-keyword trends across locations
- Developers building Business Profile integrations that need category, attribute, and chain reference data alongside location CRUD


## Tools

### Locations

<details>
<summary><code>list_locations</code> — List locations for an account, with optional filtering, sorting, and pagination</summary>

Lists the locations for the specified account, optionally filtered and sorted, and returns the matching Location objects with pagination info.

**Inputs:**
```
- `parent` (string, required) — The name of the account to fetch locations from. If the parent Account is of type PERSONAL, only directly-owned Locations are returned; otherwise all accessible locations (direct or indirect) are returned.
- `read_mask` (string, required) — Comma-separated list of fully qualified field names to return. Example: "user.displayName,photo".
- `page_size` (integer, optional) — How many locations to fetch per page. Default 10, minimum 1, maximum 100.
- `page_token` (string, optional) — Fetches the next page; returned by a previous call when more locations exist than fit the page size.
- `filter_` (string, optional) — Filter constraining which locations to return. Empty means no constraints (all locations, paginated). See Google's "Work with Location Data" guide for valid fields.
- `order_by` (string, optional) — Comma-separated sort fields (SQL syntax). Default ascending; append " desc" for descending. Valid fields: title, storeCode. E.g. "title, storeCode desc".
```

**Output `data` schema:**

```typescript
{
  locations: {
    name: string;
    languageCode: string | null;
    storeCode: string | null;
    title: string | null;
    phoneNumbers: object | null;
    categories: object | null;
    storefrontAddress: object | null;
    websiteUri: string | null;
    regularHours: object | null;
    specialHours: object | null;
    serviceArea: object | null;
    labels: any[] | null;
    adWordsLocationExtensions: object | null;
    latlng: object | null;
    openInfo: object | null;
    metadata: object | null;
    profile: object | null;
    relationshipData: object | null;
    moreHours: any[] | null;
    serviceItems: any[] | null;
  }[];
  nextPageToken: string | null;
  totalSize: number | null;
}
```

</details>

<details>
<summary><code>create_location</code> — Create a new location owned by the authenticated user</summary>

Creates a new Location that will be owned by the logged-in user, and returns the newly created Location.

**Inputs:**
```
- `parent` (string, required) — The name of the account in which to create this location.
- `location` (object, required) — Location object to create. Required sub-fields: title (and primaryCategory within categories if categories are set).
- `validate_only` (boolean, optional) — If true, validates the request without actually creating the location.
- `request_id` (string, optional) — A unique request ID for the server to detect duplicate requests. UUIDs recommended. Max 50 characters.
```

**Output `data` schema:**

```typescript
{
  name: string;
  languageCode: string | null;
  storeCode: string | null;
  title: string | null;
  phoneNumbers: object | null;
  categories: object | null;
  storefrontAddress: object | null;
  websiteUri: string | null;
  regularHours: object | null;
  specialHours: object | null;
  serviceArea: object | null;
  labels: any[] | null;
  adWordsLocationExtensions: object | null;
  latlng: object | null;
  openInfo: object | null;
  metadata: object | null;
  profile: object | null;
  relationshipData: object | null;
  moreHours: any[] | null;
  serviceItems: any[] | null;
}
```

</details>

<details>
<summary><code>get_location</code> — Get a location's merchant-set field values</summary>

Returns the specified location as last set by the merchant; may not reflect updates from Google or user-generated content live on Google Maps.

**Inputs:**
```
- `name` (string, required) — The name of the location to fetch.
- `read_mask` (string, required) — Read mask specifying which fields to return in the response. Comma-separated list of fully qualified field names. Example: "title,websiteUri".
```

**Output `data` schema:**

```typescript
{
  name: string;
  languageCode: string | null;
  storeCode: string | null;
  title: string | null;
  phoneNumbers: object | null;
  categories: object | null;
  storefrontAddress: object | null;
  websiteUri: string | null;
  regularHours: object | null;
  specialHours: object | null;
  serviceArea: object | null;
  labels: any[] | null;
  adWordsLocationExtensions: object | null;
  latlng: object | null;
  openInfo: object | null;
  metadata: object | null;
  profile: object | null;
  relationshipData: object | null;
  moreHours: any[] | null;
  serviceItems: any[] | null;
}
```

</details>

<details>
<summary><code>update_location</code> — <strong>UPDATE</strong>: change specific fields on a location and get the before/after state</summary>

Updates the specified location's fields per the given update mask, and returns the updated Location. Only the fields you provide are changed — others keep their current value. NOTE: this overwrites the current field values — the original state is not stored after the call. The response includes both the before and after state so you have a full record of what changed.

**Inputs:**
```
- `location_name` (string, required) — Google identifier for this location, in the form locations/{locationId}.
- `update_mask` (string, required) — The specific fields to update. Comma-separated list of fully qualified field names.
- `location` (object, required) — Location object carrying the updated field values.
- `validate_only` (boolean, optional) — If true, validates the request without actually updating; response is empty unless there are validation errors.
```

**Output `data` schema:**

```typescript
{
  before: {
    name: string;
    languageCode: string | null;
    storeCode: string | null;
    title: string | null;
    phoneNumbers: object | null;
    categories: object | null;
    storefrontAddress: object | null;
    websiteUri: string | null;
    regularHours: object | null;
    specialHours: object | null;
    serviceArea: object | null;
    labels: any[] | null;
    adWordsLocationExtensions: object | null;
    latlng: object | null;
    openInfo: object | null;
    metadata: object | null;
    profile: object | null;
    relationshipData: object | null;
    moreHours: any[] | null;
    serviceItems: any[] | null;
  };
  after: {
    name: string;
    languageCode: string | null;
    storeCode: string | null;
    title: string | null;
    phoneNumbers: object | null;
    categories: object | null;
    storefrontAddress: object | null;
    websiteUri: string | null;
    regularHours: object | null;
    specialHours: object | null;
    serviceArea: object | null;
    labels: any[] | null;
    adWordsLocationExtensions: object | null;
    latlng: object | null;
    openInfo: object | null;
    metadata: object | null;
    profile: object | null;
    relationshipData: object | null;
    moreHours: any[] | null;
    serviceItems: any[] | null;
  };
}
```

</details>

<details>
<summary><code>delete_location</code> — <strong>DESTRUCTIVE</strong>: permanently delete a location (requires explicit user confirmation)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes the location. This action is irreversible — the location and its data cannot be recovered via this API (the Google Business Profile website may offer other recovery paths). NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `name` (string, required) — The name of the location to delete.
```

**Output `data` schema:**

```typescript
{
  // no fields — deletion is confirmed by the envelope's success/statusCode
}
```

</details>

<details>
<summary><code>get_google_updated_location</code> — Get a location as it appears live on Google Maps/Search, with diff and pending masks</summary>

Returns the specified location as it appears live on Google Maps and Search, which may differ from the merchant's version, along with masks of what Google changed and what's still pending.

**Inputs:**
```
- `name` (string, required) — The name of the location to fetch.
- `read_mask` (string, required) — Comma-separated list of fully qualified field names to return.
```

**Output `data` schema:**

```typescript
{
  location: object;
  diffMask: string | null;
  pendingMask: string | null;
}
```

</details>

<details>
<summary><code>get_location_attributes</code> — Get a location's merchant-set attributes</summary>

Retrieves attributes for a location as last set by the merchant.

**Inputs:**
```
- `name` (string, required) — Google identifier for this location, in the form locations/{locationId}/attributes.
```

**Output `data` schema:**

```typescript
{
  name: string;
  attributes: {
    name: string;
    valueType: string | null;
    values: any[] | null;
    repeatedEnumValue: object | null;
    uriValues: any[] | null;
  }[];
}
```

</details>

<details>
<summary><code>update_location_attributes</code> — <strong>UPDATE</strong>: change specific attributes on a location and get the before/after state</summary>

Updates attributes for a given location per the given attribute mask, and returns the updated Attributes. Only the fields you provide are changed — others keep their current value. NOTE: this overwrites the current field values — the original state is not stored after the call. The response includes both the before and after state so you have a full record of what changed.

**Inputs:**
```
- `attributes_name` (string, required) — Google identifier for this location, in the form locations/{locationId}/attributes.
- `attribute_mask` (string, required) — Attribute names (as attributes/{attribute}) to update. Every attribute you want updated must be in both attributes and attributeMask. To delete an attribute, put it in attributeMask with no matching entry in attributes.
- `name` (string, required) — Google identifier for this location, in the form locations/{locationId}/attributes (body field, same value as attributes.name).
- `attributes` (array<object>, optional) — The attributes to set (each with name, valueType, values, repeatedEnumValue, uriValues). May be empty when deleting all attributes via attributeMask.
```

**Output `data` schema:**

```typescript
{
  before: {
    name: string;
    attributes: {
      name: string;
      valueType: string | null;
      values: any[] | null;
      repeatedEnumValue: object | null;
      uriValues: any[] | null;
    }[];
  };
  after: {
    name: string;
    attributes: {
      name: string;
      valueType: string | null;
      values: any[] | null;
      repeatedEnumValue: object | null;
      uriValues: any[] | null;
    }[];
  };
}
```

</details>

<details>
<summary><code>get_google_updated_location_attributes</code> — Get a location's attributes as they appear live on Google Maps/Search</summary>

Retrieves attributes for a location as they appear live on Google Maps and Search, which may differ from the merchant's version.

**Inputs:**
```
- `name` (string, required) — Google identifier for this location, in the form locations/{locationId}/attributes.
```

**Output `data` schema:**

```typescript
{
  name: string;
  attributes: {
    name: string;
    valueType: string | null;
    values: any[] | null;
    repeatedEnumValue: object | null;
    uriValues: any[] | null;
  }[];
}
```

</details>


### Chains

<details>
<summary><code>get_chain</code> — Get a chain by resource name</summary>

Gets the specified chain, returning NOT_FOUND if the chain does not exist.

**Inputs:**
```
- `name` (string, required) — The chain's resource name, in the format `chains/{chain_place_id}`.
```

**Output `data` schema:**

```typescript
{
  name: string;
  chainNames: {
    displayName: string | null;
    languageCode: string | null;
  }[] | null;
  websites: {
    uri: string | null;
  }[] | null;
  locationCount: number | null;
}
```

</details>

<details>
<summary><code>search_chains</code> — Search chains by name</summary>

Searches for a chain based on chain name and returns the list of matching chains.

**Inputs:**
```
- `chain_name` (string, required) — Search for a chain by its name. Exact/partial/fuzzy/related queries are supported. Examples: "walmart", "wal-mart", "walmmmart", "沃尔玛".
- `page_size` (integer, optional, default: 10) — The maximum number of matched chains to return from this query. Default is 10, maximum is 500.
```

**Output `data` schema:**

```typescript
{
  chains: {
    name: string;
    chainNames: {
      displayName: string | null;
      languageCode: string | null;
    }[] | null;
    websites: {
      uri: string | null;
    }[] | null;
    locationCount: number | null;
  }[] | null;
}
```

</details>


### Categories

<details>
<summary><code>list_categories</code> — List business categories matching the front of a name</summary>

Returns a list of business categories matched by the front of the category name (e.g. 'food' matches 'Food Court' but not 'Fast Food Restaurant').

**Inputs:**
```
- `region_code` (string, required) — The ISO 3166-1 alpha-2 country code.
- `language_code` (string, required) — The BCP 47 code of the language.
- `view` (string, required) — Specifies which parts of the Category resource to return. Values: `CATEGORY_VIEW_UNSPECIFIED` (equivalent to `BASIC`), `BASIC` (only `displayName`, `category_id`, `languageCode`), `FULL` (all fields).
- `filter_` (string, optional) — Filter string from the user; the only supported field is `displayName`, e.g. `filter=displayName=foo`.
- `page_size` (integer, optional) — How many categories to fetch per page. Default is 100, minimum is 1, maximum is 100.
- `page_token` (string, optional) — If specified, fetches the next page of categories.
```

**Output `data` schema:**

```typescript
{
  categories: {
    name: string | null;
    displayName: string | null;
    languageCode: string | null;
  }[] | null;
  nextPageToken: string | null;
}
```

</details>

<details>
<summary><code>batch_get_categories</code> — Get business categories for a set of category IDs</summary>

Returns a list of business categories for the provided language and category (GConcept) IDs.

**Inputs:**
```
- `names` (array<string>, required) — The GConcept ids the localized category names should be returned for. Repeat this parameter to request more than one category; at least one name must be set.
- `language_code` (string, required) — The BCP 47 code of the language that the category names should be returned in.
- `view` (string, required) — Specifies which parts of the Category resource to return. Values: `CATEGORY_VIEW_UNSPECIFIED` (equivalent to `BASIC`), `BASIC` (only `displayName`, `category_id`, `languageCode`), `FULL` (all fields).
- `region_code` (string, optional) — The ISO 3166-1 alpha-2 country code used to infer non-standard language.
```

**Output `data` schema:**

```typescript
{
  categories: {
    name: string | null;
    displayName: string | null;
    languageCode: string | null;
  }[] | null;
}
```

</details>


### Attributes

<details>
<summary><code>list_available_attributes</code> — List attributes available for a location's category and country</summary>

Returns the list of attributes that would be available for a location with the given primary category and country. Provide exactly one of: `parent` (the resource name of an existing location), OR `category_name` together with `region_code` and `language_code`. Set `show_all` to true to get metadata for all available attributes regardless of `parent`/`category_name` — in that case `region_code` and `language_code` are required. Use `page_token` from a previous response to page through results.

**Inputs:**
```
- `parent` (string, optional) — Resource name of the location to look up available attributes for. If set, category_name, region_code, language_code and show_all are not required and must not be set.
- `category_name` (string, optional) — The primary category stable ID to find available attributes. Must be of the format categories/{category_id}.
- `region_code` (string, optional) — The ISO 3166-1 alpha-2 country code to find available attributes.
- `language_code` (string, optional) — The BCP 47 code of language to get attribute display names in. Falls back to English if unavailable.
- `show_all` (boolean, optional) — If true, metadata for all available attributes is returned, disregarding parent and category_name. region_code and language_code are required when this is true.
- `page_size` (integer, optional) — How many attributes to include per page. Default is 200, minimum is 1.
- `page_token` (string, optional) — If specified, the next page of attribute metadata is retrieved.
```

**Output `data` schema:**

```typescript
{
  attributeMetadata: {
    parent: string | null;
    valueType: string | null;
    displayName: string | null;
    groupDisplayName: string | null;
    repeatable: boolean | null;
    valueMetadata: any[] | null;
    deprecated: boolean | null;
  }[] | null;
  nextPageToken: string | null;
}
```

</details>


### Google Locations

<details>
<summary><code>search_google_locations</code> — Search Google's own location records by location details or text query</summary>

Searches all of the possible locations on Google that are a match to the specified request and returns the matching GoogleLocation entries. Exactly one of `location` or `query` must be provided.

**Inputs:**
```
- `page_size` (integer, optional) — The number of matches to return. Default is 3, maximum is 10. No pagination.
- `location` (object, optional) — Union field `search_query` — exactly one of `location` or `query` is required. Location to search for; if provided, finds locations matching the provided details.
- `query` (string, optional) — Union field `search_query` — exactly one of `location` or `query` is required. Text query to search for. Less accurate than an exact location, but can surface more inexact matches.
```

**Output `data` schema:**

```typescript
{
  googleLocations: {
    name: string | null;
    location: object | null;
    requestAdminRightsUri: string | null;
  }[] | null;
}
```

</details>


### Performance

<details>
<summary><code>get_daily_metrics_time_series</code> — Get a date-range time series for one daily metric</summary>

Returns the values for each date in a given time range for a single specified daily metric. Only daily data is available; hourly metrics are not supported.

**Inputs:**
```
- `name` (string, required) — The location for which the time series should be fetched. Format: `locations/{locationId}` where `locationId` is an unobfuscated listing id.
- `daily_metric` (string, required) — The metric to retrieve time series for. One of: `DAILY_METRIC_UNKNOWN`, `BUSINESS_IMPRESSIONS_DESKTOP_MAPS`, `BUSINESS_IMPRESSIONS_DESKTOP_SEARCH`, `BUSINESS_IMPRESSIONS_MOBILE_MAPS`, `BUSINESS_IMPRESSIONS_MOBILE_SEARCH`, `BUSINESS_CONVERSATIONS`, `BUSINESS_DIRECTION_REQUESTS`, `CALL_CLICKS`, `WEBSITE_CLICKS`, `BUSINESS_BOOKINGS`, `BUSINESS_FOOD_ORDERS`, `BUSINESS_FOOD_MENU_CLICKS`.
- `daily_range` (object, required) — The timerange to fetch. `{ "startDate": {"year", "month", "day"}, "endDate": {"year", "month", "day"} }`, both inclusive.
- `daily_sub_entity_type` (object, optional) — The sub-entity type/id the time series relates to. Currently no `DailyMetric` supports this (breakdown not available). Union of `dayOfWeek` (enum) or `timeOfDay` (`{"hours", "minutes", "seconds", "nanos"}`).
```

**Output `data` schema:**

```typescript
{
  timeSeries: {
    datedValues: {
      date: object | null;
      value: string | null;
    }[] | null;
  } | null;
}
```

</details>

<details>
<summary><code>fetch_multi_daily_metrics_time_series</code> — Get a date-range time series for multiple daily metrics at once</summary>

Returns the values for each date in a given time range for multiple specified daily metrics at once. Only daily data is available; hourly metrics are not supported.

**Inputs:**
```
- `location` (string, required) — The location for which the time series should be fetched. Format: `locations/{locationId}` where `locationId` is an unobfuscated listing id.
- `daily_metrics` (array<string>, required) — The metrics to retrieve time series for. Same enum values as `get_daily_metrics_time_series`. Repeat this parameter for multiple metrics.
- `daily_range` (object, required) — The timerange to fetch. `{ "startDate": {"year", "month", "day"}, "endDate": {"year", "month", "day"} }`, both inclusive.
```

**Output `data` schema:**

```typescript
{
  multiDailyMetricTimeSeries: {
    dailyMetricTimeSeries: {
      dailyMetric: string | null;
      dailySubEntityType: object | null;
      timeSeries: {
        datedValues: {
          date: object | null;
          value: string | null;
        }[] | null;
      } | null;
    }[] | null;
  }[] | null;
}
```

</details>

<details>
<summary><code>list_search_keyword_impressions_monthly</code> — List monthly search-keyword impression counts for a location</summary>

Returns the search keywords used to find a business in Search or Maps, each accompanied by impression counts aggregated on a monthly basis.

**Inputs:**
```
- `parent` (string, required) — The location for which the time series should be fetched. Format: `locations/{locationId}` where `locationId` is an unobfuscated listing id.
- `monthly_range` (object, required) — The range in months to aggregate search keyword impressions over. `{ "startMonth": {"year", "month", "day"}, "endMonth": {"year", "month", "day"} }`, both inclusive — only year and month are considered.
- `page_size` (integer, optional, default: 100) — Number of results requested. Default 100, maximum 100.
- `page_token` (string, optional) — Base64-encoded token indicating the next paginated result to return.
```

**Output `data` schema:**

```typescript
{
  searchKeywordsCounts: {
    searchKeyword: string | null;
    insightsValue: {
      value: string | null;
      threshold: string | null;
    } | null;
  }[] | null;
  nextPageToken: string | null;
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 400,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "VALIDATION_ERROR", "message": "page_size must be between 1 and 100", "details": null },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for validation and auth errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `VALIDATION_ERROR` (bad input, caught before the call is made), `AUTH_ERROR` (no OAuth access token on the credential), `UPSTREAM_ERROR` (Google's API returned an error status), `SERVER_ERROR` (unexpected failure).

</details>

<details>
<summary><strong>Common Parameters</strong></summary>

- `page_size` — Maximum number of results to return per page. Every list/search tool defines its own default and maximum — see that tool's Inputs.
- `page_token` — Opaque pagination token from a previous response's `nextPageToken` (or equivalent), used to fetch the next page of results.
- `filter_` — Tool-specific filter expression constraining which records are returned; the supported fields differ per tool (see `list_locations` and `list_categories`).

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Location:**

```
locations/{locationId}
Example: locations/12345678901234567890
```

**Location Attributes:**

```
locations/{locationId}/attributes
Example: locations/12345678901234567890/attributes
```

**Attribute:**

```
attributes/{attribute}
Example: attributes/has_wifi
```

**Chain:**

```
chains/{chain_place_id}
Example: chains/10248
```

**Category:**

```
categories/{category_id}
Example: categories/gcid:coffee_shop
```

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** OAuth access token not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_ACCESS_TOKEN` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check that your Google credential is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Google credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your Google account via OAuth
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Google Business Profile API Error</strong></summary>

- **Cause:** Upstream My Business Business Information API or Business Profile Performance API call returned an error
- **Solution:**
  1. Check the [Google Cloud Status Dashboard](https://status.cloud.google.com/) for outages
  2. Verify your Google account is an owner or manager of the business location, and that the `business.manage` scope was granted during OAuth
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[My Business Business Information API Reference](https://developers.google.com/my-business/reference/businessinformation/rest)** — Complete endpoint reference for locations, chains, categories, attributes, and Google Locations
- **[Business Profile Performance API Reference](https://developers.google.com/my-business/reference/performance/rest)** — Complete endpoint reference for performance metrics and search keyword impressions
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
