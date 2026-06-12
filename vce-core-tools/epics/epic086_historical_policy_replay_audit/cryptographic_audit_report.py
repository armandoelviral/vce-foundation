from dataclasses import dataclass


@dataclass(frozen=True)
class CryptographicAuditReport:
    evidence_hash: str
    policy_id: str
    policy_version: str
    replay_result: str
    original_decision: str
    replay_decision: str
    verified: bool

    def to_dict(self):

        return {
            "evidence_hash": self.evidence_hash,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "replay_result": self.replay_result,
            "original_decision": self.original_decision,
            "replay_decision": self.replay_decision,
            "verified": self.verified,
        }


def build_audit_report(
    evidence,
    comparison,
):

    return CryptographicAuditReport(
        evidence_hash=evidence["evidence_hash"],
        policy_id=evidence["policy_id"],
        policy_version=evidence["policy_version"],
        replay_result=comparison["result"],
        original_decision=comparison["original_decision"],
        replay_decision=comparison["replay_decision"],
        verified=comparison["result"] == "REPLAY_MATCH",
    )
