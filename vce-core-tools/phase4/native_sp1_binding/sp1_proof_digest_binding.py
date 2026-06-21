from dataclasses import dataclass


@dataclass(frozen=True)
class SP1ProofDigestBinding:

    tcu_did: str
    proof_digest: str

    def to_dict(self):

        return {
            "tcu_did": self.tcu_did,
            "proof_digest": self.proof_digest,
        }
