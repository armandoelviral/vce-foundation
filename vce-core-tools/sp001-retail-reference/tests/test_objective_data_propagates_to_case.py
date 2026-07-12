from sp001.models.objective import Objective


def test_objective_data_propagates_to_case() -> None:
    objective = Objective(
        objective_id="OBJ-001",
        title="Increase pink dress sell-through",
        description="Improve sell-through before Back to School.",
    )

    case = objective.create_case(
        case_id="CASE-001",
        scope="STORE-MX-014",
    )

    assert case.case_id == "CASE-001"
    assert case.objective_id == "OBJ-001"
    assert case.objective_title == "Increase pink dress sell-through"
    assert case.scope == "STORE-MX-014"
