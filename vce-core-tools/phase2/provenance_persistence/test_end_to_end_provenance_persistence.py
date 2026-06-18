from phase2.provenance_persistence.provenance_record import (
    ProvenanceRecord,
)

from phase2.provenance_persistence.provenance_store import (
    ProvenanceStore,
)

from phase2.provenance_persistence.provenance_query import (
    ProvenanceQuery,
)

from phase2.provenance_persistence.artifact_provenance_binding import (
    ArtifactProvenanceBinding,
)

from phase2.provenance_persistence.execution_provenance_binding import (
    ExecutionProvenanceBinding,
)

from phase2.provenance_persistence.provenance_verifier import (
    ProvenanceVerifier,
)

from phase2.provenance_persistence.provenance_report import (
    ProvenanceReport,
)


def test_end_to_end_provenance_flow():

    store = ProvenanceStore()

    record = ProvenanceRecord(
        subject_id="artifact-001",
        origin_id="execution-001",
        provenance_hash="hash-001",
    )

    store.add(record)

    query = ProvenanceQuery(
        store
    )

    recovered = query.by_subject(
        "artifact-001"
    )

    assert (
        recovered.origin_id
        == "execution-001"
    )

    artifact_binding = (
        ArtifactProvenanceBinding(
            artifact_id="artifact-001",
            provenance_hash="hash-001",
        )
    )

    assert (
        artifact_binding.provenance_hash
        == "hash-001"
    )

    execution_binding = (
        ExecutionProvenanceBinding(
            execution_id="execution-001",
            provenance_hash="hash-001",
        )
    )

    assert (
        execution_binding.provenance_hash
        == "hash-001"
    )

    verified = (
        ProvenanceVerifier.verify(
            recovered,
            expected_hash="hash-001",
        )
    )

    assert verified is True

    report = ProvenanceReport(
        [recovered]
    )

    assert (
        report.total_records()
        == 1
    )

    assert report.subject_ids() == [
        "artifact-001"
    ]
