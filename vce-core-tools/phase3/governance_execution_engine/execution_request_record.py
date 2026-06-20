from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ExecutionRequestRecord:

    request_id: str
    resource_type: str
    action: str
    subject: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "request_id":
                self.request_id,

            "resource_type":
                self.resource_type,

            "action":
                self.action,

            "subject":
                self.subject,
        }
