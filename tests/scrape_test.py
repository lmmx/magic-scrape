from unittest.mock import patch

from pytest import mark
from pytest_httpx import HTTPXMock

import magic_scrape
from magic_scrape.scrape import ai_extract, get_first_page

from .extraction import mock_extract


@mark.parametrize(
    "target,expected",
    [("animal", "body p i"), ("clothing", "body p em")],
)
def test_ai_extract_known_target_full_mock(target, expected, dummy_page):
    with patch("magic_scrape.scrape.ai_extract", new=mock_extract):
        result = magic_scrape.scrape.ai_extract(target=target, page=dummy_page)
        assert result == expected


@mark.parametrize(
    "target,expected",
    [("animal", "body p i"), ("clothing", "body p em")],
)
def test_ai_extract_known_target_page_mock(target, expected, dummy_page):
    with patch("magic_scrape.scrape.get_first_page", return_value=dummy_page):
        result = ai_extract(target=target, page="")
        assert result == expected


@mark.parametrize("target,expected", [("ghost", None)])
def test_ai_extract_unknown_target_full_mock(target, expected, dummy_page):
    with patch("magic_scrape.scrape.ai_extract", new=mock_extract):
        result = magic_scrape.scrape.ai_extract(target=target, page=dummy_page)
        assert result is expected


@mark.parametrize("target,expected", [("ghost", None)])
def test_ai_extract_unknown_target_page_mock(target, expected, dummy_page):
    with patch("magic_scrape.scrape.get_first_page", return_value=dummy_page):
        result = magic_scrape.scrape.ai_extract(target=target, page="")
        assert result is expected


def test_full_scrape(dummy_sitemap, sitemap_first_page_url, httpx_mock: HTTPXMock):
    httpx_mock.add_response(text=dummy_sitemap)
    first_page = get_first_page(sitemap_url="http://example.com")
    assert first_page == sitemap_first_page_url
