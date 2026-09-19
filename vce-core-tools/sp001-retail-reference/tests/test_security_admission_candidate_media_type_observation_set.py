from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.security_admission_candidate_media_type_observation_set import (
    SecurityAdmissionCandidateMediaTypeObservationSet,
)
from tests.test_security_admission_candidate_detected_media_type_observation import (
    create_observation,
)


def create_set() -> SecurityAdmissionCandidateMediaTypeObservationSet:
    first = create_observation()
    second = replace(first, observation_id="observation-002")
    return SecurityAdmissionCandidateMediaTypeObservationSet(
        observation_set_id="observation-set-001",
        observation_set_version=1,
        candidate_identity=first.candidate_identity,
        observations=(first, second),
    )


def test_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(
        SecurityAdmissionCandidateMediaTypeObservationSet
    )) == (
        "observation_set_id",
        "observation_set_version",
        "candidate_identity",
        "observations",
    )


def test_preserves_multiple_complete_observations() -> None:
    collection = create_set()
    first, second = collection.observations
    assert first is collection.observations[0]
    assert second is collection.observations[1]
    assert first.observation_id == "observation-001"
    assert second.observation_id == "observation-002"
    assert first.verification_procedure_identity is not None
    assert second.observed_at is not None


def test_equal_reconstruction_has_value_equality() -> None:
    collection = create_set()
    assert replace(collection) == collection
    assert replace(collection) is not collection


def test_immutable_and_slotted() -> None:
    collection = create_set()
    assert not hasattr(collection, "__dict__")
    with pytest.raises(FrozenInstanceError):
        collection.observations = ()  # type: ignore[misc]


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_set_id_requires_string(value: object) -> None:
    with pytest.raises(TypeError, match="observation_set_id must be a string"):
        replace(create_set(), observation_set_id=value)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", ["", " ", "\t"])
def test_set_id_must_not_be_blank(value: str) -> None:
    with pytest.raises(ValueError, match="observation_set_id must not be blank"):
        replace(create_set(), observation_set_id=value)


@pytest.mark.parametrize("value", [None, True, False, 1.0, "1"])
def test_set_version_requires_strict_integer(value: object) -> None:
    with pytest.raises(TypeError, match="observation_set_version must be an integer"):
        replace(create_set(), observation_set_version=value)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [0, -1])
def test_set_version_must_be_positive(value: int) -> None:
    with pytest.raises(ValueError, match="observation_set_version must be positive"):
        replace(create_set(), observation_set_version=value)


def test_candidate_requires_nominal_type() -> None:
    with pytest.raises(TypeError, match="candidate_identity must be a"):
        replace(create_set(), candidate_identity=object())  # type: ignore[arg-type]


def test_observations_require_tuple() -> None:
    collection = create_set()
    with pytest.raises(TypeError, match="observations must be an immutable tuple"):
        replace(collection, observations=list(collection.observations))  # type: ignore[arg-type]


def test_observations_must_not_be_empty() -> None:
    with pytest.raises(ValueError, match="observations must not be empty"):
        replace(create_set(), observations=())


def test_observation_requires_nominal_type() -> None:
    collection = create_set()
    with pytest.raises(TypeError, match="observations must contain"):
        replace(collection, observations=(object(),))  # type: ignore[arg-type]


def test_different_candidate_is_rejected() -> None:
    collection = create_set()
    other_candidate = replace(
        collection.candidate_identity,
        candidate_version=collection.candidate_identity.candidate_version + 1,
    )
    other_observation = replace(
        collection.observations[1], candidate_identity=other_candidate
    )
    with pytest.raises(ValueError, match="set candidate_identity"):
        replace(
            collection,
            observations=(collection.observations[0], other_observation),
        )


def test_repeated_observation_identity_is_rejected() -> None:
    collection = create_set()
    repeated = replace(collection.observations[0])
    with pytest.raises(ValueError, match="duplicate observation identity"):
        replace(collection, observations=(collection.observations[0], repeated))


def test_different_versions_of_one_observation_remain_distinct() -> None:
    collection = create_set()
    first = collection.observations[0]
    newer = replace(first, observation_version=first.observation_version + 1)
    preserved = replace(collection, observations=(first, newer))
    assert preserved.observations == (first, newer)


def test_noncanonical_order_is_rejected() -> None:
    collection = create_set()
    with pytest.raises(ValueError, match="canonical identity order"):
        replace(collection, observations=tuple(reversed(collection.observations)))


def test_observation_value_participates_in_set_value() -> None:
    collection = create_set()
    changed = replace(
        collection.observations[0], detected_media_type="image/png"
    )
    assert replace(
        collection,
        observations=(changed, collection.observations[1]),
    ) != collection


def test_no_coverage_or_admission_fields() -> None:
    names = {
        field.name
        for field in fields(SecurityAdmissionCandidateMediaTypeObservationSet)
    }
    assert names.isdisjoint({
        "comparison_result",
        "coverage_status",
        "decision",
        "admitted",
        "rejected",
        "authorized",
    })
