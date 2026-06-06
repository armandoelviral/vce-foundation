from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeOpcode:

    name: str

    payload: dict
