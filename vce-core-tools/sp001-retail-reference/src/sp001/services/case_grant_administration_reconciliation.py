import sqlite3

from sp001.contracts.administration_event_reader import (
    AdministrationEventReader,
)
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationRecord,
)
from sp001.contracts.case_grant_administration_reconciliation import (
    AdministrationReconciliationResult,
    AdministrationReconciliationStatus as Status,
)
from sp001.contracts.administration_event_errors import (
    InvalidPersistedAdministrationEventError,
)


def reconcile_administration_event(
    *,
    reader: AdministrationEventReader,
    expected: GrantAdministrationRecord,
) -> AdministrationReconciliationResult:
    """Classify one read without retrying or mutating the grant."""

    if not isinstance(expected, GrantAdministrationRecord):
        raise TypeError("expected must be a GrantAdministrationRecord")

    if reader is None or not callable(
        getattr(reader, "read_administration_event", None)
    ):
        raise TypeError("reader must support read_administration_event")

    try:
        observed = reader.read_administration_event(
            event_id=expected.event_id
        )
    except InvalidPersistedAdministrationEventError:
        status = Status.READ_INVALID
    except sqlite3.Error:
        status = Status.READ_UNAVAILABLE
    else:
        if observed is None:
            status = Status.EVENT_NOT_FOUND
        elif not isinstance(observed, GrantAdministrationRecord):
            raise TypeError(
                "reader returned an invalid administration record type"
            )
        elif observed == expected:
            status = Status.EXACT_MATCH
        else:
            status = Status.EVENT_CONFLICT

    return AdministrationReconciliationResult(
        event_id=expected.event_id,
        status=status,
    )
