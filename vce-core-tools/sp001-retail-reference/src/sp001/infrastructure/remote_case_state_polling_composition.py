from sp001.infrastructure.case_state_polling_runner import CaseStatePollingRunner
from sp001.infrastructure.remote_case_state_subscription_composition import (
    compose_remote_case_state_subscription,
)


def compose_remote_case_state_polling(
    *,
    endpoint,
    case_id,
    credential_provider,
    timeout_seconds,
    max_response_bytes,
    ca_file=None,
    clock=None,
    interval_provider=None,
):
    """Compose HTTPS polling without starting workers or renewing credentials."""
    if clock is not None and not callable(clock):
        raise TypeError("clock must be callable")
    if interval_provider is not None and not callable(interval_provider):
        raise TypeError("interval_provider must be callable")
    subscription = compose_remote_case_state_subscription(
        endpoint=endpoint,
        case_id=case_id,
        credential_provider=credential_provider,
        timeout_seconds=timeout_seconds,
        max_response_bytes=max_response_bytes,
        ca_file=ca_file,
        clock=clock,
    )
    return CaseStatePollingRunner(
        subscription=subscription,
        clock=clock,
        interval_provider=interval_provider,
    )
