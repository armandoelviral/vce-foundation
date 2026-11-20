from dataclasses import dataclass

from sp001.contracts.product001_host_admission import (
    REQUIRED_CHECK_IDS,
)


@dataclass(frozen=True, slots=True)
class ObservationMandate:
    """Structural observation scope; grants no authority."""

    mandate_id: str
    issuer_id: str
    observer_id: str
    host_id: str
    resource_ids: tuple[str, ...]
    check_ids: tuple[str, ...]
    policy_version: str
    valid_from: int
    valid_until: int

    def __post_init__(self) -> None:
        for field in (
            "mandate_id",
            "issuer_id",
            "observer_id",
            "host_id",
            "policy_version",
        ):
            value = getattr(self, field)
            if type(value) is not str or not value.strip():
                raise ValueError(
                    f"{field} must be a nonempty string"
                )

        for field in ("resource_ids", "check_ids"):
            values = getattr(self, field)

            if type(values) is not tuple:
                raise TypeError(
                    f"{field} must be an immutable tuple"
                )

            if not values:
                raise ValueError(
                    f"{field} must not be empty"
                )

            seen = set()

            for value in values:
                if type(value) is not str or not value.strip():
                    raise ValueError(
                        f"{field} must contain nonempty strings"
                    )

                if value in seen:
                    raise ValueError(
                        f"{field} must not contain duplicates"
                    )

                seen.add(value)

        if not set(self.check_ids).issubset(
            REQUIRED_CHECK_IDS
        ):
            raise ValueError(
                "check_ids must belong to HOST-P01..HOST-P10"
            )

        if type(self.valid_from) is not int:
            raise TypeError("valid_from must be an integer")

        if type(self.valid_until) is not int:
            raise TypeError("valid_until must be an integer")

        if self.valid_from < 0 or self.valid_until < 0:
            raise ValueError(
                "validity timestamps must be nonnegative"
            )

        if self.valid_from >= self.valid_until:
            raise ValueError(
                "valid_from must precede valid_until"
            )
