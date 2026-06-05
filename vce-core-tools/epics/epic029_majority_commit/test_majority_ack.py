from epics.epic029_majority_commit.majority_ack import (
    MajorityAcknowledgement
)

ack = MajorityAcknowledgement()

result = ack.evaluate(
    acknowledgements=[
        "node-a",
        "node-b"
    ],
    total_nodes=3
)

print(result)
