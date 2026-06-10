from dataclasses import dataclass


@dataclass(frozen=True)
class S3WORMBucket:
    bucket_name: str
    region: str
    object_lock_enabled: bool
    versioning_enabled: bool
    retention_mode: str
    retention_days: int

    def is_compliance_ready(self):

        return (
            self.object_lock_enabled is True
            and self.versioning_enabled is True
            and self.retention_mode == "COMPLIANCE"
            and self.retention_days > 0
        )
