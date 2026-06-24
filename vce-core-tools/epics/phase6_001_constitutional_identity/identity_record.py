from dataclasses import dataclass


@dataclass(frozen=True)
class IdentityRecord:
    identity_id: str
    subject_id: str
    identity_type: str

    def __post_init__(self):
        if not self.identity_id:
            raise ValueError("identity_id is required")

        if not self.subject_id:
            raise ValueError("subject_id is required")

        if not self.identity_type:
            raise ValueError("identity_type is required")
