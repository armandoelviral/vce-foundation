from dataclasses import dataclass

from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)


@dataclass(frozen=True)
class SnapshotRestoreModel:

    lsn: int
    events_applied: int
    state_hash: str

    def restore(
        self,
    ) -> RuntimeState:

        return RuntimeState(
            events_applied=self.events_applied,
            last_lsn=self.lsn,
            state_hash=self.state_hash,
        )
