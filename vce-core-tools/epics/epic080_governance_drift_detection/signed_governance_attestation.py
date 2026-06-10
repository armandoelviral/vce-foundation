import hashlib
import json

from dataclasses import dataclass


@dataclass(frozen=True)
class SignedGovernanceAttestation:
    manifest_hash: str
    fingerprint_hash: str
    decision: str
    reason: str
    signed_by: str
    signature: str

    def to_dict(self):

        return {
            "manifest_hash": self.manifest_hash,
            "fingerprint_hash": self.fingerprint_hash,
            "decision": self.decision,
            "reason": self.reason,
            "signed_by": self.signed_by,
            "signature": self.signature,
        }


def _canonical_hash(payload):

    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha256(
        encoded
    ).hexdigest()


def create_governance_attestation(
    manifest,
    fingerprint,
    decision,
    signed_by="governance-runtime",
):

    manifest_hash = _canonical_hash(
        manifest.to_dict()
    )

    fingerprint_hash = _canonical_hash(
        fingerprint.to_dict()
    )

    unsigned_payload = {
        "manifest_hash": manifest_hash,
        "fingerprint_hash": fingerprint_hash,
        "decision": decision["allowed"],
        "reason": decision["reason"],
        "signed_by": signed_by,
    }

    signature = _canonical_hash(
        unsigned_payload
    )

    return SignedGovernanceAttestation(
        manifest_hash=manifest_hash,
        fingerprint_hash=fingerprint_hash,
        decision="ALLOW" if decision["allowed"] else "BLOCK",
        reason=decision["reason"],
        signed_by=signed_by,
        signature=signature,
    )
