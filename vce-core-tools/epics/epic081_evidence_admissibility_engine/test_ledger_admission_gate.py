from epics.epic081_evidence_admissibility_engine.admission_decision import (
    admit,
    reject,
)
from epics.epic081_evidence_admissibility_engine.ledger_admission_gate import (
    LedgerAdmissionGate,
)


def test_gate_allows_admitted_evidence():

    gate = LedgerAdmissionGate()

    assert gate.can_write(
        admit()
    ) is True


def test_gate_blocks_rejected_evidence():

    gate = LedgerAdmissionGate()

    assert gate.can_write(
        reject(
            "CPS_THRESHOLD_NOT_MET"
        )
    ) is False


def test_gate_returns_write_allowed_decision():

    gate = LedgerAdmissionGate()

    decision = gate.write_decision(
        admit()
    )

    assert decision["ledger_write_allowed"] is True
    assert decision["admission_status"] == "ADMITTED"


def test_gate_returns_rejection_decision():

    gate = LedgerAdmissionGate()

    decision = gate.write_decision(
        reject(
            "CONTEXT_MISMATCH"
        )
    )

    assert decision["ledger_write_allowed"] is False
    assert decision["admission_status"] == "REJECTED"
    assert decision["rejection_reason"] == "CONTEXT_MISMATCH"
