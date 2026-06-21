from dataclasses import dataclass

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


@dataclass(frozen=True)
class TcuAutonomousPayload:

    decision: TcuDecisionBlock
    evidence: TcuEvidenceBlock
    signatures: TcuSignaturesBlock
    proof: TcuProofBlock
    transparency: TcuTransparencyBlock

    def to_dict(self):

        return {
            "decision": self.decision.to_dict(),
            "evidence": self.evidence.to_dict(),
            "signatures": self.signatures.to_dict(),
            "proof": self.proof.to_dict(),
            "transparency": self.transparency.to_dict(),
        }
