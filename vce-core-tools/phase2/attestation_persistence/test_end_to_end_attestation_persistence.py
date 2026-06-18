from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)

from phase2.attestation_persistence.state_attestation import (
    StateAttestation,
)

from phase2.attestation_persistence.attestation_store import (
    AttestationStore,
)

from phase2.attestation_persistence.attestation_query import (
    AttestationQuery,
)

from phase2.attestation_persistence.attestation_verifier import (
    AttestationVerifier,
)

from phase2.attestation_persistence.attestation_report import (
    AttestationReport,
)


def test_end_to_end_attestation_flow():

    state = RuntimeState(
        events_applied=3,
        last_lsn=3,
        state_hash="state-hash-001",
    )

    record = StateAttestation.attest(
        attestation_id="att-001",
        state=state,
    )

    store = AttestationStore()

    store.add(record)

    assert store.count() == 1

    query = AttestationQuery(store)

    results = query.by_subject(
        "runtime-state"
    )

    assert len(results) == 1

    verified = AttestationVerifier.verify(
        results[0],
        "state-hash-001",
    )

    assert verified is True

    report = AttestationReport(
        results
    )

    assert (
        report.total_attestations()
        == 1
    )

    assert report.subjects() == [
        "runtime-state"
    ]
