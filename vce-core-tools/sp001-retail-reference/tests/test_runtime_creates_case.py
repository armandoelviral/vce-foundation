from sp001.models.objective import Objective
from sp001.runtime.scientific_product_runtime import ScientificProductRuntime


def test_runtime_creates_case_preserving_objective_identity() -> None:
    runtime = ScientificProductRuntime()
    objective = Objective(
        objective_id="OBJ-001",
        title="Increase pink dress sell-through",
        description="Improve sell-through before Back to School.",
    )

    case = runtime.create_case(
        objective,
        case_id="CASE-001",
        scope="STORE-MX-014",
    )

    assert case.case_id == "CASE-001"
    assert case.objective_id == "OBJ-001"
    assert case.objective_title == "Increase pink dress sell-through"
    assert case.scope == "STORE-MX-014"
