import json

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SignedProofEnvelope:
    open_vce_payload: dict[str, Any]
    artifact_hash: str
    ledger_sequence: int
    verified: bool
    signature: str | None = None
    signing_key_id: str | None = None
    signature_algorithm: str | None = None
    signing_timestamp: str | None = None
    rekor_set: str | None = None

    def to_dict(self):

        return {
            "open_vce_payload": self.open_vce_payload,
            "artifact_hash": self.artifact_hash,
            "ledger_sequence": self.ledger_sequence,
            "verified": self.verified,
            "signature": self.signature,
            "signing_key_id": self.signing_key_id,
            "signature_algorithm": self.signature_algorithm,
            "signing_timestamp": self.signing_timestamp,
            "rekor_set": self.rekor_set,
        }

    def signing_payload(self):

        payload = self.to_dict()

        payload_without_signature = {
           key: value
           for key, value in payload.items()
           if key not in {
               "signature",
               "rekor_set",
               "signing_key_id",
               "signature_algorithm",
               "signing_timestamp",
           }
        }

        return json.dumps(
            payload_without_signature,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )


def build_unsigned_envelope(
    proof,
):

    artifact = proof["artifact"]
    receipt = proof["receipt"]

    return SignedProofEnvelope(
        open_vce_payload=artifact.to_dict(),
        artifact_hash=receipt.artifact_hash,
        ledger_sequence=receipt.ledger_sequence,
        verified=proof["verified"],
    )
