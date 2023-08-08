from unittest.mock import patch

from pytest import mark
from pytest_httpx import HTTPXMock

import magic_scrape
from magic_scrape.scrape import Selector, detect_selectors, get_first_page

from .helpers.extraction import mock_extract


@mark.parametrize(
    "target,expected",
    [("animal", "body p i"), ("clothing", "body p em")],
)
def test_ai_extract_known_target_full_mock(target, expected, fake_page):
    with patch("magic_scrape.scrape.ai_extract", new=mock_extract):
        result = magic_scrape.scrape.ai_extract(target=target, page=fake_page)
        assert result == expected


@mark.parametrize(
    "target,expected",
    [("animal", "body p i"), ("clothing", "body p em")],
)
def test_ai_extract_known_target_page_mock(target, expected, fake_page, fake_config):
    fake_config.targets = [target]
    with patch("magic_scrape.scrape.get_first_page", return_value=fake_page):
        with patch("magic_scrape.scrape.ai_extract", new=mock_extract):
            result = detect_selectors(config=fake_config, debug=False, verbose=False)
            assert result == [Selector(target=target, css_pattern=expected)]


@mark.parametrize("target,expected", [("ghost", None)])
def test_ai_extract_unknown_target_full_mock(target, expected, fake_page):
    with patch("magic_scrape.scrape.ai_extract", new=mock_extract):
        result = magic_scrape.scrape.ai_extract(target=target, page=fake_page)
        assert result is expected


@mark.parametrize("target,expected", [("ghost", None)])
def test_ai_extract_unknown_target_page_mock(target, expected, fake_page, fake_config):
    fake_config.targets = [target]
    with patch("magic_scrape.scrape.get_first_page", return_value=fake_page):
        with patch("magic_scrape.scrape.ai_extract", new=mock_extract):
            result = detect_selectors(config=fake_config, debug=False, verbose=False)
            assert result == [Selector(target=target, css_pattern=expected)]


def test_full_scrape(fake_sitemap, sitemap_page_url, httpx_mock: HTTPXMock):
    httpx_mock.add_response(text=fake_sitemap)
    first_page = get_first_page(sitemap_url="http://example.com")
    assert first_page == sitemap_page_url
