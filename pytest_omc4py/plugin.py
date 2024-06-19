from __future__ import annotations

import pytest
from os import PathLike
from typing import Union, Tuple, Protocol, Literal, overload
from omc4py import AsyncSession, Session

Use = Union[str, Tuple[str, str], PathLike[str]]


class SessionFactory(Protocol):
    @overload
    def __call__(self, asyncio: Literal[False] = False) -> Session:
        pass

    @overload
    def __call__(self, asyncio: Literal[True]) -> AsyncSession:
        pass


@pytest.fixture
def omc_uses() -> list[Use]:
    return [
        "Modelica",
    ]
