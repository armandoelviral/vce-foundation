import json
from typing import NoReturn

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)


StoredIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent
)
_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
    "MERKLE-CHECKPOINT-PUBLICATION-INTENT"
)
_TOP_LEVEL_KEYS = frozenset(
    (
        "checkpoint_serialization",
        "domain",
        "public_key_encoding",
        "public_key_fingerprint",
        "publication_id",
        "signature_encoding",
        "signature_hex",
        "signing_algorithm",
        "signing_key_id",
        "storage_schema_version",
    )
)
_LOWER_HEX = frozenset("0123456789abcdef")


def parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
    *,
    serialization: str,
) -> StoredIntent:
    """Parse one strict canonical portable signed publication intent."""

    if type(serialization) is not str:
        raise TypeError(
            "serialization must be a string"
        )
    if not serialization:
        raise ValueError(
            "serialization must not be empty"
        )

    try:
        document = json.loads(
            serialization,
            object_pairs_hook=_strict_json_object,
            parse_constant=_reject_json_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError(
            "serialization must contain valid JSON"
        ) from error

    if not isinstance(document, dict):
        raise ValueError(
            "serialization must contain a JSON object"
        )

    if frozenset(document) != _TOP_LEVEL_KEYS:
        raise ValueError(
            "stored publication intent must contain "
            "exactly the supported keys"
        )

    if document["domain"] != _DOMAIN:
        raise ValueError(
            "stored publication intent domain is not supported"
        )

    stored_intent = StoredIntent(
        storage_schema_version=(
            document["storage_schema_version"]
        ),
        publication_id=document["publication_id"],
        checkpoint_serialization=(
            document["checkpoint_serialization"]
        ),
        signing_key_id=document["signing_key_id"],
        signing_algorithm=(
            document["signing_algorithm"]
        ),
        public_key_encoding=(
            document["public_key_encoding"]
        ),
        public_key_fingerprint=(
            document["public_key_fingerprint"]
        ),
        signature_encoding=(
            document["signature_encoding"]
        ),
        signature=_decode_signature_hex(
            document["signature_hex"]
        ),
    )

    canonical = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            stored_intent=stored_intent,
        )
    )
    if canonical != serialization:
        raise ValueError(
            "serialization must be canonical"
        )

    return stored_intent


def _strict_json_object(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    document: dict[str, object] = {}

    for key, value in pairs:
        if key in document:
            raise ValueError(
                "serialization must not contain duplicate keys"
            )
        document[key] = value

    return document


def _reject_json_constant(
    value: str,
) -> NoReturn:
    raise ValueError(
        "serialization must not contain non-finite values"
    )


def _decode_signature_hex(
    value: object,
) -> bytes:
    if type(value) is not str:
        raise TypeError(
            "signature_hex must be a string"
        )
    if not value:
        raise ValueError(
            "signature_hex must not be empty"
        )
    if (
        not value.isascii()
        or len(value) % 2 != 0
        or any(
            character not in _LOWER_HEX
            for character in value
        )
    ):
        raise ValueError(
            "signature_hex must use canonical lowercase hexadecimal"
        )

    return bytes.fromhex(value)
