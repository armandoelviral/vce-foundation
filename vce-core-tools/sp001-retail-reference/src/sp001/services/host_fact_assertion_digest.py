"""SHA-256 content identity for an unverified host assertion."""

import hashlib

from sp001.contracts.host_fact_assertion import HostFactAssertion
from sp001.services.host_fact_assertion_serialization import (
    canonical_host_fact_assertion_bytes,
)


def digest_host_fact_assertion(
    assertion: HostFactAssertion,
) -> bytes:
    """Digest canonical content without authenticity or authority claims."""

    canonical_bytes = canonical_host_fact_assertion_bytes(assertion)
    return hashlib.sha256(canonical_bytes).digest()
