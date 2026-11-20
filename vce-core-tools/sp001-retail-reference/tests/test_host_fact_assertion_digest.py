import hashlib
from dataclasses import replace

import pytest

from sp001.contracts.host_fact_assertion import (
    DeclaredHostFactStatus,
    HostFactAssertion,
)
from sp001.services.host_fact_assertion_digest import (
    digest_host_fact_assertion,
)
from sp001.services.host_fact_assertion_serialization import (
    canonical_host_fact_assertion_bytes,
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
        "evidence_ids": ("E1", "E2"),
    }
    values.update(overrides)
    return HostFactAssertion(**values)


def test_digest_matches_sha256_of_canonical_bytes():
    value = assertion()
    expected = hashlib.sha256(
        canonical_host_fact_assertion_bytes(value)
    ).digest()

    assert digest_host_fact_assertion(value) == expected


def test_digest_is_deterministic():
    value = assertion()
    assert digest_host_fact_assertion(value) == digest_host_fact_assertion(
        value
    )


def test_digest_is_exactly_32_bytes():
    result = digest_host_fact_assertion(assertion())
    assert type(result) is bytes
    assert len(result) == 32


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("assertion_id", "A2"),
        ("observer_id", "O2"),
        ("mandate_id", "M2"),
        ("host_id", "H2"),
        ("resource_id", "R2"),
        ("check_id", "HOST-P02"),
        ("evaluation_id", "EV2"),
        ("challenge_id", "C2"),
        ("nonce", bytes(reversed(range(32)))),
        ("observed_at", 101),
        ("policy_version", "P2"),
        ("declared_status", DeclaredHostFactStatus.FAILED),
        ("evidence_ids", ("E2", "E1")),
    ],
)
def test_each_field_changes_digest(field, replacement):
    original = assertion()
    changed = replace(original, **{field: replacement})

    assert digest_host_fact_assertion(original) != (
        digest_host_fact_assertion(changed)
    )


def test_digest_preserves_evidence_cardinality():
    empty = assertion(evidence_ids=())
    one = assertion(evidence_ids=("E1",))
    two = assertion(evidence_ids=("E1", "E2"))

    assert len(
        {
            digest_host_fact_assertion(empty),
            digest_host_fact_assertion(one),
            digest_host_fact_assertion(two),
        }
    ) == 3


def test_invalid_input_is_rejected():
    with pytest.raises(TypeError):
        digest_host_fact_assertion(None)


def test_invalid_unicode_does_not_produce_digest():
    value = assertion(assertion_id="\ud800")

    with pytest.raises(UnicodeEncodeError):
        digest_host_fact_assertion(value)


def test_digest_grants_no_authority():
    result = digest_host_fact_assertion(assertion())

    assert type(result) is bytes
    assert not hasattr(result, "authorized")
    assert not hasattr(result, "trusted")
    assert not hasattr(result, "verified")
