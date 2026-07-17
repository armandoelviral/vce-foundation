from __future__ import annotations

from enum import Enum


class Decision(Enum):
    """
    Normative conformance decisions.
    """

    CONFORMANT = "Conformant"

    NON_CONFORMANT = "Non-Conformant"

    @property
    def is_conformant(self) -> bool:
        return self is Decision.CONFORMANT

    @property
    def is_non_conformant(self) -> bool:
        return self is Decision.NON_CONFORMANT
