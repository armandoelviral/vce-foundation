from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetailEvaluationBindingReference:
    """Caller-declared expected binding revision for one evaluation."""

    evaluation_id: str
    binding_id: str
    expected_revision: int

    def __post_init__(self):
        for name in ("evaluation_id", "binding_id"):
            value = getattr(self, name)
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
        if type(self.expected_revision) is not int:
            raise TypeError("expected_revision must be an integer")
        if self.expected_revision < 1:
            raise ValueError("expected_revision must be positive")
