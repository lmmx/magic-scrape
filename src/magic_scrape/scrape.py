from __future__ import annotations

import httpx
from pydantic import BaseModel, Field
from pydantic_xml import BaseXmlModel, element

from .config import CLIConfig
from .log import err

__all__ = ["Selector", "ai_extract", "get_first_page", "detect_selectors"]

NSMAP = {"": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class Selector(BaseModel):
    target: str = Field(..., description="Part of the web page to be extracted")
    css_pattern: str | None = Field(..., description="CSS pattern for the target")


def ai_extract(target: str, page: str) -> str | None:
    """Extract a CSS selector for the given target from the page URL content"""
    raise NotImplementedError("Insert OpenAI extraction magic here")


class Url(BaseXmlModel, tag="url", nsmap=NSMAP):  # type: ignore[call-arg]
    loc: str | None = element(default=None)
    lastmod: str | None = element(default=None)


class UrlSet(BaseXmlModel, tag="urlset", nsmap=NSMAP):  # type: ignore[call-arg]
    urls: list[Url] = element()


def get_first_page(sitemap_url: str) -> str:
    response = httpx.get(sitemap_url)
    sitemap = response.content
    site_model = UrlSet.from_xml(sitemap)
    first_page = site_model.urls[0]
    return first_page.loc


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
