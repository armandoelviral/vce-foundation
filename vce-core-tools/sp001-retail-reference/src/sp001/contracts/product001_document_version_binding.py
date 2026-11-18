from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Product001DocumentVersionBinding:
    """Explicit commercial-to-document version mapping.

    This value records a mapping; it does not establish
    the authority or authenticity of that mapping.
    """

    source_id: str
    commercial_version: int
    document_version: str
    point_of_sale_id: str
    campaign_id: str

    def __post_init__(self) -> None:
        for field in (
            "source_id",
            "document_version",
            "point_of_sale_id",
            "campaign_id",
        ):
            value = getattr(self, field)

            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{field} must be a nonempty string"
                )

        if (
            type(self.commercial_version) is not int
            or self.commercial_version < 1
        ):
            raise ValueError(
                "commercial_version must be a positive integer"
            )
