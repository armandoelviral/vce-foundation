from epics.epic015_secure_runtime.recovery import (
    DeterministicRecovery
)

from epics.epic013_external_trust.immutable_ledger import (
    ImmutableLedgerStore
)


ledger = ImmutableLedgerStore()

ledger.append(
    {
        "state_hash": "abc123",
        "sequence_number": 1
    }
)


recovery = DeterministicRecovery()

result = recovery.recover(
    ledger
)


print(
    result["recovered"]
)


print(
    result["sequence"]
)
