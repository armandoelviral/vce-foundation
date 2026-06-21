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


def test_contains_all_blocks():

    payload = build_payload()

    assert payload.decision is not None
    assert payload.evidence is not None
    assert payload.signatures is not None
    assert payload.proof is not None
    assert payload.transparency is not None


def test_serializes():

    payload = build_payload()

    data = payload.to_dict()

    assert "decision" in data
    assert "evidence" in data
    assert "signatures" in data
    assert "proof" in data
    assert "transparency" in data


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
