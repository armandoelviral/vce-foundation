from epics.epic088_replay_provenance_certificate.certificate_builder import (
    CertificateBuilder,
)

from epics.epic088_replay_provenance_certificate.certificate_hash import (
    CertificateHash,
)

from epics.epic088_replay_provenance_certificate.certificate_signature import (
    CertificateSignature,
)

from epics.epic088_replay_provenance_certificate.certificate_verifier import (
    CertificateVerifier,
)

from epics.epic088_replay_provenance_certificate.replay_provenance_attestation import (
    ReplayProvenanceAttestation,
)


def test_end_to_end_replay_certificate_flow():

    certificate = CertificateBuilder.build(
        replay_id="replay-001",
        request_hash="request-001",
        result_hash="result-001",
        environment_hash="env-001",
        comparator_hash="cmp-001",
    )

    certificate_hash = CertificateHash.compute(
        certificate
    )

    signature = CertificateSignature.sign(
        certificate_hash
    )

    verified = CertificateVerifier.verify(
        certificate_hash,
        signature,
    )

    attestation = ReplayProvenanceAttestation(
        replay_id=certificate.replay_id,
        certificate_hash=certificate_hash,
        certificate_signature=signature,
        verified=verified,
    )

    assert attestation.verified is True
