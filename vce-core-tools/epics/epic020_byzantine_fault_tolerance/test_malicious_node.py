from epics.epic020_byzantine_fault_tolerance.malicious_node import (
    NodeSimulator
)


sim = NodeSimulator()


honest = sim.create_vote(
    "node-A",
    "artifact123"
)


bad = sim.create_vote(
    "node-X",
    "artifact123",
    malicious=True
)


print(
    honest["behavior"]
)


print(
    bad["behavior"]
)
