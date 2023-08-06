from __future__ import annotations

from typing import Literal, overload

import defopt
from pydantic import BaseModel

from .config import CLIConfig, cli_config_ctx
from .log import err
from .scrape import Selector, detect_selectors

__all__ = ["ReturnValue", "main"]


class ReturnValue(BaseModel):
    config: CLIConfig
    select: list[Selector]


@overload
def main(debug: Literal[True]) -> ReturnValue:
    ...


@overload
def main(debug: Literal[False] = False) -> None:
    ...


def main(debug: bool = False, verbose: bool = False) -> ReturnValue | None:
    """CLI callable."""
    verbose = True
    with cli_config_ctx(debug):
        config = defopt.run(CLIConfig)
        if verbose:
            err(f"Loaded CLI config: {config}")
    select = detect_selectors(config=config, debug=debug, verbose=verbose)
    if verbose:
        err(f"Produced result: {select}")
    ret = ReturnValue(config=config, select=select)
    return ret if debug else None


if __name__ == "__main__":
    main()
