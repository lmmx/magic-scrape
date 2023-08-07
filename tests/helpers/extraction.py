__all__ = ["mock_extract"]


def mock_extract(target: str, page: str) -> str | None:
    """Extract a CSS selector for the given target from the page URL content"""
    classified = {"animal": "rabbit", "clothing": "hat"}
    repertoire = {
        "rabbit": "body p i",
        "hat": "body p em",
    }
    cls_instance = classified.get(target)
    if cls_instance is None:
        css_pattern = None
    else:
        assert cls_instance in page, f"Classified {cls_instance} {target=} not in page"
        css_pattern = repertoire.get(cls_instance)
    return css_pattern
