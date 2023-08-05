from __future__ import annotations

import defopt
from pydantic import BaseModel, Field, ValidationError, model_validator
from pydantic_settings import BaseSettings

__all__ = ["Settings", "APIConfig"]


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")


class APIConfig(BaseModel):
    openai_api_key: str | None = Field(None, env="OPENAI_API_KEY")

    @model_validator(mode="before")
    def check_openai_api_key(cls, values):
        openai_api_key = values.get("openai_api_key")
        if not openai_api_key:
            try:
                settings = Settings()
                openai_api_key = settings.openai_api_key
                values["openai_api_key"] = openai_api_key
            except ValidationError as ve:
                raise ValueError("openai_api_key is missing!") from ve
        return values


defopt.run(APIConfig)
