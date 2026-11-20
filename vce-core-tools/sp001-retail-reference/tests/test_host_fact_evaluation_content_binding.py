from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.host_fact_assertion import (
    DeclaredHostFactStatus,
    HostFactAssertion,
)
from sp001.contracts.host_fact_evaluation import (
    DeclaredFindingOutcome,
    HostFactEvaluation,
    HostFactFinding,
)
from sp001.contracts.host_fact_evaluation_content_binding import (
    HostFactEvaluationContentBinding,
)
from sp001.services.host_fact_assertion_digest import (
    digest_host_fact_assertion,
)
from sp001.services.host_fact_evaluation_content_binding import (
    verify_host_fact_evaluation_content_binding,
)


def assertion(**overrides):
    values = {
        "assertion_id": "A1",
        "observer_id": "O1",
        "mandate_id": "M1",
        "host_id": "H1",
        "resource_id": "R1",
        "check_id": "HOST-P01",
        "evaluation_id": "EV1",
        "challenge_id": "C1",
        "nonce": bytes(range(32)),
        "observed_at": 100,
        "policy_version": "P1",
        "declared_status": DeclaredHostFactStatus.UNKNOWN,
        "evidence_ids": ("E1",),
    }
    values.update(overrides)
    return HostFactAssertion(**values)


def evaluation(outcome=DeclaredFindingOutcome.PASS, **overrides):
    values = {
        "evaluation_record_id": "ER1",
        "assertion_id": "A1",
        "evaluation_id": "EV1",
        "evaluator_id": "EVALUATOR1",
        "evaluated_at": 101,
        "policy_version": "P1",
        "findings": (
            HostFactFinding(
                check_code="ASSERTION_STRUCTURE",
                outcome=outcome,
                evidence_ids=(),
            ),
        ),
    }
    values.update(overrides)
    return HostFactEvaluation(**values)


def binding(value=None, **overrides):
    if value is None:
        value = assertion()
    values = {
        "evaluation_record_id": "ER1",
        "assertion_id": value.assertion_id,
        "assertion_digest": digest_host_fact_assertion(value),
    }
    values.update(overrides)
    return HostFactEvaluationContentBinding(**values)


def verify(b=None, a=None, e=None):
    return verify_host_fact_evaluation_content_binding(
        binding() if b is None else b,
        assertion() if a is None else a,
        evaluation() if e is None else e,
    )


def test_matching_content_and_identifiers():
    assert verify() is True


def test_same_assertion_id_with_different_content():
    assert verify(a=assertion(observer_id="O2")) is False

def test_coordinated_assertion_and_binding_replacement_is_content_consistent():
    original = assertion()
    original_binding = binding(original)
    original_evaluation = evaluation()

    assert verify(
        b=original_binding,
        a=original,
        e=original_evaluation,
    ) is True

    substituted = assertion(
        observer_id="ATTACKER-CLAIMED-OBSERVER",
        declared_status=DeclaredHostFactStatus.SATISFIED,
    )

    assert substituted.assertion_id == original.assertion_id

    assert (
        digest_host_fact_assertion(substituted)
        != digest_host_fact_assertion(original)
    )

    # An isolated modification is detected.
    assert verify(
        b=original_binding,
        a=substituted,
        e=original_evaluation,
    ) is False

    # The adversary also replaces the untrusted content reference.
    substituted_binding = binding(substituted)

    # This verifies correspondence, not observer authenticity.
    assert verify(
        b=substituted_binding,
        a=substituted,
        e=original_evaluation,
    ) is True

def test_different_evaluation_record_id():
    assert verify(e=evaluation(evaluation_record_id="ER2")) is False


def test_different_evaluation_id():
    assert verify(e=evaluation(evaluation_id="EV2")) is False


def test_different_policy_version():
    assert verify(e=evaluation(policy_version="P2")) is False


def test_different_binding_assertion_id():
    assert verify(b=binding(assertion_id="A2")) is False


def test_different_evaluation_assertion_id():
    assert verify(e=evaluation(assertion_id="A2")) is False


def test_modified_digest_byte():
    original = binding()
    altered = bytes([original.assertion_digest[0] ^ 1])
    altered += original.assertion_digest[1:]

    assert verify(
        b=replace(original, assertion_digest=altered)
    ) is False


@pytest.mark.parametrize("length", [0, 31, 33])
def test_invalid_digest_length_rejected(length):
    with pytest.raises(ValueError):
        binding(assertion_digest=bytes(length))


@pytest.mark.parametrize("value", [None, "x", bytearray(32)])
def test_invalid_digest_type_rejected(value):
    with pytest.raises(TypeError):
        binding(assertion_digest=value)


@pytest.mark.parametrize(
    "field",
    ["evaluation_record_id", "assertion_id"],
)
@pytest.mark.parametrize("value", ["", "  ", None, 7])
def test_invalid_identifiers_rejected(field, value):
    with pytest.raises(ValueError):
        binding(**{field: value})


def test_binding_is_immutable():
    value = binding()
    with pytest.raises(FrozenInstanceError):
        value.assertion_id = "A2"


def test_pass_finding_does_not_override_digest_mismatch():
    assert verify(
        a=assertion(observer_id="O2"),
        e=evaluation(DeclaredFindingOutcome.PASS),
    ) is False


def test_fail_finding_does_not_prevent_content_match():
    assert verify(
        e=evaluation(DeclaredFindingOutcome.FAIL)
    ) is True


def test_unknown_finding_does_not_prevent_content_match():
    assert verify(
        e=evaluation(DeclaredFindingOutcome.UNKNOWN)
    ) is True


def test_unserializable_assertion_raises():
    with pytest.raises(UnicodeEncodeError):
        verify(a=assertion(observer_id="\ud800"))


@pytest.mark.parametrize(
    ("argument", "replacement"),
    [
        ("binding", None),
        ("assertion", None),
        ("evaluation", None),
    ],
)
def test_invalid_object_types_raise(argument, replacement):
    arguments = {
        "binding": binding(),
        "assertion": assertion(),
        "evaluation": evaluation(),
    }
    arguments[argument] = replacement

    with pytest.raises(TypeError):
        verify_host_fact_evaluation_content_binding(**arguments)


def test_no_authority_returned():
    result = verify()
    assert type(result) is bool
