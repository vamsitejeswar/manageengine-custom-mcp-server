"""Pagination metadata wrapper for ManageEngine API responses.

ManageEngine uses two field-name conventions for the total-record count:
  - dcapi endpoints (/dcapi/...):  "totalRecords"
  - api/1.4 endpoints:             "total"

Additional field names are probed in case a future endpoint differs.
The wrapper injects a canonical "_pagination" block so LLM callers always
have a reliable signal for total size, whether there are more pages, and
what to request next — regardless of which raw field the API happened to use.
"""

from __future__ import annotations

# Ordered by likelihood for ManageEngine Endpoint Central
_TOTAL_FIELDS = (
    "totalRecords",  # dcapi primary
    "total",         # api/1.4 primary
    "totalCount",
    "count",
    "totalItems",
    "records_count",
    "total_records",
)

_DATA_FIELDS = ("data", "records", "items", "results")


def wrap_paginated_response(
    raw: dict,
    page: int,
    pagelimit: int,
) -> dict:
    """Return a copy of *raw* with a '_pagination' key added.

    '_pagination' fields:
      page       – page number that was requested (1-based)
      pagelimit  – records-per-page that was requested
      returned   – number of records in this response (None if no list found)
      total      – API-reported grand total (None if not present in response)
      has_more   – True/False/None; None only when both total and returned are unknown
      next_page  – page+1 when has_more is True, else None
    """
    result = dict(raw)

    returned: int | None = None
    for field in _DATA_FIELDS:
        if field in raw and isinstance(raw[field], list):
            returned = len(raw[field])
            break

    total: int | None = None
    for field in _TOTAL_FIELDS:
        v = raw.get(field)
        if isinstance(v, (int, float)) and v >= 0:
            total = int(v)
            break

    if total is not None and returned is not None:
        offset = (page - 1) * pagelimit
        has_more: bool | None = (offset + returned) < total
    elif returned is not None:
        # Heuristic: a full page almost certainly means more records exist
        has_more = returned >= pagelimit
    else:
        has_more = None

    result["_pagination"] = {
        "page": page,
        "pagelimit": pagelimit,
        "returned": returned,
        "total": total,
        "has_more": has_more,
        "next_page": page + 1 if has_more else None,
    }
    return result


def wrap_offset_paginated_response(
    raw: dict,
    start_index: int,
    limit: int,
) -> dict:
    """Variant for offset-based endpoints (startIndex/limit, _FI/_PL).

    '_pagination' fields:
      start_index       – first-record offset that was requested (0-based)
      limit             – records requested
      returned          – records in this response
      total             – API-reported grand total (if available)
      has_more          – True/False/None
      next_start_index  – start_index+limit when has_more is True, else None
    """
    result = dict(raw)

    returned: int | None = None
    for field in _DATA_FIELDS:
        if field in raw and isinstance(raw[field], list):
            returned = len(raw[field])
            break

    total: int | None = None
    for field in _TOTAL_FIELDS:
        v = raw.get(field)
        if isinstance(v, (int, float)) and v >= 0:
            total = int(v)
            break

    if total is not None and returned is not None:
        has_more: bool | None = (start_index + returned) < total
    elif returned is not None:
        has_more = returned >= limit
    else:
        has_more = None

    result["_pagination"] = {
        "start_index": start_index,
        "limit": limit,
        "returned": returned,
        "total": total,
        "has_more": has_more,
        "next_start_index": start_index + limit if has_more else None,
    }
    return result
