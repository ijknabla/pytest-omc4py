from __future__ import annotations

import pytest
from os import PathLike
from typing import Union, Tuple, Protocol, Literal, overload, TYPE_CHECKING
from omc4py import AsyncSession, Session, open_session
from contextlib import ExitStack
import os

if TYPE_CHECKING:
    from collections.abc import Sequence, Iterator

    Use = Union[str, Tuple[str, Sequence[str]], PathLike[str]]
else:
    Use = ...


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


@pytest.fixture
def omc_session_factory(omc_uses: Sequence[Use]) -> Iterator[SessionFactory]:
    with ExitStack() as stack:

        @overload
        def session_factory(asyncio: Literal[False] = False) -> Session:
            pass

        @overload
        def session_factory(asyncio: Literal[True]) -> AsyncSession:
            pass

        def session_factory(
            asyncio: Literal[False, True] = False,
        ) -> Union[Session, AsyncSession]:
            session: Union[Session, AsyncSession] = stack.enter_context(  # type: ignore[assignment]
                open_session(asyncio=asyncio)
            )

            for use in omc_uses:
                if isinstance(use, os.PathLike):
                    assert session.synchronous.loadFile(use)
                elif isinstance(use, str):
                    assert any(
                        f(use)  # type: ignore[operator]
                        for f in [
                            session.synchronous.loadModel,
                            session.synchronous.loadFile,
                            session.synchronous.loadString,
                        ]
                    )
                else:
                    className, priorityVersion = use
                    assert session.synchronous.loadModel(
                        className=className,
                        priorityVersion=priorityVersion,
                    )

            return session

        yield session_factory
