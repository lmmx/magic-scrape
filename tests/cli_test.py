from unittest import mock

import pytest

from magic_scrape.cli import CLIConfig, main

# from pydantic import ValidationError


# Helper function to run the CLI command
def run_cli(*args, **env_vars):
    with mock.patch("sys.argv", ["prog_name"] + list(args)):
        with mock.patch.dict("os.environ", env_vars):
            return main()


# Test when API key is provided via command line argument
def test_openai_api_key_cli_arg():
    args = ["--openai-api-key", "some_key", "--url", "http://example.com"]
    run_cli(*args)
    config = CLIConfig(openai_api_key="some_key", url="http://example.com")
    assert config


# Test when API key is provided via environment variable
def test_openai_api_key_env_var():
    args = ["--url", "http://example.com"]
    env_vars = {"OPENAI_API_KEY": "some_key_from_env"}
    run_cli(*args, **env_vars)
    config = CLIConfig(openai_api_key="some_key_from_env", url="http://example.com")
    assert config


# Test when API key is missing in both command line and environment variable
def test_missing_openai_api_key():
    args = ["--url", "http://example.com"]
    with pytest.raises(ValueError, match="OpenAI API key is missing"):
        run_cli(*args)


# Additional tests related to the ScraperConfig or other functionalities can be added similarly.
