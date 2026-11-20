from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.host_fact_assertion import (
    DeclaredHostFactStatus,
    HOST_FACT_DOMAIN,
    HostFactAssertion,
)


def assertion(**overrides):
    values = {
        "assertion_id": "ASSERTION-001",
        "observer_id": "OBSERVER-001",
        "mandate_id": "MANDATE-001",
        "host_id": "HOST-001",
        "resource_id": "RESOURCE-001",
        "check_id": "HOST-P01",
        "evaluation_id": "EVALUATION-001",
        "challenge_id": "CHALLENGE-001",
        "nonce": bytes(range(32)),
        "observed_at": 100,
        "policy_version": "POLICY-001",
        "declared_status": DeclaredHostFactStatus.UNKNOWN,
        "evidence_ids": ("EVIDENCE-001",),
    }
    values.update(overrides)
    return HostFactAssertion(**values)


def test_valid_assertion_preserves_values():
    result = assertion()
    assert result.observer_id == "OBSERVER-001"
    assert result.nonce == bytes(range(32))
    assert result.declared_status is DeclaredHostFactStatus.UNKNOWN


def test_domain_constant_is_reserved():
    assert HOST_FACT_DOMAIN == b"HOST-FACT-ASSERTION-V1\x00"


def test_assertion_is_immutable():
    result = assertion()
    with pytest.raises(FrozenInstanceError):
        result.host_id = "OTHER"


@pytest.mark.parametrize(
    "field",
    (
        "assertion_id",
        "observer_id",
        "mandate_id",
        "host_id",
        "resource_id",
        "check_id",
        "evaluation_id",
        "challenge_id",
        "policy_version",
    ),
)
@pytest.mark.parametrize("invalid", ("", " ", None, 7))
def test_invalid_identifier_is_rejected(field, invalid):
    with pytest.raises(ValueError):
        assertion(**{field: invalid})


@pytest.mark.parametrize(
    "invalid",
    ("HOST-P00", "HOST-P11", "OTHER"),
)
def test_unknown_check_is_rejected(invalid):
    with pytest.raises(ValueError):
        assertion(check_id=invalid)


def test_all_host_checks_are_accepted():
    for i in range(1, 11):
        check_id = f"HOST-P{i:02d}"
        assert assertion(check_id=check_id).check_id == check_id


@pytest.mark.parametrize(
    "invalid",
    (None, "", bytearray(32), 7),
)
def test_invalid_nonce_type_is_rejected(invalid):
    with pytest.raises(TypeError):
        assertion(nonce=invalid)


@pytest.mark.parametrize(
    "invalid",
    (b"", bytes(31), bytes(33)),
)
def test_invalid_nonce_length_is_rejected(invalid):
    with pytest.raises(ValueError):
        assertion(nonce=invalid)


@pytest.mark.parametrize(
    "invalid",
    (None, True, False, 1.5, "100"),
)
def test_invalid_observation_time_type_is_rejected(invalid):
    with pytest.raises(TypeError):
        assertion(observed_at=invalid)


def test_negative_observation_time_is_rejected():
    with pytest.raises(ValueError):
        assertion(observed_at=-1)


@pytest.mark.parametrize(
    "status",
    tuple(DeclaredHostFactStatus),
)
def test_all_declared_statuses_are_accepted(status):
    assert assertion(declared_status=status).declared_status is status


@pytest.mark.parametrize(
    "invalid",
    ("SATISFIED", None, True, 1),
)
def test_untyped_status_is_rejected(invalid):
    with pytest.raises(TypeError):
        assertion(declared_status=invalid)


@pytest.mark.parametrize(
    "invalid",
    (None, [], "EVIDENCE-001"),
)
def test_invalid_evidence_collection_is_rejected(invalid):
    with pytest.raises(TypeError):
        assertion(evidence_ids=invalid)


@pytest.mark.parametrize(
    "invalid",
    ("", " ", None, 7),
)
def test_invalid_evidence_id_is_rejected(invalid):
    with pytest.raises(ValueError):
        assertion(evidence_ids=(invalid,))


def test_duplicate_evidence_is_rejected():
    with pytest.raises(ValueError):
        assertion(evidence_ids=("E1", "E1"))


def test_empty_evidence_collection_is_structurally_valid():
    assert assertion(evidence_ids=()).evidence_ids == ()


def test_no_authority_attributes_are_created():
    result = assertion(
        declared_status=DeclaredHostFactStatus.SATISFIED
    )
    for field in (
        "trusted",
        "authorized",
        "verified",
        "eligible",
    ):
        assert not hasattr(result, field)


def test_replacement_preserves_validation():
    with pytest.raises(ValueError):
        replace(assertion(), host_id="")
