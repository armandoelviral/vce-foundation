from epics.epic018_distributed_verification.quorum import (
    QuorumValidator
)


validator = QuorumValidator()


votes_pass = [
    {
        "payload": {
            "decision": "APPROVE"
        }
    },
    {
        "payload": {
            "decision": "APPROVE"
        }
    },
    {
        "payload": {
            "decision": "REJECT"
        }
    }
]


votes_fail = [
    {
        "payload": {
            "decision": "APPROVE"
        }
    },
    {
        "payload": {
            "decision": "REJECT"
        }
    },
    {
        "payload": {
            "decision": "REJECT"
        }
    }
]


print(
    validator.validate(
        votes_pass
    )["consensus"]
)


print(
    validator.validate(
        votes_fail
    )["consensus"]
)
