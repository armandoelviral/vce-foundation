from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RuntimeResult:
    """Result returned by a Scientific Product Runtime transition."""

    output: Any
    transition: str
    success: bool = True
