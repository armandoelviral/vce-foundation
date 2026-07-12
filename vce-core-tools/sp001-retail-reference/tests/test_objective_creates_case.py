from sp001.models.case import Case
from sp001.models.objective import Objective


def test_objective_creates_case():

    objective = Objective()

    case = objective.create_case()

    assert isinstance(case, Case)
