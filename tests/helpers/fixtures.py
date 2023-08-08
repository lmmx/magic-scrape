from pytest import fixture

from magic_scrape.config import CLIConfig

__all__ = ["fake_config", "fake_page", "sitemap_page_url", "fake_sitemap"]


@fixture
def fake_config():
    """Test when API key is provided via command line argument."""
    key = "a_key"
    url = "http://example.com"
    targets = ["animal", "clothing"]
    return CLIConfig(openai_api_key=key, url=url, targets=targets)


@fixture
def fake_page() -> str:
    return (
        """<html>"""
        """  <body>"""
        """    <p><i>rabbit</i></p>"""
        """    <p><em>hat</em></p>"""
        """  </body>"""
        """</html>"""
    )


@fixture
def sitemap_page_url() -> str:
    return "https://pyfound.blogspot.com/2023/08/announcing-our-new-pypi-safety-security.html"


@fixture
def fake_sitemap(sitemap_page_url) -> str:
    return (
        """<?xml version="1.0" encoding="UTF-8"?>"""
        """<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""
        """<url>"""
        f"""<loc>{sitemap_page_url}</loc>"""
        """<lastmod>2023-08-04T16:32:28Z</lastmod>"""
        """</url>"""
        """</urlset>"""
    )


# """<url><loc>https://pyfound.blogspot.com/2023/08/announcing-python-software-foundation.html</loc><lastmod>2023-08-02T14:51:09Z</lastmod></url>"""
# """<url><loc>https://pyfound.blogspot.com/2023/06/announcing-2023-psf-board-election.html</loc><lastmod>2023-07-01T00:13:47Z</lastmod></url>"""
