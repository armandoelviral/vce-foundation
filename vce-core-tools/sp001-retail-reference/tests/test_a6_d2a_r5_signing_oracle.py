"""R5 adversarial characterization: signature is not host authenticity."""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from sp001.contracts.host_observation_authenticity import (
    HostAuthenticityStatus,
)
from sp001.contracts.isk_isolation_authority import (
    AuthorityConfigurationAssessment,
    AuthorityConfigurationStatus,
)
from sp001.services.host_fact_assertion_serialization import (
    canonical_host_fact_assertion_bytes,
)
from sp001.services.host_observation_authenticity import (
    assess_host_observation_authenticity,
)
from tests.test_host_fact_assertion import assertion


def test_valid_signature_over_executor_chosen_assertion_does_not_authenticate():
    # Adversarial assumption: executor chooses structurally valid content.
    hostile_assertion = assertion(
        observer_id="CLAIMED-OBSERVER",
        challenge_id="UNTRUSTED-CHALLENGE",
        nonce=b"\x42" * 32,
    )

    payload = canonical_host_fact_assertion_bytes(hostile_assertion)

    # Signing-oracle characterization, not an operational host signer.
    private_key = ec.generate_private_key(ec.SECP256R1())
    signature = private_key.sign(
        payload,
        ec.ECDSA(hashes.SHA256()),
    )

    # Cryptographic validity is independently demonstrable.
    private_key.public_key().verify(
        signature,
        payload,
        ec.ECDSA(hashes.SHA256()),
    )

    # Existing production authenticity gate receives no trusted
    # provenance, mandate, challenge or isolation evidence.
    structural = AuthorityConfigurationAssessment(
        status=AuthorityConfigurationStatus.CONFIGURATION_CONSISTENT,
        violations=(),
    )
    assessment = assess_host_observation_authenticity(
        structural_assessment=structural,
    )

    assert assessment.status is HostAuthenticityStatus.INDETERMINATE
    assert assessment.status is not HostAuthenticityStatus.AUTHENTICATED
