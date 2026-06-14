from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SecurityValidationReport:

    report_id: str
    total_tests: int
    failures: int

    def successes(
        self,
    ) -> int:

        return (
            self.total_tests
            - self.failures
        )

    def to_dict(
        self,
    ) -> Dict[str, int | str]:

        return {
            "report_id": self.report_id,
            "total_tests": self.total_tests,
            "failures": self.failures,
            "successes": self.successes(),
        }
