from dataclasses import FrozenInstanceError, replace
import hashlib
import json
import os
from pathlib import Path

import pytest

from sp001.contracts.knowledge_governed_retrieval_evidence_storage_location import (
    KnowledgeGovernedRetrievalEvidenceStorageLocation,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    KnowledgeGovernedRetrievalEvidenceArtifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact_storage_serialization import (
    serialize_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_atomic_write import (
    KnowledgeGovernedRetrievalEvidenceWriteResult,
    write_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_digest import (
    KnowledgeGovernedRetrievalEvidenceDigest,
)
from test_knowledge_governed_retrieval_evidence_artifact import (
    create_artifact,
)


def create_location(
    tmp_path: Path,
    *,
    logical_name: str = "retrieval-run-001",
) -> KnowledgeGovernedRetrievalEvidenceStorageLocation:
    return KnowledgeGovernedRetrievalEvidenceStorageLocation(
        storage_root=tmp_path / "retrieval-evidence-storage",
        logical_name=logical_name,
    )


def digest_for(
    payload: str,
) -> KnowledgeGovernedRetrievalEvidenceDigest:
    return KnowledgeGovernedRetrievalEvidenceDigest(
        algorithm="SHA-256",
        encoding="UTF-8",
        value=hashlib.sha256(
            payload.encode(
                "utf-8",
            )
        ).hexdigest(),
    )


def test_atomic_write_persists_exact_canonical_artifact_envelope(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )

    artifact = create_artifact()

    write_knowledge_governed_retrieval_evidence_artifact(
        location=location,
        artifact=artifact,
    )

    expected = (
        serialize_knowledge_governed_retrieval_evidence_artifact(
            artifact=artifact,
        )
    )

    assert location.artifact_path.read_bytes() == (
        expected.encode(
            "utf-8",
        )
    )

    stored = json.loads(
        location.artifact_path.read_text(
            encoding="utf-8",
        )
    )

    assert stored["payload"] == artifact.payload
    assert stored["digest"]["value"] == artifact.digest.value


def test_atomic_write_creates_authorized_storage_root(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )

    assert not location.storage_root.exists()

    write_knowledge_governed_retrieval_evidence_artifact(
        location=location,
        artifact=create_artifact(),
    )

    assert location.storage_root.is_dir()


def test_atomic_write_returns_immutable_result(
    tmp_path: Path,
) -> None:
    result = write_knowledge_governed_retrieval_evidence_artifact(
        location=create_location(
            tmp_path,
        ),
        artifact=create_artifact(),
    )

    assert isinstance(
        result,
        KnowledgeGovernedRetrievalEvidenceWriteResult,
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        result.bytes_written = 0


def test_write_result_preserves_completed_write_facts(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )

    artifact = create_artifact()

    result = write_knowledge_governed_retrieval_evidence_artifact(
        location=location,
        artifact=artifact,
    )

    assert result.artifact_path == location.artifact_path
    assert result.digest == artifact.digest
    stored = serialize_knowledge_governed_retrieval_evidence_artifact(
        artifact=artifact,
    )

    assert result.bytes_written == len(
        stored.encode(
            "utf-8",
        )
    )


def test_atomic_write_replaces_existing_artifact(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )

    original = create_artifact(
        raw_text="original governed planogram",
    )

    replacement = create_artifact(
        raw_text="replacement governed planogram",
    )

    write_knowledge_governed_retrieval_evidence_artifact(
        location=location,
        artifact=original,
    )

    write_knowledge_governed_retrieval_evidence_artifact(
        location=location,
        artifact=replacement,
    )

    stored = json.loads(
        location.artifact_path.read_text(
            encoding="utf-8",
        )
    )

    assert stored["payload"] == replacement.payload
    assert "original governed planogram" not in stored["payload"]


def test_success_leaves_no_temporary_file(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )

    write_knowledge_governed_retrieval_evidence_artifact(
        location=location,
        artifact=create_artifact(),
    )

    assert tuple(
        location.storage_root.glob(
            ".*.tmp",
        )
    ) == ()


@pytest.mark.parametrize(
    "invalid_location",
    (
        None,
        {},
        (),
        "location",
    ),
)
def test_atomic_write_rejects_untyped_location(
    invalid_location: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeGovernedRetrievalEvidenceStorageLocation",
    ):
        write_knowledge_governed_retrieval_evidence_artifact(
            location=invalid_location,
            artifact=create_artifact(),
        )


@pytest.mark.parametrize(
    "invalid_artifact",
    (
        None,
        {},
        (),
        "artifact",
    ),
)
def test_atomic_write_rejects_untyped_artifact(
    tmp_path: Path,
    invalid_artifact: object,
) -> None:
    location = create_location(
        tmp_path,
    )

    with pytest.raises(
        TypeError,
        match="KnowledgeGovernedRetrievalEvidenceArtifact",
    ):
        write_knowledge_governed_retrieval_evidence_artifact(
            location=location,
            artifact=invalid_artifact,
        )

    assert not location.storage_root.exists()


def test_structurally_invalid_artifact_is_blocked_before_write(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )

    payload = "{}"

    artifact = KnowledgeGovernedRetrievalEvidenceArtifact(
        payload=payload,
        digest=digest_for(
            payload,
        ),
        media_type="application/json",
        schema_version=1,
    )

    with pytest.raises(
        ValueError,
    ):
        write_knowledge_governed_retrieval_evidence_artifact(
            location=location,
            artifact=artifact,
        )

    assert not location.storage_root.exists()


def test_digest_mismatch_is_blocked_before_write(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )

    artifact = create_artifact()

    modified = replace(
        artifact,
        payload=artifact.payload + " ",
    )

    with pytest.raises(
        ValueError,
    ):
        write_knowledge_governed_retrieval_evidence_artifact(
            location=location,
            artifact=modified,
        )

    assert not location.storage_root.exists()


def test_replace_receives_sibling_temporary_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    location = create_location(
        tmp_path,
    )

    observed = {}
    real_replace = os.replace

    def observing_replace(
        source: object,
        destination: object,
    ) -> None:
        observed["source"] = Path(
            source,
        )
        observed["destination"] = Path(
            destination,
        )

        real_replace(
            source,
            destination,
        )

    monkeypatch.setattr(
        "sp001.services."
        "knowledge_governed_retrieval_evidence_atomic_write."
        "os.replace",
        observing_replace,
    )

    write_knowledge_governed_retrieval_evidence_artifact(
        location=location,
        artifact=create_artifact(),
    )

    assert observed["source"].parent == (
        location.storage_root
    )

    assert observed["destination"] == (
        location.artifact_path
    )


def test_atomic_write_synchronizes_file_and_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    location = create_location(
        tmp_path,
    )

    descriptors = []

    def recording_fsync(
        descriptor: int,
    ) -> None:
        descriptors.append(
            descriptor,
        )

    monkeypatch.setattr(
        "sp001.services."
        "knowledge_governed_retrieval_evidence_atomic_write."
        "os.fsync",
        recording_fsync,
    )

    write_knowledge_governed_retrieval_evidence_artifact(
        location=location,
        artifact=create_artifact(),
    )

    assert len(
        descriptors,
    ) == 2

    assert all(
        isinstance(
            descriptor,
            int,
        )
        for descriptor in descriptors
    )


def test_replace_failure_preserves_existing_destination_and_cleans_temp(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    location = create_location(
        tmp_path,
    )

    original = create_artifact(
        raw_text="original governed planogram",
    )

    replacement = create_artifact(
        raw_text="replacement governed planogram",
    )

    write_knowledge_governed_retrieval_evidence_artifact(
        location=location,
        artifact=original,
    )

    original_bytes = location.artifact_path.read_bytes()

    def failing_replace(
        source: object,
        destination: object,
    ) -> None:
        raise OSError(
            "simulated replace failure"
        )

    monkeypatch.setattr(
        "sp001.services."
        "knowledge_governed_retrieval_evidence_atomic_write."
        "os.replace",
        failing_replace,
    )

    with pytest.raises(
        OSError,
        match="simulated replace failure",
    ):
        write_knowledge_governed_retrieval_evidence_artifact(
            location=location,
            artifact=replacement,
        )

    assert location.artifact_path.read_bytes() == (
        original_bytes
    )

    assert tuple(
        location.storage_root.glob(
            ".*.tmp",
        )
    ) == ()


def test_write_result_claims_no_authority_or_external_durability(
    tmp_path: Path,
) -> None:
    result = write_knowledge_governed_retrieval_evidence_artifact(
        location=create_location(
            tmp_path,
        ),
        artifact=create_artifact(),
    )

    for attribute in (
        "authority",
        "approved",
        "authenticity",
        "signature",
        "replicated",
        "backed_up",
        "remote_durability",
        "customer_acceptance",
    ):
        assert not hasattr(
            result,
            attribute,
        )


def test_atomic_write_requires_no_domain_evidence_reconstruction(
    tmp_path: Path,
) -> None:
    artifact = create_artifact()

    result = write_knowledge_governed_retrieval_evidence_artifact(
        location=create_location(
            tmp_path,
        ),
        artifact=artifact,
    )

    assert result.digest == artifact.digest
