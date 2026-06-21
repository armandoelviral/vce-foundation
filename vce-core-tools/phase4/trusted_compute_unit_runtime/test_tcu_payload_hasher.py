from phase4.trusted_compute_unit_runtime.tcu_payload_hasher import (
    TcuPayloadHasher,
)

from phase4.trusted_compute_unit_runtime.tcu_autonomous_payload import (
    TcuAutonomousPayload,
)

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


def test_generates_hash():

    payload = build_payload()

    result = TcuPayloadHasher.hash_payload(payload)

    assert isinstance(result, str)
    assert len(result) == 64


def test_same_payload_same_hash():

    payload = build_payload()

    h1 = TcuPayloadHasher.hash_payload(payload)
    h2 = TcuPayloadHasher.hash_payload(payload)

    assert h1 == h2


def build_payload():

    return TcuAutonomousPayload(
        decision=TcuDecisionBlock(
            verdict="APPROVED",
            execution_status="SUCCESS",
            compute_gas_used=1,
            system_state_root="root",
        ),
        evidence=TcuEvidenceBlock(
            artifact_hash="artifact",
            facts_hash="facts",
            input_commitment="input",
            purified_time_utc="2026",
        ),
        signatures=TcuSignaturesBlock(
            classical_ed25519="ed25519",
            post_quantum_mldsa65="mldsa",
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
            merkle_inclusion_proof=["a"],
        ),
    )
