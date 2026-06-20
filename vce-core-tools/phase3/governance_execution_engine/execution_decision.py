from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ExecutionDecision:

    status: str

    @staticmethod
    def from_authorization(
        authorized: bool,
    ):

        return ExecutionDecision(
            status=(
                "EXECUTE_ACTION"
                if authorized
                else "REJECT_ACTION"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status":
                self.status
        }
