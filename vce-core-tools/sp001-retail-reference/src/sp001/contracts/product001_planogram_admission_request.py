from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Product001PlanogramAdmissionRequest:
    """Commercial identifiers only; no documentary authority."""

    source_id: str
    source_version: int
    point_of_sale_id: str
    campaign_id: str

    def __post_init__(self) -> None:
        for field in (
            "source_id",
            "point_of_sale_id",
            "campaign_id",
        ):
            value = getattr(self, field)

            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{field} must be a nonempty string"
                )

        if (
            type(self.source_version) is not int
            or self.source_version < 1
        ):
            raise ValueError(
                "source_version must be a positive integer"
            )
