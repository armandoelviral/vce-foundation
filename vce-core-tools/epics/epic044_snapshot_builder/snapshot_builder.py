from epics.epic040_deterministic_replay.replay_engine import ReplayEngine
from epics.epic042_state_hashing.state_hasher import StateHasher
from epics.epic043_snapshot_object.snapshot import Snapshot


class SnapshotBuilder:

    def __init__(self):
        self.replay_engine = ReplayEngine()
        self.state_hasher = StateHasher()

    def build(self, events):
        state = self.replay_engine.replay(events)
        state_hash = self.state_hasher.hash(state)

        return Snapshot(
            sequence=state.last_sequence,
            state_hash=state_hash,
        )
