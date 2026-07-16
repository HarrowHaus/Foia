from pril.sources.base import SearchResult


def test_search_result_serialization():
    result = SearchResult("x", "1", "Title", url="https://example.gov/1")
    payload = result.to_dict()
    assert payload["source_id"] == "x"
    assert payload["external_id"] == "1"
