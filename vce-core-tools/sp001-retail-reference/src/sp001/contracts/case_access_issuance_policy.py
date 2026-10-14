from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CaseAccessIssuancePolicy:
    """Trusted server configuration, never supplied by the requester."""

    primary_audience: str
    access_issuer: str
    access_audience: str
    signing_key_id: str
    max_lifetime_seconds: int

    def __post_init__(self):
        for name in (
            "primary_audience", "access_issuer", "access_audience", "signing_key_id",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a nonempty string")
        if type(self.max_lifetime_seconds) is not int or self.max_lifetime_seconds <= 0:
            raise ValueError("max_lifetime_seconds must be a positive integer")
