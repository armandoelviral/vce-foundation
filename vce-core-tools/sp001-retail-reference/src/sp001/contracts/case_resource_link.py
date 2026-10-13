from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CaseResourceLink:
    """Explicit reference from a case to a related module resource."""

    relationship: str
    resource_type: str
    resource_id: str

    def __post_init__(self) -> None:
        for field_name in ("relationship", "resource_type", "resource_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string")
            if not value.strip():
                raise ValueError(f"{field_name} must not be empty")
