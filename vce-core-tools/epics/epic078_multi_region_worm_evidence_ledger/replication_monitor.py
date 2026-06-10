from dataclasses import dataclass


@dataclass(frozen=True)
class ReplicationHealth:
    source_region: str
    destination_region: str
    replication_enabled: bool
    last_replication_status: str
    replication_lag_seconds: int
    failure_count: int

    def is_healthy(self):

        return (
            self.replication_enabled is True
            and self.last_replication_status == "COMPLETED"
            and self.replication_lag_seconds <= 900
            and self.failure_count == 0
        )
