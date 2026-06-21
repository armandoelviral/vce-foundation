from dataclasses import dataclass


@dataclass(frozen=True)
class TcuProofBlock:

    proof_backend: str
    proof_status: str
    verification_key: str
    proof_hash: str

    def to_dict(self):

        return {
            "proof_backend": self.proof_backend,
            "proof_status": self.proof_status,
            "verification_key": self.verification_key,
            "proof_hash": self.proof_hash,
        }
