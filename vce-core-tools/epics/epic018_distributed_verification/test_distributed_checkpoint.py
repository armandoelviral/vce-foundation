from epics.epic018_distributed_verification.distributed_checkpoint import (
    DistributedCheckpoint
)


ledger = DistributedCheckpoint()


ledger.append(
    "transcript-001"
)


ledger.append(
    "transcript-002"
)


print(
    ledger.verify_chain()
)


ledger.chain[0][
    "transcript_hash"
] = "tampered"


print(
    ledger.verify_chain()
)
