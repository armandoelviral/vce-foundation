from dataclasses import dataclass


@dataclass(frozen=True)
class AdmissionSecurityPolicy:

    mtls_required: bool
    mldsa_required: bool
    admission_required: bool

    def to_dict(self):

        return {
            "mtls_required": self.mtls_required,
            "mldsa_required": self.mldsa_required,
            "admission_required": self.admission_required,
        }
