from sp001.models.case import Case
from sp001.models.recommendation import Recommendation


def test_case_creates_recommendation() -> None:
    case = Case()

    recommendation = case.create_recommendation()

    assert isinstance(recommendation, Recommendation)
