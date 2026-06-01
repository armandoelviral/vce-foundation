from epics.epic020_byzantine_fault_tolerance.adversarial_consensus import (
    AdversarialConsensusTest
)


test = AdversarialConsensusTest()

result = test.run()


print(
    result["consensus"]
)

print(
    result["faults_tolerated"]
)
