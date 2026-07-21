from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Claim:
    """
    Executable Claim.

    Represents one normative Claim.
    """

    identifier: str

    statement: str

    contract: str
