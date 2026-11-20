"""Canonical byte encoding of an unverified host assertion."""

import struct

from sp001.contracts.host_fact_assertion import (
    HOST_FACT_DOMAIN,
    HostFactAssertion,
)

_MAX_U32 = (1 << 32) - 1


def _u32(value: int) -> bytes:
    if value > _MAX_U32:
        raise ValueError("length exceeds uint32")
    return struct.pack(">I", value)


def _text(value: str) -> bytes:
    encoded = value.encode("utf-8", errors="strict")
    return _u32(len(encoded)) + encoded


def _nonnegative_integer(value: int) -> bytes:
    if value == 0:
        encoded = b"\x00"
    else:
        encoded = value.to_bytes(
            (value.bit_length() + 7) // 8,
            byteorder="big",
        )
    return _u32(len(encoded)) + encoded


def canonical_host_fact_assertion_bytes(
    assertion: HostFactAssertion,
) -> bytes:
    """Encode content identity; does not establish trust."""

    if type(assertion) is not HostFactAssertion:
        raise TypeError("assertion must be HostFactAssertion")

    parts = [HOST_FACT_DOMAIN]

    for value in (
        assertion.assertion_id,
        assertion.observer_id,
        assertion.mandate_id,
        assertion.host_id,
        assertion.resource_id,
        assertion.check_id,
        assertion.evaluation_id,
        assertion.challenge_id,
    ):
        parts.append(_text(value))

    parts.append(assertion.nonce)
    parts.append(_nonnegative_integer(assertion.observed_at))
    parts.append(_text(assertion.policy_version))
    parts.append(_text(assertion.declared_status.value))

    parts.append(_u32(len(assertion.evidence_ids)))

    for evidence_id in assertion.evidence_ids:
        parts.append(_text(evidence_id))

    return b"".join(parts)
