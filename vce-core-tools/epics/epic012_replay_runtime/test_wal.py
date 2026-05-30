from wal_reader import read_wal
from lsn_validator import validate_lsn
from transition_validator import validate_transitions
from replay_engine import ReplayEngine

path = "epics/epic012_replay_runtime/governance.wal"

events = read_wal(path)

print(validate_lsn(events))
print(validate_transitions(events))

engine = ReplayEngine()
state = engine.replay([
    f"{event['lsn']}|{event['opcode']}|{event['payload']}"
    for event in events
])

print(state.state_hash)
