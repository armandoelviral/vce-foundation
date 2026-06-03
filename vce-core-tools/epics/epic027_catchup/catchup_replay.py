from epics.epic026_recovery.replay_recovery import (
    ReplayRecovery
)

from epics.epic027_catchup.ledger_apply import (
    LedgerApply
)


class CatchupReplay:

    def execute(
        self,
        canonical_ledger
    ):

        apply = LedgerApply()

        apply.apply(
            canonical_ledger
        )

        replay = ReplayRecovery()

        rebuilt_state = replay.rebuild(
            apply.current()
        )

        return {
            "ledger_size": len(
                apply.current()
            ),
            "rebuilt_state": rebuilt_state
        }
