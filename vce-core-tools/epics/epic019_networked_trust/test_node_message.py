from epics.epic019_networked_trust.node_message import NodeMessage


factory = NodeMessage()


message = factory.create(
    "node-001",
    "VOTE",
    {
        "artifact_hash": "abc123",
        "decision": "APPROVE"
    }
)


print(
    factory.validate(
        message
    )
)


del message["sender"]


print(
    factory.validate(
        message
    )
)
