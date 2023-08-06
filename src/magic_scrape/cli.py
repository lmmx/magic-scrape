from __future__ import annotations

import defopt
from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic_settings import BaseSettings

__all__ = ["OpenAI", "APIConfig", "main"]


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
            raise ValueError("OpenAI API key is missing!")


class ScraperConfig(BaseModel):
    url: str


class CLIConfig(ScraperConfig, APIConfig):
    """
    Configure both the API key auth and web scrape settings.
    """


def main():
    config = defopt.run(CLIConfig)
    print("Loaded CLI config:", config)


if __name__ == "__main__":
    try:
        main()
    except ValidationError as ve:
        print(ve)
