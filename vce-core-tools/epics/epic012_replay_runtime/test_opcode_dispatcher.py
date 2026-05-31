from replay_state import ReplayState
from opcode_dispatcher import OpcodeDispatcher


state = ReplayState()
dispatcher = OpcodeDispatcher()

events = [
    {
        "lsn": 1,
        "opcode": "APPEND_EVIDENCE",
        "payload": "artifact-001"
    },
    {
        "lsn": 2,
        "opcode": "REGISTER_ARTIFACT",
        "payload": "artifact-001"
    },
    {
        "lsn": 3,
        "opcode": "SEAL_SNAPSHOT",
        "payload": "snapshot-001"
    }
]

for event in events:
    state = dispatcher.dispatch(
        state,
        event
    )

print(state.sequence_number)
print(len(state.events))
print(state.state_hash)
