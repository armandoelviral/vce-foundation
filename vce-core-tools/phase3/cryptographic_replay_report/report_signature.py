from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ReportSignature:

    report_id: str
    signature: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "report_id": self.report_id,
            "signature": self.signature,
        }
