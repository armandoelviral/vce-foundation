from replay_engine import ReplayEngine

engine = ReplayEngine()

events = [
    "AppendEvidence",
    "SealSnapshot",
    "RegisterArtifact"
]

run_a = engine.replay(
    events
)

run_b = engine.replay(
    events
)

print(
    run_a.state_hash
)

print(
    run_b.state_hash
)

print(
    run_a.state_hash ==
    run_b.state_hash
)
