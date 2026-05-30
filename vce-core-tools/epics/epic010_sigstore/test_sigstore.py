from rekor_validator import RekorValidator
from fulcio_validator import FulcioValidator

rekor = RekorValidator()
fulcio = FulcioValidator()

valid_rekor = {
    "uuid": {
        "verification": {
            "signedEntryTimestamp": "0xSET"
        }
    }
}

invalid_rekor = {
    "uuid": {
        "verification": {
            "signedEntryTimestamp": ""
        }
    }
}

valid_cert = """
-----BEGIN CERTIFICATE-----
Subject: CN=urn:vce:actor:fintech-runner
-----END CERTIFICATE-----
"""

print(
    rekor.verify_inclusion_proof(
        valid_rekor
    )
)

print(
    rekor.verify_inclusion_proof(
        invalid_rekor
    )
)

print(
    fulcio.verify_ephemeral_certificate(
        valid_cert,
        "urn:vce:actor:fintech-runner"
    )
)

print(
    fulcio.verify_ephemeral_certificate(
        valid_cert,
        "urn:vce:actor:malicious-node"
    )
)
