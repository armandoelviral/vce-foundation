from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetailRuleCriterion:
    """Declared versioned criterion; does not establish approval or authority."""

    rule_id: str
    criterion_version: int
    statement: str

    def __post_init__(self) -> None:
        for name in ("rule_id", "statement"):
            value = getattr(self, name)
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

        if type(self.criterion_version) is not int:
            raise TypeError("criterion_version must be an integer")
        if self.criterion_version < 1:
            raise ValueError("criterion_version must be positive")
