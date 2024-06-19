from __future__ import annotations

import pytest
from os import PathLike

Use = str | tuple[str, str] | PathLike[str]


@pytest.fixture
def omc_uses() -> list[Use]:
    return [
        "Modelica",
    ]
