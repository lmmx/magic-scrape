from pytest import mark
from pytest_httpx import HTTPXMock

from magic_scrape import scrape
from magic_scrape.scrape import Selector, detect_selectors, get_first_page

from .helpers.data import target_css_mapping
from .helpers.extraction import mock_extract


@mark.parametrize("target, expected", target_css_mapping.items())
def test_ai_extract(target, expected, fake_page, mocker):
    """Patch the extract.ai_extract function after it's impored into scrape"""
    mocker.patch("magic_scrape.scrape.ai_extract", new=mock_extract)
    result = scrape.ai_extract(target=target, page=fake_page)
    assert result == expected


@mark.parametrize("target, expected", target_css_mapping.items())
def test_detect_selectors(target, expected, fake_page, fake_config, mocker):
    fake_config.targets = [target]
    mocker.patch("magic_scrape.scrape.get_first_page", return_value=fake_page)
    mocker.patch("magic_scrape.scrape.ai_extract", new=mock_extract)
    result = detect_selectors(config=fake_config, debug=False, verbose=False)
    assert result == [Selector(target=target, css_pattern=expected)]


def test_full_scrape(fake_sitemap, sitemap_page_url, httpx_mock: HTTPXMock):
    httpx_mock.add_response(text=fake_sitemap)
    first_page = get_first_page(sitemap_url="http://example.com")
    assert first_page == sitemap_page_url
