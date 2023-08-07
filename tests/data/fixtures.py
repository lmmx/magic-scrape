from pytest import fixture

__all__ = ["dummy_page"]


@fixture
def dummy_page() -> str:
    body = """
    <p><i>rabbit</i></p>
    <p><em>hat</em></p>"""
    return f"""<html>\n  <body>{body}\n  </body>\n</html>"""
