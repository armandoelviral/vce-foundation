from epics.epic013_external_trust.ledger_admission import (
    LedgerAdmissionController,
)


def test_admits_approved_entry():

    controller = LedgerAdmissionController()

    approved = {
        "ledger_admission": "APPROVED",
        "state_hash": "abc123",
        "sequence_number": 3,
    }

    result = controller.admit(
        approved
    )

    assert result["status"] == "COMMITTED"


def test_rejects_denied_entry():

    controller = LedgerAdmissionController()

    rejected = {
        "ledger_admission": "DENIED",
    }

    result = controller.admit(
        rejected
    )

    assert result["status"] != "COMMITTED"
