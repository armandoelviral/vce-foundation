from ledger_admission import LedgerAdmissionController


controller = LedgerAdmissionController()


approved = {
    "ledger_admission": "APPROVED",
    "state_hash": "abc123",
    "sequence_number": 3
}


rejected = {
    "ledger_admission": "DENIED"
}


print(
    controller.admit(
        approved
    )["status"]
)


print(
    controller.admit(
        rejected
    )["status"]
)
