from __future__ import annotations

import pytest
from os import PathLike
from typing import Union, Tuple

Use = Union[str, Tuple[str, str], PathLike[str]]


@pytest.fixture
def omc_uses() -> list[Use]:
    return [
        "Modelica",
    ]
