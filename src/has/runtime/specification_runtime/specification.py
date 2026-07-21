from __future__ import annotations

from dataclasses import dataclass

from .claim import Claim


@dataclass(frozen=True, slots=True)
class Specification:
    """
    Executable Specification.

    Represents one immutable executable
    Specification.
    """

    identifier: str

    claims: tuple[Claim, ...]
