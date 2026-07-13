from sp001.models.expert_decision import ExpertDecision
from sp001.runtime.scientific_product_runtime import ScientificProductRuntime


def test_runtime_records_operational_evidence_from_expert_decision() -> None:
    runtime = ScientificProductRuntime()
    decision = ExpertDecision()

    evidence = runtime.record_operational_evidence(decision)

    assert evidence is not None
