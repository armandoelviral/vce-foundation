from phase3.historical_replay_auditor.replay_audit_decision import (
    ReplayAuditDecision,
)

from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)


class CertificateIssuer:

    @staticmethod
    def issue(
        certificate_id: str,
        replay_id: str,
        decision: ReplayAuditDecision,
    ) -> ReplayCertificateRecord:

        return ReplayCertificateRecord(
            certificate_id=certificate_id,
            replay_id=replay_id,
            status=decision.status,
        )
