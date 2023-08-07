from unittest.mock import patch

from pytest import mark

from magic_scrape.scrape import ai_extract


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
