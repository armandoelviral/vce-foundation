from dataclasses import dataclass

from sp001.contracts.knowledge_derived_artifact import (
    KnowledgeDerivedArtifactIdentity,
    KnowledgeFragmentSet,
)


@dataclass(frozen=True, slots=True)
class KnowledgeIngestionRecord:
    """One immutable derived artifact and its declared fragment set."""

    ingestion_id: str
    artifact_identity: KnowledgeDerivedArtifactIdentity
    fragment_set: KnowledgeFragmentSet

    def __post_init__(self) -> None:
        if (
            not isinstance(self.ingestion_id, str)
            or not self.ingestion_id.strip()
        ):
            raise ValueError(
                "ingestion_id must not be empty"
            )

        if not isinstance(
            self.artifact_identity,
            KnowledgeDerivedArtifactIdentity,
        ):
            raise TypeError(
                "artifact_identity must be a "
                "KnowledgeDerivedArtifactIdentity"
            )

        if not isinstance(
            self.fragment_set,
            KnowledgeFragmentSet,
        ):
            raise TypeError(
                "fragment_set must be a KnowledgeFragmentSet"
            )

        if (
            self.fragment_set.artifact_identity
            != self.artifact_identity
        ):
            raise ValueError(
                "fragment_set must describe artifact_identity"
            )

    @property
    def artifact_key(self) -> tuple[str, str]:
        return (
            self.artifact_identity.artifact_id,
            self.artifact_identity.artifact_version,
        )


@dataclass(frozen=True, slots=True)
class KnowledgeIngestionRegistry:
    """Ordered conflict-free registry of ingested artifact records."""

    records: tuple[KnowledgeIngestionRecord, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.records, tuple):
            raise TypeError(
                "records must be an immutable tuple"
            )

        seen_ingestion_ids: set[str] = set()
        seen_artifact_keys: set[tuple[str, str]] = set()

        for record in self.records:
            if not isinstance(
                record,
                KnowledgeIngestionRecord,
            ):
                raise TypeError(
                    "records must contain "
                    "KnowledgeIngestionRecord values"
                )

            if record.ingestion_id in seen_ingestion_ids:
                raise ValueError(
                    "duplicate ingestion_id: "
                    f"{record.ingestion_id}"
                )

            seen_ingestion_ids.add(record.ingestion_id)

            if record.artifact_key in seen_artifact_keys:
                raise ValueError(
                    "duplicate artifact key: "
                    f"{record.artifact_key[0]} "
                    f"{record.artifact_key[1]}"
                )

            seen_artifact_keys.add(record.artifact_key)
