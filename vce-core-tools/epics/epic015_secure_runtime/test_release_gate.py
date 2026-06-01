from epics.epic015_secure_runtime.release_gate import (
    ReleaseCandidateGate
)


gate = ReleaseCandidateGate()


valid_report = {
    "secure_execution": True,
    "hardening": True,
    "trust": True,
    "ledger": True,
    "audit": True,
    "recovery": True
}


bad_report = {
    "secure_execution": True,
    "hardening": False,
    "trust": True
}


print(
    gate.validate(
        valid_report
    )
)


print(
    gate.validate(
        bad_report
    )
)
