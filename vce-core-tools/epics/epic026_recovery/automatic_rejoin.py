from epics.epic026_recovery.recovery_handshake import (
    RecoveryHandshake
)

from epics.epic026_recovery.state_selector import (
    StateSelector
)

from epics.epic026_recovery.state_pull import (
    StatePull
)

from epics.epic026_recovery.replay_recovery import (
    ReplayRecovery
)


class AutomaticRejoin:

    def execute(
        self,
        peers
    ):

        handshake = RecoveryHandshake()

        states = handshake.request_cluster_state(
            peers
        )

        selector = StateSelector()

        selected = selector.select(
            states
        )

        pull = StatePull()

        remote_state = pull.pull(
            f"http://127.0.0.1:8000"
        )

        replay = ReplayRecovery()

        rebuilt = replay.rebuild(
            remote_state["ledger"]
        )

        return {
            "selected": selected,
            "rebuilt": rebuilt
        }
