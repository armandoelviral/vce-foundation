from dataclasses import dataclass

from phase3.historical_replay_auditor.replay_audit_decision import (
    ReplayAuditDecision,
)


@dataclass(frozen=True)
class ReplayCertification:

    status: str
    certified: bool

    @staticmethod
    def certify(
        decision: ReplayAuditDecision,
    ):

        return ReplayCertification(
            status=decision.status,
            certified=(
                decision.status == "PASS"
            ),
        )
