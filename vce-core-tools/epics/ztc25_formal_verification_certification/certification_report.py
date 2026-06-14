from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class CertificationReport:

    report_id: str
    obligations_checked: int
    violations: int

    def satisfied(
        self,
    ) -> int:

        return (
            self.obligations_checked
            - self.violations
        )

    def to_dict(
        self,
    ) -> Dict[str, int | str]:

        return {
            "report_id": self.report_id,
            "obligations_checked": self.obligations_checked,
            "violations": self.violations,
            "satisfied": self.satisfied(),
        }
