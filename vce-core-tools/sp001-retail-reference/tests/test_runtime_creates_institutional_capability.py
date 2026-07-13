from sp001.models.governance_decision import GovernanceDecision
from sp001.runtime.scientific_product_runtime import ScientificProductRuntime


def test_runtime_creates_institutional_capability_from_governance() -> None:
    runtime = ScientificProductRuntime()
    decision = GovernanceDecision()

    capability = runtime.create_institutional_capability(decision)

    assert capability is not None
