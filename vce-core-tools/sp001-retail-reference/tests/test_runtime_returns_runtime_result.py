from sp001.models.case import Case
from sp001.models.objective import Objective
from sp001.runtime.runtime_result import RuntimeResult
from sp001.runtime.scientific_product_runtime import ScientificProductRuntime


def test_runtime_returns_runtime_result() -> None:
    runtime = ScientificProductRuntime()
    objective = Objective(
        objective_id="OBJ-001",
        title="Increase pink dress sell-through",
        description="Improve sell-through before Back to School.",
    )

    result = runtime.create_case(
        objective,
        case_id="CASE-001",
        scope="STORE-MX-014",
    )

    assert isinstance(result, RuntimeResult)
    assert result.success is True
    assert result.transition == "Objective->Case"
    assert isinstance(result.output, Case)
    assert result.output.case_id == "CASE-001"
    assert result.output.objective_id == "OBJ-001"
