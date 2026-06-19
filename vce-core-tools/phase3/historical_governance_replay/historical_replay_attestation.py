from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.historical_governance_replay.historical_governance_snapshot import (
    HistoricalGovernanceSnapshot,
)


class HistoricalReplayAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        snapshot: HistoricalGovernanceSnapshot,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="historical_governance_snapshot",
            evidence_hash=(
                snapshot.snapshot_id
            ),
        )
