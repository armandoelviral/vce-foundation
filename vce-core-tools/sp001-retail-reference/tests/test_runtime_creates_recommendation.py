from sp001.models.case import Case
from sp001.runtime.scientific_product_runtime import ScientificProductRuntime


def test_runtime_creates_recommendation_from_case() -> None:
    runtime = ScientificProductRuntime()
    case = Case(
        case_id="CASE-001",
        objective_id="OBJ-001",
        objective_title="Increase pink dress sell-through",
        scope="STORE-MX-014",
    )

    recommendation = runtime.create_recommendation(case)

    assert recommendation is not None
