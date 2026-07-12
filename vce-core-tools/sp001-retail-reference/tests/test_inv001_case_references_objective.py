from sp001.models.objective import Objective


def test_case_preserves_objective_identity() -> None:

    objective = Objective(
        objective_id="OBJ-001",
        title="Back to School",
        description="..."
    )

    case = objective.create_case(
        case_id="CASE-001",
        scope="STORE-MX-014",
    )

    assert case.objective_id == objective.objective_id
