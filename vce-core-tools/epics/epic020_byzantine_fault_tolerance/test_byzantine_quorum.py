from epics.epic020_byzantine_fault_tolerance.byzantine_quorum import (
    ByzantineQuorum
)


quorum = ByzantineQuorum()


result_ok = quorum.validate(
    total_validators=4,
    approvals=3
)


result_fail = quorum.validate(
    total_validators=4,
    approvals=2
)


print(
    result_ok[
        "consensus"
    ]
)


print(
    result_fail[
        "consensus"
    ]
)


print(
    result_ok[
        "faults_tolerated"
    ]
)
