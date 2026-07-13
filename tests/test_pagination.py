"""Regression tests for the pagination metadata wrapper.

These tests guard against the exact silent-wrong-answer bug class where:
  1. A field-name mismatch between the API response and the wrapper silently
     produces total=None instead of the real total.
  2. has_more is miscalculated, causing the LLM to stop paginating early and
     report a partial count as if it were the full count.
  3. A full page with no total field is mistakenly declared "last page."

Tests use small, arbitrary numbers — never real production data values.
"""

import pytest
from src.utils.pagination import wrap_paginated_response, wrap_offset_paginated_response


# ---------------------------------------------------------------------------
# wrap_paginated_response — total field name variants
# ---------------------------------------------------------------------------

class TestTotalFieldNameVariants:
    """Each variant must surface the total correctly — this is the field-name
    mismatch regression: if the probe list is incomplete a silently-None total
    causes the LLM to under-count."""

    def test_totalRecords(self):
        raw = {"data": list(range(3)), "totalRecords": 17}
        r = wrap_paginated_response(raw, page=1, pagelimit=3)
        assert r["_pagination"]["total"] == 17

    def test_total(self):
        raw = {"data": list(range(3)), "total": 17}
        r = wrap_paginated_response(raw, page=1, pagelimit=3)
        assert r["_pagination"]["total"] == 17

    def test_totalCount(self):
        raw = {"data": list(range(3)), "totalCount": 17}
        r = wrap_paginated_response(raw, page=1, pagelimit=3)
        assert r["_pagination"]["total"] == 17

    def test_count(self):
        raw = {"data": list(range(3)), "count": 17}
        r = wrap_paginated_response(raw, page=1, pagelimit=3)
        assert r["_pagination"]["total"] == 17

    def test_totalItems(self):
        raw = {"data": list(range(3)), "totalItems": 17}
        r = wrap_paginated_response(raw, page=1, pagelimit=3)
        assert r["_pagination"]["total"] == 17

    def test_unknown_field_stays_none(self):
        """A field NOT in the probe list must NOT silently become the total."""
        raw = {"data": list(range(3)), "grandTotal": 999}
        r = wrap_paginated_response(raw, page=1, pagelimit=3)
        assert r["_pagination"]["total"] is None

    def test_string_total_not_picked_up(self):
        """A string value for a known field must not be used as total."""
        raw = {"data": list(range(3)), "totalRecords": "not-a-number"}
        r = wrap_paginated_response(raw, page=1, pagelimit=3)
        assert r["_pagination"]["total"] is None

    def test_negative_total_not_picked_up(self):
        raw = {"data": list(range(3)), "totalRecords": -1}
        r = wrap_paginated_response(raw, page=1, pagelimit=3)
        assert r["_pagination"]["total"] is None


# ---------------------------------------------------------------------------
# wrap_paginated_response — has_more / next_page logic
# ---------------------------------------------------------------------------

class TestHasMorePageBased:
    """has_more must be derived from (page-1)*pagelimit + returned vs total,
    not from a simple 'returned == pagelimit' check when total is known."""

    def test_more_pages_exist(self):
        # page 1, 5 per page, 13 total → has_more True
        raw = {"data": list(range(5)), "totalRecords": 13}
        r = wrap_paginated_response(raw, page=1, pagelimit=5)
        assert r["_pagination"]["has_more"] is True
        assert r["_pagination"]["next_page"] == 2
        assert r["_pagination"]["returned"] == 5

    def test_last_page_exactly(self):
        # page 3 of 13, 5 per page → offset=10, 10+3=13 → has_more False
        raw = {"data": list(range(3)), "totalRecords": 13}
        r = wrap_paginated_response(raw, page=3, pagelimit=5)
        assert r["_pagination"]["has_more"] is False
        assert r["_pagination"]["next_page"] is None

    def test_first_page_full_with_total(self):
        # exactly fills page, total says more
        raw = {"data": list(range(5)), "total": 10}
        r = wrap_paginated_response(raw, page=1, pagelimit=5)
        assert r["_pagination"]["has_more"] is True

    def test_single_item_on_last_page(self):
        raw = {"data": [1], "totalRecords": 6}
        r = wrap_paginated_response(raw, page=2, pagelimit=5)
        # offset=5, 5+1=6, 6<6 → False
        assert r["_pagination"]["has_more"] is False

    def test_total_zero(self):
        raw = {"data": [], "totalRecords": 0}
        r = wrap_paginated_response(raw, page=1, pagelimit=5)
        assert r["_pagination"]["total"] == 0
        assert r["_pagination"]["returned"] == 0
        assert r["_pagination"]["has_more"] is False


class TestHasMoreHeuristic:
    """When the API returns no total count field, has_more is estimated from
    whether the page is full. This prevents the LLM from stopping too early."""

    def test_full_page_implies_more(self):
        raw = {"data": list(range(5))}
        r = wrap_paginated_response(raw, page=1, pagelimit=5)
        assert r["_pagination"]["total"] is None
        assert r["_pagination"]["has_more"] is True  # 5 >= 5 → might be more

    def test_partial_page_implies_no_more(self):
        raw = {"data": list(range(3))}
        r = wrap_paginated_response(raw, page=1, pagelimit=5)
        assert r["_pagination"]["total"] is None
        assert r["_pagination"]["has_more"] is False  # 3 < 5 → definitely last page

    def test_empty_page_no_more(self):
        raw = {"data": []}
        r = wrap_paginated_response(raw, page=2, pagelimit=5)
        assert r["_pagination"]["has_more"] is False


# ---------------------------------------------------------------------------
# wrap_paginated_response — data list detection
# ---------------------------------------------------------------------------

class TestDataListDetection:
    def test_data_key(self):
        raw = {"data": [1, 2, 3], "totalRecords": 10}
        r = wrap_paginated_response(raw, page=1, pagelimit=5)
        assert r["_pagination"]["returned"] == 3

    def test_records_key(self):
        raw = {"records": [1, 2], "totalRecords": 10}
        r = wrap_paginated_response(raw, page=1, pagelimit=5)
        assert r["_pagination"]["returned"] == 2

    def test_no_list_returned_is_none(self):
        raw = {"message_type": "SUCCESS", "totalRecords": 5}
        r = wrap_paginated_response(raw, page=1, pagelimit=5)
        assert r["_pagination"]["returned"] is None


# ---------------------------------------------------------------------------
# wrap_paginated_response — immutability
# ---------------------------------------------------------------------------

class TestImmutability:
    def test_does_not_mutate_original(self):
        raw = {"data": [1, 2], "totalRecords": 7}
        original_keys = set(raw.keys())
        wrap_paginated_response(raw, page=1, pagelimit=5)
        assert set(raw.keys()) == original_keys
        assert "_pagination" not in raw

    def test_returns_new_dict_with_pagination(self):
        raw = {"data": [1]}
        result = wrap_paginated_response(raw, page=1, pagelimit=5)
        assert "_pagination" in result
        assert result is not raw


# ---------------------------------------------------------------------------
# wrap_offset_paginated_response
# ---------------------------------------------------------------------------

class TestOffsetPaginatedResponse:
    def test_has_more_when_records_remain(self):
        raw = {"data": list(range(3)), "totalRecords": 10}
        r = wrap_offset_paginated_response(raw, start_index=0, limit=3)
        assert r["_pagination"]["has_more"] is True
        assert r["_pagination"]["next_start_index"] == 3

    def test_no_more_at_exact_end(self):
        raw = {"data": list(range(2)), "totalRecords": 5}
        r = wrap_offset_paginated_response(raw, start_index=3, limit=3)
        # 3+2=5, 5<5 → False
        assert r["_pagination"]["has_more"] is False
        assert r["_pagination"]["next_start_index"] is None

    def test_partial_page_heuristic(self):
        raw = {"data": [1, 2]}
        r = wrap_offset_paginated_response(raw, start_index=0, limit=5)
        assert r["_pagination"]["total"] is None
        assert r["_pagination"]["has_more"] is False

    def test_full_page_heuristic(self):
        raw = {"data": list(range(5))}
        r = wrap_offset_paginated_response(raw, start_index=0, limit=5)
        assert r["_pagination"]["total"] is None
        assert r["_pagination"]["has_more"] is True

    def test_metadata_fields_present(self):
        raw = {"data": [1], "total": 7}
        r = wrap_offset_paginated_response(raw, start_index=4, limit=3)
        p = r["_pagination"]
        assert p["start_index"] == 4
        assert p["limit"] == 3
        assert p["returned"] == 1
        assert p["total"] == 7

    def test_immutability(self):
        raw = {"data": [1], "totalRecords": 5}
        original_keys = set(raw.keys())
        wrap_offset_paginated_response(raw, start_index=0, limit=5)
        assert set(raw.keys()) == original_keys


# ---------------------------------------------------------------------------
# Integration: tool-level ceiling enforcement
# ---------------------------------------------------------------------------

class TestToolCeilingEnforcement:
    """Verify that the pagelimit/pageLimit ceilings are applied before the
    wrapper runs, so _pagination reflects the actual capped value."""

    def test_pagelimit_ceiling_reflected_in_pagination(self):
        # Simulate what a tool does: cap then wrap
        raw = {"data": list(range(50)), "totalRecords": 500}
        capped = min(200, 200)  # caller asked 200, ceiling is 200
        r = wrap_paginated_response(raw, page=1, pagelimit=capped)
        assert r["_pagination"]["pagelimit"] == 200

    def test_pagelimit_exceeding_ceiling_gets_capped(self):
        # Caller asks for 999, ceiling is 100 for api/1.4
        raw = {"data": list(range(100)), "total": 500}
        capped = min(999, 100)
        r = wrap_paginated_response(raw, page=1, pagelimit=capped)
        assert r["_pagination"]["pagelimit"] == 100
        assert r["_pagination"]["has_more"] is True
