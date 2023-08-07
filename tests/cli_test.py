from unittest.mock import patch

import pytest
from pytest import mark

from magic_scrape.cli import CLIConfig, main

from .data.fixtures import dummy_page


def run_cli(*args, **env_vars):
    """Helper function to run the CLI command."""
    with patch("sys.argv", ["prog_name"] + list(args)):
        with patch.dict("os.environ", env_vars):
            with patch(
                "magic_scrape.scrape.get_first_page",
                return_value=dummy_page,
            ):
                return main(debug=True)


@mark.parametrize("key,url", [("a_key", "http://example.com")])
def test_openai_api_key_cli_arg(key, url):
    """Test when API key is provided via command line argument."""
    targets = "animal", "clothing"
    args = ["--openai-api-key", key, "--url", url, "--targets", *targets]
    result = run_cli(*args)
    expected = CLIConfig(openai_api_key=key, url=url, targets=targets)
    assert result.config == expected


@mark.parametrize("key,url", [("e_key", "http://example.com")])
def test_openai_api_key_env_var(key, url):
    """Test when API key is provided via environment variable."""
    targets = "animal", "clothing"
    args = ["--url", url, "--targets", *targets]
    env_vars = {"OPENAI_API_KEY": key}
    result = run_cli(*args, **env_vars)
    expected = CLIConfig(openai_api_key=key, url=url, targets=targets)
    assert result.config == expected


@mark.parametrize("arg_key,env_key,url", [("a_key", "e_key", "http://example.com")])
def test_openai_api_key_cli_arg_and_env_var(arg_key, env_key, url):
    """Test CLI argument overrides environment variable when both set the API key."""
    targets = "animal", "clothing"
    args = ["--openai-api-key", arg_key, "--url", url, "--targets", *targets]
    env_vars = {"OPENAI_API_KEY": env_key}
    result = run_cli(*args, **env_vars)
    expected = CLIConfig(openai_api_key=arg_key, url=url, targets=targets)
    assert result.config == expected


def test_missing_openai_api_key():
    """Test when API key is missing in both command line and environment variable."""
    targets = "animal", "clothing"
    args = ["--url", "http://example.com", "--targets", *targets]
    with pytest.raises(ValueError, match="OpenAI API key is missing"):
        run_cli(*args)
