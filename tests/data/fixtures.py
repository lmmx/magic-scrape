from pytest import fixture

__all__ = ["dummy_page", "sitemap_first_page_url", "dummy_sitemap"]


@fixture
def dummy_page() -> str:
    return (
        """<html>"""
        """  <body>"""
        """    <p><i>rabbit</i></p>"""
        """    <p><em>hat</em></p>"""
        """  </body>"""
        """</html>"""
    )


@fixture
def sitemap_first_page_url() -> str:
    return "https://pyfound.blogspot.com/2023/08/announcing-our-new-pypi-safety-security.html"


@fixture
def dummy_sitemap(sitemap_first_page_url) -> str:
    return (
        """<?xml version="1.0" encoding="UTF-8"?>"""
        """<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""
        """<url>"""
        f"""<loc>{sitemap_first_page_url}</loc>"""
        """<lastmod>2023-08-04T16:32:28Z</lastmod>"""
        """</url>"""
        """</urlset>"""
    )


# """<url><loc>https://pyfound.blogspot.com/2023/08/announcing-python-software-foundation.html</loc><lastmod>2023-08-02T14:51:09Z</lastmod></url>"""
# """<url><loc>https://pyfound.blogspot.com/2023/06/announcing-2023-psf-board-election.html</loc><lastmod>2023-07-01T00:13:47Z</lastmod></url>"""
