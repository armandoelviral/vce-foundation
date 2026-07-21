from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """
    Specification execution result.
    """

    specification_identifier: str

    passed: bool

    evidence: tuple[str, ...]

    decision: str
