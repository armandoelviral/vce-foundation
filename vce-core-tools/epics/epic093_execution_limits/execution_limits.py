from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionLimits:
    fuel: int
    timeout_ms: int
    memory_pages: int
