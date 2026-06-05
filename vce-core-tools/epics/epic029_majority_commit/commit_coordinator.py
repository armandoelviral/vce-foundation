from epics.epic027_replicated_ledger.broadcast_append import (
    BroadcastAppend
)

from epics.epic029_majority_commit.durable_ack import (
    DurableAcknowledgement
)

from epics.epic029_majority_commit.majority_ack import (
    MajorityAcknowledgement
)


class CommitCoordinator:

    def commit(
        self,
        peers,
        event
    ):

        broadcaster = BroadcastAppend()

        results = broadcaster.broadcast(
            peers,
            event
        )

        durable = DurableAcknowledgement()

        acknowledgements = durable.filter(
            results
        )

        quorum = MajorityAcknowledgement()

        decision = quorum.evaluate(
            acknowledgements,
            len(peers)
        )

        return {
            "acks": acknowledgements,
            "decision": decision
        }
