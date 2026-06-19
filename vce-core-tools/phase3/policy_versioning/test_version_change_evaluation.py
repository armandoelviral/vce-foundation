from phase3.policy_versioning.version_change_evaluation import (
    VersionChangeEvaluation,
)


def test_higher_version_is_accepted():

    result = (
        VersionChangeEvaluation.evaluate(
            current_version="v1",
            proposed_version="v2",
        )
    )

    assert result is True


def test_same_version_is_rejected():

    result = (
        VersionChangeEvaluation.evaluate(
            current_version="v2",
            proposed_version="v2",
        )
    )

    assert result is False


def test_lower_version_is_rejected():

    result = (
        VersionChangeEvaluation.evaluate(
            current_version="v3",
            proposed_version="v2",
        )
    )

    assert result is False
