import datetime

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID

from epics.epic076_sigstore_compatibility_layer.real_certificate_parser import (
    RealCertificateParser,
)


def generate_mock_ephemeral_cert(
    identity_uri: str,
    valid_minutes=10,
    context_shift_seconds=0,
) -> str:

    ca_private_key = ec.generate_private_key(
        ec.SECP256R1()
    )

    ca_subject = x509.Name(
        [
            x509.NameAttribute(
                NameOID.COMMON_NAME,
                "Veracity Runtime Mock Root CA",
            ),
            x509.NameAttribute(
                NameOID.ORGANIZATION_NAME,
                "VCE Institute Testing Group",
            ),
        ]
    )

    user_private_key = ec.generate_private_key(
        ec.SECP256R1()
    )

    base_time = datetime.datetime.now(
        datetime.timezone.utc
    )

    not_valid_before = base_time + datetime.timedelta(
        seconds=context_shift_seconds
    )

    not_valid_after = not_valid_before + datetime.timedelta(
        minutes=valid_minutes
    )

    subject = x509.Name(
        [
            x509.NameAttribute(
                NameOID.COMMON_NAME,
                "VCE Ephemeral Session Signer",
            )
        ]
    )

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_subject)
        .public_key(user_private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(
            not_valid_before.replace(tzinfo=None)
        )
        .not_valid_after(
            not_valid_after.replace(tzinfo=None)
        )
        .add_extension(
            x509.SubjectAlternativeName(
                [
                    x509.UniformResourceIdentifier(
                        identity_uri
                    )
                ]
            ),
            critical=False,
        )
        .sign(
            ca_private_key,
            hashes.SHA256(),
        )
    )

    return cert.public_bytes(
        serialization.Encoding.PEM
    ).decode("utf-8")


def test_parser_accepts_valid_local_mock_token():

    parser = RealCertificateParser()

    target_identity = "urn:vce:actor:saas-deployment-runner"

    cert_pem = generate_mock_ephemeral_cert(
        identity_uri=target_identity
    )

    report = parser.verify_and_parse_fulcio_cert(
        cert_pem,
        target_identity,
    )

    assert report["status"] == "CERTIFICATE_VALIDATED_SUCCESSFULLY"
    assert target_identity in report["subject_san_identities"]
    assert report["key_algorithm"] == "ECDSA (secp256r1)"


def test_parser_intercepts_identity_mismatch_attacks():

    parser = RealCertificateParser()

    legitimate_identity = "urn:vce:actor:authorized-fintech-node"
    attacker_identity = "urn:vce:actor:malicious-tampered-node"

    cert_pem = generate_mock_ephemeral_cert(
        identity_uri=attacker_identity
    )

    report = parser.verify_and_parse_fulcio_cert(
        cert_pem,
        legitimate_identity,
    )

    assert report["status"] == "REJECTED_CERTIFICATE"
    assert report["error_code"] == "OIDC_IDENTITY_MISMATCH"


def test_parser_intercepts_expired_ephemeral_bounds():

    parser = RealCertificateParser()

    target_identity = "urn:vce:actor:healthtech-clinical-inference"

    cert_pem = generate_mock_ephemeral_cert(
        identity_uri=target_identity,
        valid_minutes=5,
        context_shift_seconds=-1500,
    )

    report = parser.verify_and_parse_fulcio_cert(
        cert_pem,
        target_identity,
    )

    assert report["status"] == "REJECTED_CERTIFICATE"
    assert (
        report["error_code"]
        == "CERTIFICATE_EXPIRED_OR_NOT_YET_VALID"
    )
