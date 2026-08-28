from dataclasses import dataclass
import re


@dataclass(frozen=True, slots=True)
class KnowledgeContentDigest:
    """Validated SHA-256 byte-content identity without authenticity claims."""

    algorithm: str
    value: str

    def __post_init__(self) -> None:
        if self.algorithm != "SHA-256":
            raise ValueError(
                "digest algorithm must be SHA-256"
            )

        if (
            not isinstance(
                self.value,
                str,
            )
            or re.fullmatch(
                r"[0-9a-f]{64}",
                self.value,
            )
            is None
        ):
            raise ValueError(
                "digest value must contain "
                "64 lowercase hexadecimal characters"
            )


@dataclass(frozen=True, slots=True)
class KnowledgeSourceIdentity:
    """Immutable versioned identity of one original knowledge source."""

    source_id: str
    source_version: str
    source_content_digest: KnowledgeContentDigest

    def __post_init__(self) -> None:
        identity_fields = {
            "source_id": self.source_id,
            "source_version": self.source_version,
        }

        for field, identity in identity_fields.items():
            if (
                not isinstance(
                    identity,
                    str,
                )
                or not identity.strip()
            ):
                raise ValueError(
                    f"{field} must not be empty"
                )

        if not isinstance(
            self.source_content_digest,
            KnowledgeContentDigest,
        ):
            raise TypeError(
                "source_content_digest must be a "
                "KnowledgeContentDigest"
            )
