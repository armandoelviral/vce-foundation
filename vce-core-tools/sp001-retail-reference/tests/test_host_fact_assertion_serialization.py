from dataclasses import replace

import pytest

from sp001.contracts.host_fact_assertion import (
    DeclaredHostFactStatus,
    HOST_FACT_DOMAIN,
    HostFactAssertion,
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


def test_deterministic_encoding():
    value = assertion()
    assert (
        canonical_host_fact_assertion_bytes(value)
        == canonical_host_fact_assertion_bytes(value)
    )


def test_domain_prefix():
    encoded = canonical_host_fact_assertion_bytes(assertion())
    assert encoded.startswith(HOST_FACT_DOMAIN)


def test_all_fields_affect_encoding():
    base = assertion()
    changes = {
        "assertion_id": "A2",
        "observer_id": "O2",
        "mandate_id": "M2",
        "host_id": "H2",
        "resource_id": "R2",
        "check_id": "HOST-P02",
        "evaluation_id": "EV2",
        "challenge_id": "C2",
        "nonce": bytes(reversed(range(32))),
        "observed_at": 101,
        "policy_version": "P2",
        "declared_status": DeclaredHostFactStatus.FAILED,
        "evidence_ids": ("E2", "E1"),
    }
    original = canonical_host_fact_assertion_bytes(base)
    for field, replacement in changes.items():
        changed = replace(base, **{field: replacement})
        assert canonical_host_fact_assertion_bytes(changed) != original


def test_unicode_is_not_normalized():
    composed = assertion(assertion_id="\u00e9")
    decomposed = assertion(assertion_id="e\u0301")
    assert (
        canonical_host_fact_assertion_bytes(composed)
        != canonical_host_fact_assertion_bytes(decomposed)
    )


def test_zero_and_large_integer():
    zero = assertion(observed_at=0)
    large = assertion(observed_at=1 << 128)
    assert (
        canonical_host_fact_assertion_bytes(zero)
        != canonical_host_fact_assertion_bytes(large)
    )


def test_empty_evidence_collection():
    encoded = canonical_host_fact_assertion_bytes(
        assertion(evidence_ids=())
    )
    assert type(encoded) is bytes


def test_wrong_input_type():
    with pytest.raises(TypeError):
        canonical_host_fact_assertion_bytes(None)


def test_exact_binary_vector():
    import struct

    value = assertion(
        evidence_ids=("E1",),
        observed_at=256,
    )

    def text(value):
        encoded = value.encode("utf-8")
        return struct.pack(">I", len(encoded)) + encoded

    expected = b"".join(
        (
            HOST_FACT_DOMAIN,
            text("A1"),
            text("O1"),
            text("M1"),
            text("H1"),
            text("R1"),
            text("HOST-P01"),
            text("EV1"),
            text("C1"),
            bytes(range(32)),
            b"\x00\x00\x00\x02\x01\x00",
            text("P1"),
            text("UNKNOWN"),
            b"\x00\x00\x00\x01",
            text("E1"),
        )
    )

    assert canonical_host_fact_assertion_bytes(value) == expected


def test_field_boundaries_are_unambiguous():
    first = assertion(
        assertion_id="ab",
        observer_id="c",
    )
    second = assertion(
        assertion_id="a",
        observer_id="bc",
    )

    assert (
        canonical_host_fact_assertion_bytes(first)
        != canonical_host_fact_assertion_bytes(second)
    )


def test_evidence_cardinality_and_order():
    empty = assertion(evidence_ids=())
    one = assertion(evidence_ids=("E1",))
    two = assertion(evidence_ids=("E1", "E2"))
    reversed_two = assertion(evidence_ids=("E2", "E1"))

    encodings = {
        canonical_host_fact_assertion_bytes(value)
        for value in (empty, one, two, reversed_two)
    }

    assert len(encodings) == 4


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (0, b"\x00\x00\x00\x01\x00"),
        (255, b"\x00\x00\x00\x01\xff"),
        (256, b"\x00\x00\x00\x02\x01\x00"),
        (1 << 64, b"\x00\x00\x00\x09\x01" + b"\x00" * 8),
    ],
)
def test_integer_encoding_is_minimal(number, expected):
    from sp001.services.host_fact_assertion_serialization import (
        _nonnegative_integer,
    )

    assert _nonnegative_integer(number) == expected


def test_invalid_unicode_is_rejected():
    value = assertion(assertion_id="\ud800")

    with pytest.raises(UnicodeEncodeError):
        canonical_host_fact_assertion_bytes(value)


def test_uint32_length_overflow_is_rejected():
    from sp001.services.host_fact_assertion_serialization import _u32

    with pytest.raises(ValueError):
        _u32(1 << 32)


def test_uint32_boundary():
    from sp001.services.host_fact_assertion_serialization import _u32

    assert _u32((1 << 32) - 1) == b"\xff" * 4
