from sp001.contracts.isk_isolation_experiment import IsolationExperiment
from sp001.contracts.isk_isolation_observation import IsolationObservation
from sp001.contracts.isk_isolation_preconditions import IsolationPreconditions
from sp001.contracts.isk_isolation_verdict import (
    IsolationVerdict,
    IsolationVerdictStatus,
)


def validate_isolation_consistency(
    *,
    experiment: IsolationExperiment,
    preconditions: IsolationPreconditions,
    observations: tuple[IsolationObservation, ...],
    verdict: IsolationVerdict,
) -> None:
    """Validate supplied record relations; establish no security authority."""

    if type(experiment) is not IsolationExperiment:
        raise TypeError("experiment must be an IsolationExperiment")

    if type(preconditions) is not IsolationPreconditions:
        raise TypeError("preconditions must be IsolationPreconditions")

    if type(verdict) is not IsolationVerdict:
        raise TypeError("verdict must be IsolationVerdict")

    if not isinstance(observations, tuple):
        raise TypeError("observations must be a tuple")

    experiment_id = experiment.experiment_id

    if preconditions.experiment_id != experiment_id:
        raise ValueError("preconditions experiment identity mismatch")

    if verdict.experiment_id != experiment_id:
        raise ValueError("verdict experiment identity mismatch")

    observation_ids: set[str] = set()

    for observation in observations:
        if type(observation) is not IsolationObservation:
            raise TypeError("invalid isolation observation")

        if observation.experiment_id != experiment_id:
            raise ValueError("observation experiment identity mismatch")

        if observation.attempt_id != experiment.attempt_id:
            raise ValueError("observation attempt identity mismatch")

        if observation.observation_id in observation_ids:
            raise ValueError("duplicate observation identity")

        observation_ids.add(observation.observation_id)

    referenced_ids = set(verdict.observation_ids)

    if referenced_ids != observation_ids:
        raise ValueError(
            "verdict observation references must match supplied observations"
        )

    if (
        verdict.status is IsolationVerdictStatus.NOT_TESTED
        and observations
    ):
        raise ValueError("NOT_TESTED must not have observations")
