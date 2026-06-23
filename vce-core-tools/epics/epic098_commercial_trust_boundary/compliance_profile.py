from dataclasses import dataclass


@dataclass(frozen=True)
class ComplianceProfile:

    profile_id: str
    jurisdiction: str
    residency_required: bool
    hsm_required: bool

    def to_dict(self):

        return {
            "profile_id": self.profile_id,
            "jurisdiction": self.jurisdiction,
            "residency_required": self.residency_required,
            "hsm_required": self.hsm_required,
        }
