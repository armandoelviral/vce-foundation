from sp001.models.capability_candidate import CapabilityCandidate
from sp001.runtime.scientific_product_runtime import ScientificProductRuntime


def test_runtime_creates_governance_decision_from_candidate() -> None:
    runtime = ScientificProductRuntime()
    candidate = CapabilityCandidate()

    decision = runtime.create_governance_decision(candidate)

    assert decision is not None
