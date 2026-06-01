import os

from epics.epic022_persistence.persistent_ledger import PersistentLedger
from epics.epic022_persistence.recovery_engine import RecoveryEngine


db_path = "test_recovery.db"

if os.path.exists(db_path):
    os.remove(db_path)


ledger = PersistentLedger(db_path)

ledger.append(
    "ATTESTATION",
    {
        "artifact": "runtime"
    }
)

ledger.append(
    "CHECKPOINT",
    {
        "state_hash": "abc123",
        "sequence_number": 7
    }
)

recovery = RecoveryEngine(db_path)

result = recovery.recover_checkpoint()

print(result["recovered"])
print(result["checkpoint"]["state_hash"])
print(result["checkpoint"]["sequence_number"])
