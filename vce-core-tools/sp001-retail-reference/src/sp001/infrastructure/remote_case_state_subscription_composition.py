from collections.abc import Callable

from sp001.infrastructure.case_state_http_route import validate_case_path_id
from sp001.infrastructure.remote_case_state_reader import RemoteCaseStateReader
from sp001.services.supervised_case_state_subscription import (
    SupervisedCaseStateSubscription,
)


def compose_remote_case_state_subscription(
    *, endpoint: str, case_id: str,
    credential_provider: Callable[[], str],
    timeout_seconds: float, max_response_bytes: int,
    ca_file: str | None = None,
    clock: Callable[[], float] | None = None,
) -> SupervisedCaseStateSubscription:
    """Compose an authenticated HTTPS reader with terminal visibility policy.

    No automatic refresh, polling worker or credential renewal.
    """
    validate_case_path_id(case_id)
    if not callable(credential_provider):
        raise TypeError("credential_provider must be callable")
    if clock is not None and not callable(clock):
        raise TypeError("clock must be callable")
    reader = RemoteCaseStateReader(
        endpoint=endpoint, timeout_seconds=timeout_seconds,
        max_response_bytes=max_response_bytes, ca_file=ca_file,
        credential_provider=credential_provider,
    )
    return SupervisedCaseStateSubscription(
        reader=reader, case_id=case_id, clock=clock,
    )
