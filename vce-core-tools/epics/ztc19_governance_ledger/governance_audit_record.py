from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class GovernanceAuditRecord:
    audit_id: str
    ledger_valid: bool

    def to_dict(self) -> Dict[str, Union[str, bool]]:
        return {
            "audit_id": self.audit_id,
            "ledger_valid": self.ledger_valid,
        }
