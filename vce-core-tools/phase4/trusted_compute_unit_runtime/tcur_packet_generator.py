from phase4.trusted_compute_unit_runtime.tcu_decision_block import (
    TcuDecisionBlock,
)

from phase4.trusted_compute_unit_runtime.tcu_evidence_block import (
    TcuEvidenceBlock,
)

from phase4.trusted_compute_unit_runtime.tcu_signatures_block import (
    TcuSignaturesBlock,
)

from phase4.trusted_compute_unit_runtime.tcu_proof_block import (
    TcuProofBlock,
)

from phase4.trusted_compute_unit_runtime.tcu_transparency_block import (
    TcuTransparencyBlock,
)

from phase4.trusted_compute_unit_runtime.tcu_autonomous_payload import (
    TcuAutonomousPayload,
)

from phase4.trusted_compute_unit_runtime.tcu_payload_hasher import (
    TcuPayloadHasher,
)


class TcurPacketGenerator:

    @staticmethod
    def generate():

        payload = TcuAutonomousPayload(
            decision=TcuDecisionBlock(
                verdict="APPROVED",
                execution_status="SUCCESS",
                compute_gas_used=42100,
                system_state_root="state-root",
            ),
            evidence=TcuEvidenceBlock(
                artifact_hash="artifact",
                facts_hash="facts",
                input_commitment="input",
                purified_time_utc="2026-06-21T00:00:00Z",
            ),
            signatures=TcuSignaturesBlock(
                classical_ed25519="ed25519",
                post_quantum_mldsa65="mldsa65",
            ),
            proof=TcuProofBlock(
                proof_backend="SP1",
                proof_status="VERIFIED",
                verification_key="vk",
                proof_hash="proof",
            ),
            transparency=TcuTransparencyBlock(
                ledger_index=1,
                parent_block_hash="parent",
                merkle_root="root",
                merkle_inclusion_proof=["node"],
            ),
        )

        packet = payload.to_dict()

        packet["payload_hash"] = (
            TcuPayloadHasher.hash_payload(payload)
        )

        return packet
