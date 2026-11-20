from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ObserverIdentityCertificate:
    """Structural identity record; grants no trust or authority."""

    certificate_id: str
    observer_id: str
    key_id: str
    public_key_bytes: bytes
    platform_evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for field in (
            "certificate_id",
            "observer_id",
            "key_id",
        ):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field} must be a nonempty string")

        if type(self.public_key_bytes) is not bytes:
            raise TypeError("public_key_bytes must be bytes")

        if not self.public_key_bytes:
            raise ValueError("public_key_bytes must not be empty")

        if type(self.platform_evidence_ids) is not tuple:
            raise TypeError(
                "platform_evidence_ids must be an immutable tuple"
            )

        seen = set()
        for evidence_id in self.platform_evidence_ids:
            if (
                not isinstance(evidence_id, str)
                or not evidence_id.strip()
            ):
                raise ValueError(
                    "platform evidence_id must be a nonempty string"
                )

            if evidence_id in seen:
                raise ValueError("duplicate platform evidence_id")

            seen.add(evidence_id)
