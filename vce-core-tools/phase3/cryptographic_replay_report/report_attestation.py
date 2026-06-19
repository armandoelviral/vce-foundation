from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.cryptographic_replay_report.cryptographic_replay_report_record import (
    CryptographicReplayReportRecord,
)


class ReportAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        report: CryptographicReplayReportRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="cryptographic_replay_report",
            evidence_hash=report.report_id,
        )
