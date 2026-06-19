from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class DidDocumentRecord:

    did: str
    controller: str
    classical_key_id: str
    pqc_key_id: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "did": self.did,
            "controller": self.controller,
            "classical_key_id": self.classical_key_id,
            "pqc_key_id": self.pqc_key_id,
        }
