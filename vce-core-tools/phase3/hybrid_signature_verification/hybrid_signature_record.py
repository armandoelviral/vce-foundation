from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class HybridSignatureRecord:

    witness_did: str
    classical_signature: str
    pqc_signature: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "witness_did":
                self.witness_did,

            "classical_signature":
                self.classical_signature,

            "pqc_signature":
                self.pqc_signature,
        }
