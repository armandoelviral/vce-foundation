from typing import Protocol

from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationRecord,
)


class AdministrationEventReader(Protocol):
    """Read one administrative event without mutation authority."""

    def read_administration_event(
        self, *, event_id: str
    ) -> GrantAdministrationRecord | None:
        ...
