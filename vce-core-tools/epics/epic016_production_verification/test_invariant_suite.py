from epics.epic016_production_verification.invariant_suite import (
    InvariantSuite
)


suite = InvariantSuite()


valid_runtime_state = {
    "execution": "VERIFIED",
    "trust": "ACCEPTED",
    "ledger": "COMMITTED",
    "tamper_evident": True
}


corrupted_runtime_state = {
    "execution": "VERIFIED",
    "trust": "ACCEPTED",
    "ledger": "MODIFIED",
    "tamper_evident": False
}


print(
    suite.verify_release_state(
        valid_runtime_state
    )["passed"]
)


print(
    suite.verify_release_state(
        corrupted_runtime_state
    )["passed"]
)
