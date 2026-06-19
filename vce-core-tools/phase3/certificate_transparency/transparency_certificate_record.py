from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class TransparencyCertificateRecord:

    entry_id: str
    certificate_id: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "entry_id": self.entry_id,
            "certificate_id": self.certificate_id,
        }
