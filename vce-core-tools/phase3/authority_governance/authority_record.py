from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class AuthorityRecord:

    authority_id: str
    principal_id: str
    role: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "authority_id": self.authority_id,
            "principal_id": self.principal_id,
            "role": self.role,
        }
