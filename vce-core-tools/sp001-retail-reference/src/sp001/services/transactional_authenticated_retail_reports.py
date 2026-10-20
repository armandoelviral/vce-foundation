from collections.abc import Callable
from typing import Protocol, runtime_checkable

from sp001.contracts.case_access_context import (
    CaseAccessContextAuthenticator, ValidatedCaseAccessContext,
)
from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportIdentity,
)
from sp001.services.authenticated_retail_reports import (
    RetailReportAccessDenied, RetailReportAuthenticationRejected,
)
from sp001.services.retail_report_access_policy import (
    required_retail_report_permissions, token_allows_retail_report,
)
from sp001.services.retail_rule_evaluation_report import (
    RetailRuleEvaluationReport,
)


@runtime_checkable
class AuthorizedRetailReportBackend(Protocol):
    def save_authorized(
        self, *, access: ValidatedCaseAccessContext,
        identity: RetailRuleEvaluationReportIdentity,
        report: RetailRuleEvaluationReport,
    ) -> RetailRuleEvaluationReport:
        """Authorize within the write transaction, including identical retries."""
        ...

    def recover_authorized(
        self, *, access: ValidatedCaseAccessContext,
        identity: RetailRuleEvaluationReportIdentity, case_id: str,
    ) -> RetailRuleEvaluationReport | None:
        """Authorize and read from one local snapshot; validate report case."""
        ...


class TransactionalAuthenticatedRetailReports:
    """Credential boundary for an explicitly authorized transactional backend."""

    def __init__(
        self, *, authenticator: CaseAccessContextAuthenticator,
        backend: AuthorizedRetailReportBackend,
        expected_audience: str, clock: Callable[[], int],
    ) -> None:
        if not isinstance(authenticator, CaseAccessContextAuthenticator):
            raise TypeError("invalid authenticator")
        if not isinstance(backend, AuthorizedRetailReportBackend):
            raise TypeError("backend must implement authorized operations")
        if not isinstance(expected_audience, str):
            raise TypeError("expected_audience must be a string")
        if not expected_audience.strip():
            raise ValueError("expected_audience must not be empty")
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._authenticator = authenticator
        self._backend = backend
        self._audience = expected_audience
        self._clock = clock

    def _check(self, access, case_id, recover_only):
        now = self._clock()
        if type(now) is not int:
            raise TypeError("clock must return integer Unix seconds")
        if now < 0:
            raise ValueError("clock must return nonnegative Unix seconds")
        if (
            access.audience != self._audience
            or not access.issued_at <= access.not_before <= now < access.expires_at
        ):
            raise RetailReportAuthenticationRejected("access context unusable")
        if not token_allows_retail_report(
            access=access, case_id=case_id, expected_audience=self._audience,
            at_time=now, recover_only=recover_only,
        ):
            raise RetailReportAccessDenied("report access denied")

    def _authenticate(self, credential):
        if not isinstance(credential, str):
            raise TypeError("credential must be a string")
        access = self._authenticator.authenticate(credential=credential)
        if access is None:
            raise RetailReportAuthenticationRejected("credential rejected")
        if not isinstance(access, ValidatedCaseAccessContext):
            raise TypeError("authenticator returned an invalid context")
        return access

    def save(self, *, credential, identity, report):
        if not isinstance(identity, RetailRuleEvaluationReportIdentity):
            raise TypeError("identity must be a report identity")
        if type(report) is not RetailRuleEvaluationReport:
            raise TypeError("report must be a RetailRuleEvaluationReport")
        access = self._authenticate(credential)
        self._check(access, report.case_id, False)
        result = self._backend.save_authorized(
            access=access, identity=identity, report=report,
        )
        self._check(access, report.case_id, False)
        if type(result) is not RetailRuleEvaluationReport:
            raise TypeError("backend returned an invalid report")
        if result != report:
            raise ValueError("backend returned a different report")
        return result

    def save_with_admissions(
        self, *, credential, identity, report, binding_references,
    ):
        """Explicit attribution admission; no fallback to declarative saves."""
        if not isinstance(identity, RetailRuleEvaluationReportIdentity):
            raise TypeError("identity must be a report identity")
        if type(report) is not RetailRuleEvaluationReport:
            raise TypeError("report must be a RetailRuleEvaluationReport")
        access = self._authenticate(credential)
        self._check(access, report.case_id, False)
        operation = getattr(
            self._backend, "save_with_admissions_authorized", None,
        )
        if not callable(operation):
            raise TypeError("backend does not support attribution admission")
        result = operation(
            access=access, identity=identity, report=report,
            binding_references=binding_references,
        )
        self._check(access, report.case_id, False)
        if type(result) is not RetailRuleEvaluationReport:
            raise TypeError("backend returned an invalid report")
        if result != report:
            raise ValueError("backend returned a different report")
        return result

    def recover(self, *, credential, identity, case_id):
        if not isinstance(identity, RetailRuleEvaluationReportIdentity):
            raise TypeError("identity must be a report identity")
        required_retail_report_permissions(
            case_id=case_id, recover_only=True,
        )
        access = self._authenticate(credential)
        self._check(access, case_id, True)
        result = self._backend.recover_authorized(
            access=access, identity=identity, case_id=case_id,
        )
        self._check(access, case_id, True)
        if result is None:
            return None
        if type(result) is not RetailRuleEvaluationReport:
            raise TypeError("backend returned an invalid report")
        if result.case_id != case_id:
            raise RetailReportAccessDenied("report access denied")
        return result
