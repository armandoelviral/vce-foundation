from epics.epic029_majority_commit.durable_ack import (
    DurableAcknowledgement
)

ack = DurableAcknowledgement()

result = ack.filter(
    [
        {
            "peer": "node-a",
            "status": {
                "durable": True
            }
        },
        {
            "peer": "node-b",
            "status": {
                "durable": True
            }
        },
        {
            "peer": "node-c",
            "status": {
                "durable": False
            }
        }
    ]
)

print(result)
