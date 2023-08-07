from unittest.mock import patch

from pytest import mark
from pytest_httpx import HTTPXMock

from magic_scrape.scrape import ai_extract, get_first_page


def mock_extract(target: str, page: str) -> str | None:
    """Extract a CSS selector for the given target from the page URL content"""
    classified = {"animal": "rabbit", "clothing": "hat"}
    repertoire = {
        "rabbit": "body p i",
        "hat": "body p em",
    }
    cls_instance = classified.get(target)
    assert cls_instance, f"Cannot classify {target=} from mock repertoire"
    assert cls_instance in page, f"Classified {cls_instance} ({target=}) not in page"
    css_pattern = repertoire.get(cls_instance)
    return css_pattern


@mark.parametrize(
    "target,expected",
    [("animal", "body p i"), ("clothing", "body p em")],
)
def test_ai_extract_known_target(target, expected, dummy_page):
    with patch("magic_scrape.scrape.ai_extract", new=mock_extract):
        result = ai_extract(target=target, page=dummy_page)
        assert result == expected
    with patch("magic_scrape.scrape.get_first_page", return_value=dummy_page):
        result = ai_extract(target=target, page="")
        assert result == expected


@mark.parametrize("target,expected", [("ghost", None)])
def test_ai_extract_unknown_target(target, expected, dummy_page):
    with patch("magic_scrape.scrape.ai_extract", new=mock_extract):
        result = ai_extract(target=target, page=dummy_page)
        assert result is expected
    with patch("magic_scrape.scrape.get_first_page", return_value=dummy_page):
        result = ai_extract(target=target, page="")
        assert result is expected


def test_full_scrape(dummy_sitemap, sitemap_first_page_url, httpx_mock: HTTPXMock):
    httpx_mock.add_response(text=dummy_sitemap)
    first_page = get_first_page(sitemap_url="http://example.com")
    assert first_page == sitemap_first_page_url
