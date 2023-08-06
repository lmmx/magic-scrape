from __future__ import annotations

from contextlib import contextmanager
from sys import stderr
from typing import Iterator

from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic_settings import BaseSettings

__all__ = ["OpenAI", "APIConfig", "ScraperConfig", "CLIConfig", "cli_config_ctx"]


class OpenAI(BaseSettings):
    key: str = Field(..., validation_alias="openai_api_key")


class APIConfig(BaseModel):
    openai_api_key: str | None = None

    @field_validator("openai_api_key", mode="before")
    @classmethod
    def check_openai_api_key(cls, v: str | None):
        try:
            return v or OpenAI().key
        except ValidationError:
            raise ValueError(
                "OpenAI API key is missing: supply the CLI argument or "
                "set the OPENAI_API_KEY environment variable in your shell.",
            )


class ScraperConfig(BaseModel):
    url: str


class CLIConfig(ScraperConfig, APIConfig):
    """
    Configure both the API key auth and web scrape settings.

      :param openai_api_key: The OPENAI_API_KEY environment variable must be set if
                             this argument is not supplied
      :param url: URL of the sitemap for the website to scrape.
    """


@contextmanager
def cli_config_ctx(debug: bool = False) -> Iterator:
    """
    If config parsing raises a validation error, if `debug` is True, raise them.
    If not, print error to STDERR without traceback and exit with non-zero status code.
    """
    try:
        yield
    except ValidationError as ve:
        if debug:
            raise
        else:
            print(ve, file=stderr)
            exit(1)
