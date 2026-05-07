"""
Hermetic unit tests for the search-URL discovery regex.

These don't hit the network and are intended to catch silent regressions
when HLTB rotates their endpoint name (which they do periodically — most
recently from /api/finder to /api/bleed).
"""
from unittest import TestCase

from howlongtobeatpy.HTMLRequests import SearchInformations


# Real shape captured from HLTB's Turbopack chunk on 2026-05-07. If HLTB
# rotates the endpoint name again, update this fixture to the new shape and
# the tests should still pass without code changes.
BLEED_CHUNK_SHAPE = (
    '...he:!(u?.user_id>0)};a&&(s[a]=l);'
    'let i=await fetch("/api/bleed",{method:"POST",'
    'headers:{"Content-Type":"application/json",'
    '"x-auth-token":t,"x-hp-key":a,"x-hp-val":l},'
    'body:JSON.stringify(s)});'
    'if(403===i.status&&!e){...'
)


class TestSearchUrlExtraction(TestCase):

    def test_extracts_current_api_bleed_endpoint(self):
        info = SearchInformations(BLEED_CHUNK_SHAPE)
        self.assertEqual("api/bleed", info.search_url)

    def test_extracts_a_hypothetical_future_endpoint(self):
        future = BLEED_CHUNK_SHAPE.replace("/api/bleed", "/api/somethingnew")
        info = SearchInformations(future)
        self.assertEqual("api/somethingnew", info.search_url)

    def test_returns_none_when_no_post_fetch_present(self):
        info = SearchInformations('var x = 1; console.log("hello")')
        self.assertIsNone(info.search_url)

    def test_ignores_get_only_fetches(self):
        get_only = 'fetch("/api/bleed",{method:"GET"})'
        info = SearchInformations(get_only)
        self.assertIsNone(info.search_url)

    def test_extracts_root_path_from_versioned_endpoint(self):
        versioned = BLEED_CHUNK_SHAPE.replace("/api/bleed", "/api/bleed/v2")
        info = SearchInformations(versioned)
        self.assertEqual("api/bleed", info.search_url)
