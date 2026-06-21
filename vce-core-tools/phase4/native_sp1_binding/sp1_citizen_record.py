from dataclasses import dataclass


@dataclass(frozen=True)
class SP1CitizenRecord:

    tcu_did: str
    program_id: str
    verification_key: str
    proof_digest: str
    public_values: dict

    def to_dict(self):

        return {
            "tcu_did":
                self.tcu_did,
            "program_id":
                self.program_id,
            "verification_key":
                self.verification_key,
            "proof_digest":
                self.proof_digest,
            "public_values":
                self.public_values,
        }
