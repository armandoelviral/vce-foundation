from dataclasses import dataclass


@dataclass(frozen=True)
class TcuSignaturesBlock:

    classical_ed25519: str
    post_quantum_mldsa65: str

    def to_dict(self):

        return {
            "classical_ed25519": self.classical_ed25519,
            "post_quantum_mldsa65": self.post_quantum_mldsa65,
        }
