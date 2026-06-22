from dataclasses import dataclass


@dataclass(frozen=True)
class ResponseEvidence:

    citizen_did: str
    evidence_type: str
    evidence_value: str

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "evidence_type":
                self.evidence_type,
            "evidence_value":
                self.evidence_value,
        }
