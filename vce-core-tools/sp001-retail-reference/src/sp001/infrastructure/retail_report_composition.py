from collections.abc import Callable
from pathlib import Path

from sp001.contracts.access_token_key_resolver import AccessTokenKeyResolver
from sp001.infrastructure.jwt_case_access_authenticator import (
    JwtCaseAccessAuthenticator,
)
from sp001.infrastructure.sqlite_admitted_retail_report_writer import (
    SqliteAdmittedRetailReportWriter,
)
from sp001.services.transactional_authenticated_retail_reports import (
    TransactionalAuthenticatedRetailReports,
)


def compose_transactional_retail_reports(
    *,
    issuer: str,
    audience: str,
    key_resolver: AccessTokenKeyResolver,
    max_lifetime_seconds: int,
    max_token_bytes: int,
    database_path: str | Path,
    clock: Callable[[], int],
) -> TransactionalAuthenticatedRetailReports:
    """Compose JWT verification and same-database local authorization.

    The JWT library also validates time using its system clock.
    The supplied Unix-second clock must agree with that clock.
    Does not generate keys. Evaluator admission uses save_with_admissions.
    """
    authenticator = JwtCaseAccessAuthenticator(
        issuer=issuer,
        audience=audience,
        key_resolver=key_resolver,
        max_lifetime_seconds=max_lifetime_seconds,
        max_token_bytes=max_token_bytes,
    )
    backend = SqliteAdmittedRetailReportWriter(
        database_path=database_path,
        expected_audience=audience,
        clock=clock,
    )
    return TransactionalAuthenticatedRetailReports(
        authenticator=authenticator,
        backend=backend,
        expected_audience=audience,
        clock=clock,
    )
