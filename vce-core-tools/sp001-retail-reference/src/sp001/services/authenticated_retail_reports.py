from collections.abc import Callable
from typing import Protocol, runtime_checkable

from sp001.contracts.case_access_context import (
    CaseAccessContextAuthenticator, ValidatedCaseAccessContext,
)
from sp001.contracts.case_access_grant import CaseAccessGrantSource
from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportIdentity,
)
from sp001.services.retail_rule_evaluation_report import (
    RetailRuleEvaluationReport,
)
from sp001.services.retail_report_access_policy import (
    required_retail_report_permissions, token_allows_retail_report,
)


class RetailReportAuthenticationRejected(PermissionError):
    """Credential rejected or attributed context outside its validity."""


class RetailReportAccessDenied(PermissionError):
    """Required report access is not granted."""


@runtime_checkable
class RetailReportPersistence(Protocol):
    def save(
        self, *, identity: RetailRuleEvaluationReportIdentity,
        report: RetailRuleEvaluationReport,
    ) -> RetailRuleEvaluationReport:
        ...

    def recover(
        self, *, identity: RetailRuleEvaluationReportIdentity,
    ) -> RetailRuleEvaluationReport | None:
        ...


class AuthenticatedRetailReports:
    """Application gate; current-grant checks are not commit-atomic."""

    def __init__(
        self, *,
        authenticator: CaseAccessContextAuthenticator,
        grants: CaseAccessGrantSource,
        persistence: RetailReportPersistence,
        expected_audience: str,
        clock: Callable[[], int],
    ) -> None:
        if not isinstance(authenticator, CaseAccessContextAuthenticator):
            raise TypeError("invalid authenticator")
        if not isinstance(grants, CaseAccessGrantSource):
            raise TypeError("invalid grant source")
        if not isinstance(persistence, RetailReportPersistence):
            raise TypeError("invalid persistence capability")
        if not isinstance(expected_audience, str):
            raise TypeError("expected_audience must be a string")
        if not expected_audience.strip():
            raise ValueError("expected_audience must not be empty")
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._authenticator = authenticator
        self._grants = grants
        self._persistence = persistence
        self._audience = expected_audience
        self._clock = clock

    def _authenticate(self, credential):
        if not isinstance(credential, str):
            raise TypeError("credential must be a string")
        access = self._authenticator.authenticate(credential=credential)
        if access is None:
            raise RetailReportAuthenticationRejected("credential rejected")
        if not isinstance(access, ValidatedCaseAccessContext):
            raise TypeError("authenticator returned an invalid context")
        return access

    def _authorize(self, access, case_id, recover_only):
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
            access=access, case_id=case_id,
            expected_audience=self._audience,
            at_time=now, recover_only=recover_only,
        ):
            raise RetailReportAccessDenied("report access denied")
        for permission in required_retail_report_permissions(
            case_id=case_id, recover_only=recover_only,
        ):
            allowed = self._grants.permits(
                principal=access.principal, permission=permission, at_time=now,
            )
            if type(allowed) is not bool:
                raise TypeError("grant source must return an exact bool")
            if not allowed:
                raise RetailReportAccessDenied("report access denied")

    def save(self, *, credential, identity, report):
        if not isinstance(identity, RetailRuleEvaluationReportIdentity):
            raise TypeError("identity must be a report identity")
        if type(report) is not RetailRuleEvaluationReport:
            raise TypeError("report must be a RetailRuleEvaluationReport")
        access = self._authenticate(credential)
        self._authorize(access, report.case_id, False)
        confirmed = self._persistence.save(identity=identity, report=report)
        self._authorize(access, report.case_id, False)
        if type(confirmed) is not RetailRuleEvaluationReport:
            raise TypeError("persistence returned an invalid report")
        if confirmed != report:
            raise ValueError("persistence returned a different report")
        return confirmed

    def recover(self, *, credential, identity, case_id):
        if not isinstance(identity, RetailRuleEvaluationReportIdentity):
            raise TypeError("identity must be a report identity")
        # Validate the declared case before authentication or storage access.
        required_retail_report_permissions(case_id=case_id, recover_only=True)
        access = self._authenticate(credential)
        self._authorize(access, case_id, True)
        report = self._persistence.recover(identity=identity)
        self._authorize(access, case_id, True)
        if report is None:
            return None
        if type(report) is not RetailRuleEvaluationReport:
            raise TypeError("persistence returned an invalid report")
        if report.case_id != case_id:
            raise RetailReportAccessDenied("report access denied")
        return report
