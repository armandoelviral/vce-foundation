from dataclasses import dataclass


@dataclass(frozen=True)
class AdmissionState:

    citizen_did: str
    admission_state: str

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "admission_state":
                self.admission_state,
        }
