from dataclasses import dataclass

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)


@dataclass(frozen=True, slots=True)
class KnowledgeExtractionIdentity:
    """Versioned extractor and exact configuration-byte identity."""

    extraction_id: str
    extractor_id: str
    extractor_version: str
    configuration_digest: KnowledgeContentDigest

    def __post_init__(self) -> None:
        identity_fields = {
            "extraction_id": self.extraction_id,
            "extractor_id": self.extractor_id,
            "extractor_version": self.extractor_version,
        }

        for field, identity in identity_fields.items():
            if (
                not isinstance(identity, str)
                or not identity.strip()
            ):
                raise ValueError(
                    f"{field} must not be empty"
                )

        if not isinstance(
            self.configuration_digest,
            KnowledgeContentDigest,
        ):
            raise TypeError(
                "configuration_digest must be a "
                "KnowledgeContentDigest"
            )


@dataclass(frozen=True, slots=True)
class KnowledgeDerivedArtifactIdentity:
    """Identity of exact bytes derived from one original source."""

    artifact_id: str
    artifact_version: str
    source_identity: KnowledgeSourceIdentity
    extraction_identity: KnowledgeExtractionIdentity
    artifact_content_digest: KnowledgeContentDigest

    def __post_init__(self) -> None:
        identity_fields = {
            "artifact_id": self.artifact_id,
            "artifact_version": self.artifact_version,
        }

        for field, identity in identity_fields.items():
            if (
                not isinstance(identity, str)
                or not identity.strip()
            ):
                raise ValueError(
                    f"{field} must not be empty"
                )

        if not isinstance(
            self.source_identity,
            KnowledgeSourceIdentity,
        ):
            raise TypeError(
                "source_identity must be a "
                "KnowledgeSourceIdentity"
            )

        if not isinstance(
            self.extraction_identity,
            KnowledgeExtractionIdentity,
        ):
            raise TypeError(
                "extraction_identity must be a "
                "KnowledgeExtractionIdentity"
            )

        if not isinstance(
            self.artifact_content_digest,
            KnowledgeContentDigest,
        ):
            raise TypeError(
                "artifact_content_digest must be a "
                "KnowledgeContentDigest"
            )


@dataclass(frozen=True, slots=True)
class KnowledgeFragmentIdentity:
    """Half-open byte range and digest within one derived artifact."""

    fragment_id: str
    artifact_identity: KnowledgeDerivedArtifactIdentity
    sequence_number: int
    byte_start: int
    byte_end: int
    fragment_content_digest: KnowledgeContentDigest

    def __post_init__(self) -> None:
        if (
            not isinstance(self.fragment_id, str)
            or not self.fragment_id.strip()
        ):
            raise ValueError(
                "fragment_id must not be empty"
            )

        if not isinstance(
            self.artifact_identity,
            KnowledgeDerivedArtifactIdentity,
        ):
            raise TypeError(
                "artifact_identity must be a "
                "KnowledgeDerivedArtifactIdentity"
            )

        integer_fields = {
            "sequence_number": self.sequence_number,
            "byte_start": self.byte_start,
            "byte_end": self.byte_end,
        }

        for field, value in integer_fields.items():
            if (
                isinstance(value, bool)
                or not isinstance(value, int)
            ):
                raise TypeError(
                    f"{field} must be an integer"
                )

        if self.sequence_number < 0:
            raise ValueError(
                "sequence_number must not be negative"
            )

        if self.byte_start < 0:
            raise ValueError(
                "byte_start must not be negative"
            )

        if self.byte_end <= self.byte_start:
            raise ValueError(
                "byte_end must be greater than byte_start"
            )

        if not isinstance(
            self.fragment_content_digest,
            KnowledgeContentDigest,
        ):
            raise TypeError(
                "fragment_content_digest must be a "
                "KnowledgeContentDigest"
            )


@dataclass(frozen=True, slots=True)
class KnowledgeFragmentSet:
    """Ordered non-overlapping fragment identities for one artifact."""

    artifact_identity: KnowledgeDerivedArtifactIdentity
    fragments: tuple[KnowledgeFragmentIdentity, ...]

    def __post_init__(self) -> None:
        if not isinstance(
            self.artifact_identity,
            KnowledgeDerivedArtifactIdentity,
        ):
            raise TypeError(
                "artifact_identity must be a "
                "KnowledgeDerivedArtifactIdentity"
            )

        if not isinstance(self.fragments, tuple):
            raise TypeError(
                "fragments must be an immutable tuple"
            )

        seen_fragment_ids: set[str] = set()
        seen_sequence_numbers: set[int] = set()
        previous_end: int | None = None

        for fragment in self.fragments:
            if not isinstance(
                fragment,
                KnowledgeFragmentIdentity,
            ):
                raise TypeError(
                    "fragments must contain "
                    "KnowledgeFragmentIdentity values"
                )

            if fragment.artifact_identity != self.artifact_identity:
                raise ValueError(
                    "fragment must reference set artifact"
                )

            if fragment.fragment_id in seen_fragment_ids:
                raise ValueError(
                    "duplicate fragment_id: "
                    f"{fragment.fragment_id}"
                )

            seen_fragment_ids.add(fragment.fragment_id)

            if (
                fragment.sequence_number
                in seen_sequence_numbers
            ):
                raise ValueError(
                    "duplicate fragment sequence_number: "
                    f"{fragment.sequence_number}"
                )

            seen_sequence_numbers.add(
                fragment.sequence_number,
            )

            if (
                previous_end is not None
                and fragment.byte_start < previous_end
            ):
                raise ValueError(
                    "fragments must not overlap "
                    "in declared order"
                )

            previous_end = fragment.byte_end
