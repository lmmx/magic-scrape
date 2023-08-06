from __future__ import annotations

from sys import stderr
from typing import Literal, overload

import defopt
from pydantic import BaseModel

from .config import CLIConfig, cli_config_ctx
from .scrape import detect_selectors

__all__ = ["ReturnValue", "main"]


class ReturnValue(BaseModel):
    config: CLIConfig


@overload
def main(debug: Literal[True]) -> ReturnValue:
    ...


@overload
def main(debug: Literal[False] = False) -> None:
    ...


def main(debug: bool = False) -> ReturnValue | None:
    """CLI callable."""
    with cli_config_ctx(debug):
        config = defopt.run(CLIConfig)
        if debug:
            print(f"Loaded CLI config: {config}", file=stderr)
    select = detect_selectors(config=config, debug=debug)
    return ReturnValue(config=config, select=select) if debug else None


if __name__ == "__main__":
    main()
