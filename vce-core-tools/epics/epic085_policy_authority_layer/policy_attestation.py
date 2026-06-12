import hashlib
import json

from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyAttestation:
    policy_id: str
    policy_version: str
    policy_hash: str
    approval_status: str
    attested_by: str
    signature: str

    def to_dict(self):

        return {
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "policy_hash": self.policy_hash,
            "approval_status": self.approval_status,
            "attested_by": self.attested_by,
            "signature": self.signature,
        }


def _canonical_hash(
    payload,
):

    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha256(
        encoded
    ).hexdigest()


def create_policy_attestation(
    policy,
    approval,
    attested_by="policy-authority",
):

    unsigned_payload = {
        "policy_id": policy.policy_id,
        "policy_version": policy.policy_version,
        "policy_hash": policy.policy_hash,
        "approval_status": approval.approval_status,
        "attested_by": attested_by,
    }

    signature = _canonical_hash(
        unsigned_payload
    )

    return PolicyAttestation(
        policy_id=policy.policy_id,
        policy_version=policy.policy_version,
        policy_hash=policy.policy_hash,
        approval_status=approval.approval_status,
        attested_by=attested_by,
        signature=signature,
    )
