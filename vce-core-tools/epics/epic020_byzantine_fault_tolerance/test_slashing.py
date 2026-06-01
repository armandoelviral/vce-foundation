from epics.epic020_byzantine_fault_tolerance.slashing import (
    SlashingEvidence
)


slashing = SlashingEvidence()


record = slashing.create(
    {
        "node_id": "node-X",
        "attack": "DOUBLE_VOTE"
    }
)


print(
    slashing.verify(
        record
    )
)


record[
    "evidence"
][
    "attack"
] = "MODIFIED"


print(
    slashing.verify(
        record
    )
)
