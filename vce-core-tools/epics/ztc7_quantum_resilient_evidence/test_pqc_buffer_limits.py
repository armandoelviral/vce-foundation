from epics.ztc7_quantum_resilient_evidence.pqc_buffer_limits import (
    PQCBufferLimits,
)


def test_accepts_signature_within_limit():

    assert PQCBufferLimits.allow(
        signature_size_bytes=2400,
    )


def test_accepts_signature_at_limit():

    assert PQCBufferLimits.allow(
        signature_size_bytes=65536,
    )


def test_rejects_signature_over_limit():

    assert not PQCBufferLimits.allow(
        signature_size_bytes=65537,
    )
