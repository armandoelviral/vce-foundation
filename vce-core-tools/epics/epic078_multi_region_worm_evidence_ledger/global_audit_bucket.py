from dataclasses import dataclass


@dataclass(frozen=True)
class GlobalAuditBucket:
    bucket_name: str
    primary_region: str
    replica_regions: list[str]
    read_only: bool
    worm_enabled: bool

    def is_audit_ready(self):

        return (
            self.read_only is True
            and self.worm_enabled is True
            and len(self.replica_regions) > 0
        )
