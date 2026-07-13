from sp001.models.operational_evidence import OperationalEvidence
from sp001.runtime.scientific_product_runtime import ScientificProductRuntime


def test_runtime_creates_capability_candidate_from_evidence() -> None:
    runtime = ScientificProductRuntime()
    evidence = OperationalEvidence()

    candidate = runtime.create_capability_candidate(evidence)

    assert candidate is not None
