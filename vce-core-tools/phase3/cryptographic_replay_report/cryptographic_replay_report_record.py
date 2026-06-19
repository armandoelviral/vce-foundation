from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class CryptographicReplayReportRecord:

    report_id: str
    certificate_id: str
    status: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "report_id": self.report_id,
            "certificate_id": self.certificate_id,
            "status": self.status,
        }
