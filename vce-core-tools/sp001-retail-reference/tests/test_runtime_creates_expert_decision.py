from sp001.models.recommendation import Recommendation
from sp001.runtime.scientific_product_runtime import ScientificProductRuntime


def test_runtime_creates_expert_decision_from_recommendation() -> None:
    runtime = ScientificProductRuntime()
    recommendation = Recommendation()

    decision = runtime.create_expert_decision(recommendation)

    assert decision is not None
