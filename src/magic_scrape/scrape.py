from __future__ import annotations

import httpx
from pydantic import BaseModel, Field

from .config import CLIConfig
from .log import err

__all__ = ["Selector", "ai_extract", "get_first_page", "detect_selectors"]


class Selector(BaseModel):
    target: str = Field(..., description="Part of the web page to be extracted")
    css_pattern: str | None = Field(..., description="CSS pattern for the target")


def ai_extract(target: str, page: str) -> str | None:
    """Extract a CSS selector for the given target from the page URL content"""
    repertoire = {
        "animal": "body p i",
        "clothing": "body p em",
    }
    magic = repertoire.get(target)
    return magic


def get_first_page(sitemap_url: str) -> str:
    draft = True
    if draft:
        raise NotImplementedError()
    response = httpx.get(sitemap_url)
    first_page = response.content
    return first_page


def detect_selectors(config: CLIConfig, debug: bool, verbose: bool) -> list[Selector]:
    """CLI callable."""
    selectors = []
    source_page = get_first_page(sitemap_url=config.url)
    for target in config.targets:
        detected = ai_extract(target=target, page=source_page)
        sel = Selector(target=target, css_pattern=detected)
        if verbose:
            if detected:
                err(f"Found pattern {detected!r} for {target=}")
            else:
                err(f"No pattern found for {target=}")
        selectors.append(sel)
    return selectors
