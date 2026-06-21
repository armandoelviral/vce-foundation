from dataclasses import dataclass


@dataclass(frozen=True)
class SP1Claim:

    claim_id: str
    citizen_did: str
    statement: str
    proof_digest: str

    def to_dict(self):

        return {
            "claim_id":
                self.claim_id,
            "citizen_did":
                self.citizen_did,
            "statement":
                self.statement,
            "proof_digest":
                self.proof_digest,
        }

