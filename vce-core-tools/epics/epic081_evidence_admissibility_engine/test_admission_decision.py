from epics.epic081_evidence_admissibility_engine.admission_decision import (
    admit,
    reject,
)


def test_admission_decision_admits():

    decision = admit()

    assert decision.admitted is True
    assert decision.decision == "ADMIT"
    assert decision.reason == "ALL_ADMISSION_RULES_SATISFIED"


def test_admission_decision_rejects():

    decision = reject(
        "CPS_THRESHOLD_NOT_MET"
    )

    assert decision.admitted is False
    assert decision.decision == "REJECT"
    assert decision.reason == "CPS_THRESHOLD_NOT_MET"


def test_admission_decision_serializes():

    decision = reject(
        "CONTEXT_MISMATCH"
    )

    payload = decision.to_dict()

    assert payload["admitted"] is False
    assert payload["decision"] == "REJECT"
    assert payload["reason"] == "CONTEXT_MISMATCH"
