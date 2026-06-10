import datetime

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import ExtensionOID


class RealCertificateParser:

    def verify_and_parse_fulcio_cert(
        self,
        cert_pem: str,
        expected_identity: str,
    ):

        cert = x509.load_pem_x509_certificate(
            cert_pem.encode("utf-8")
        )

        now = datetime.datetime.now(
            datetime.timezone.utc
        )

        if (
            cert.not_valid_before_utc > now
            or cert.not_valid_after_utc < now
        ):
            return {
                "status": "REJECTED_CERTIFICATE",
                "error_code": "CERTIFICATE_EXPIRED_OR_NOT_YET_VALID",
            }

        san = cert.extensions.get_extension_for_oid(
            ExtensionOID.SUBJECT_ALTERNATIVE_NAME
        ).value

        identities = san.get_values_for_type(
            x509.UniformResourceIdentifier
        )

        if expected_identity not in identities:
            return {
                "status": "REJECTED_CERTIFICATE",
                "error_code": "OIDC_IDENTITY_MISMATCH",
                "subject_san_identities": identities,
            }

        public_key = cert.public_key()

        if isinstance(public_key, ec.EllipticCurvePublicKey):
            key_algorithm = "ECDSA (secp256r1)"
        else:
            key_algorithm = "UNKNOWN"

        return {
            "status": "CERTIFICATE_VALIDATED_SUCCESSFULLY",
            "subject_san_identities": identities,
            "key_algorithm": key_algorithm,
        }
