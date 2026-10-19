import sqlite3
import time
from datetime import datetime, timezone

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation, CaseAccessPermission,
)
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action, GrantAdministrationRecord,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_context_rule_observation import (
    RetailContextRuleObservation, RuleObservationStatus,
)
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole
from sp001.contracts.retail_rule_criterion import RetailRuleCriterion
from sp001.contracts.retail_rule_evaluation_record import RetailRuleEvaluationRecord
from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportIdentity,
)
from sp001.infrastructure.configured_access_token_keys import (
    ConfiguredAccessTokenKeys,
)
from sp001.infrastructure.jwt_case_access_authenticator import (
    AccessTokenKeyResolutionError,
)
from sp001.infrastructure.retail_report_composition import (
    compose_transactional_retail_reports,
)
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.services.authenticated_retail_reports import (
    RetailReportAccessDenied, RetailReportAuthenticationRejected,
)
from sp001.services.retail_rule_evaluation_report import (
    build_retail_rule_evaluation_report,
)


ISSUER = "https://issuer.test"
AUDIENCE = "retail-reports-test"
IDENTITY = RetailRuleEvaluationReportIdentity("REPORT-1")


@pytest.fixture(scope="module")
def keys():
    # Synthetic signing keys, generated only by the test suite.
    return (
        rsa.generate_private_key(public_exponent=65537, key_size=2048),
        rsa.generate_private_key(public_exponent=65537, key_size=2048),
    )


def make_report():
    actor = RetailProcessActor(
        "ACTOR", "CUSTOMER", ActorType.HUMAN, "ORG",
        RetailProcessRole("ROLE", "CUSTOMER", "VM reviewer"),
    )
    evaluation = RetailRuleEvaluationRecord(
        "EVAL",
        RetailContextRuleObservation(
            "OBS", "RULE", "SNAPSHOT", 1, "CASE",
            RuleObservationStatus.CONFORMANT, ("EVIDENCE",),
        ),
        RetailRuleCriterion("RULE", 1, "Synthetic criterion."),
        actor, datetime(2026, 1, 1, tzinfo=timezone.utc),
        "Synthetic rationale.",
    )
    return build_retail_rule_evaluation_report(
        case_id="CASE", evaluations=(evaluation,),
    )


def token(key, *, operations=None, overrides=None):
    now = int(time.time())
    if operations is None:
        operations = (Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT)
    claims = {
        "iss": ISSUER, "sub": "SUBJECT", "aud": AUDIENCE,
        "iat": now - 2, "nbf": now - 1, "exp": now + 60,
        "case_permissions": [
            {"case_id": "CASE", "operation": operation.value}
            for operation in operations
        ],
    }
    claims.update(overrides or {})
    return jwt.encode(
        claims, key, algorithm="RS256",
        headers={"kid": "KEY-1", "typ": "at+jwt"},
    )


def environment(tmp_path, keys):
    path = tmp_path / "shared.sqlite3"
    service = compose_transactional_retail_reports(
        issuer=ISSUER, audience=AUDIENCE,
        key_resolver=ConfiguredAccessTokenKeys(
            issuer=ISSUER, public_keys={"KEY-1": keys[0].public_key()},
        ),
        max_lifetime_seconds=120, max_token_bytes=16384,
        database_path=path, clock=lambda: int(time.time()),
    )
    grants = SqliteCaseAccessGrants(database_path=path)
    principal = AuthenticatedPrincipal(ISSUER, "SUBJECT")
    now = int(time.time())
    definitions = []
    for index, operation in enumerate((
        Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT,
    )):
        grant = CaseAccessGrant(
            f"GRANT-{index}", principal,
            CaseAccessPermission("CASE", operation),
            now - 10, now + 600,
        )
        assert grants.apply(record=GrantAdministrationRecord(
            f"EVENT-{index}", principal, Action.GRANT, grant, now,
        ))
        definitions.append(grant)
    return path, service, grants, definitions


def row_count(path):
    with sqlite3.connect(path) as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM retail_rule_evaluation_reports"
        ).fetchone()[0]


def test_signed_credential_save_retry_and_recovery(tmp_path, keys):
    path, service, _, _ = environment(tmp_path, keys)
    credential = token(keys[0])
    report = make_report()
    assert service.save(
        credential=credential, identity=IDENTITY, report=report,
    ) == report
    assert service.save(
        credential=credential, identity=IDENTITY, report=report,
    ) == report
    read_credential = token(keys[0], operations=(Operation.READ_RETAIL_REPORT,))
    assert service.recover(
        credential=read_credential, identity=IDENTITY, case_id="CASE",
    ) == report
    assert row_count(path) == 1


@pytest.mark.parametrize("fault", ["signature", "audience", "issuer", "expired"])
def test_invalid_credential_never_persists_report(tmp_path, keys, fault):
    path, service, _, _ = environment(tmp_path, keys)
    signing_key = keys[1] if fault == "signature" else keys[0]
    overrides = {}
    if fault == "audience":
        overrides["aud"] = "OTHER-AUDIENCE"
    elif fault == "issuer":
        overrides["iss"] = "https://other-issuer.test"
    elif fault == "expired":
        now = int(time.time())
        overrides.update(iat=now - 90, nbf=now - 90, exp=now - 1)

    with pytest.raises(RetailReportAuthenticationRejected):
        service.save(
            credential=token(signing_key, overrides=overrides),
            identity=IDENTITY, report=make_report(),
        )
    assert row_count(path) == 0


def test_state_read_claim_does_not_authorize_report_write(tmp_path, keys):
    path, service, _, _ = environment(tmp_path, keys)
    with pytest.raises(RetailReportAccessDenied):
        service.save(
            credential=token(keys[0], operations=(Operation.READ_STATE,)),
            identity=IDENTITY, report=make_report(),
        )
    assert row_count(path) == 0


def test_valid_jwt_does_not_replace_current_local_grants(tmp_path, keys):
    path, service, grants, definitions = environment(tmp_path, keys)
    credential = token(keys[0])
    report = make_report()
    service.save(credential=credential, identity=IDENTITY, report=report)
    for index, grant in enumerate(definitions):
        assert grants.apply(record=GrantAdministrationRecord(
            f"REVOKE-{index}", grant.principal,
            Action.REVOKE, grant, int(time.time()),
        ))
    with pytest.raises(RetailReportAccessDenied):
        service.save(credential=credential, identity=IDENTITY, report=report)
    with pytest.raises(RetailReportAccessDenied):
        service.recover(
            credential=credential, identity=IDENTITY, case_id="CASE",
        )
    assert row_count(path) == 1


def test_key_provider_failure_remains_distinct(tmp_path, keys):
    class BrokenResolver:
        def resolve(self, *, issuer, key_id, algorithm):
            raise OSError("synthetic trusted provider failure")

    path = tmp_path / "provider.sqlite3"
    service = compose_transactional_retail_reports(
        issuer=ISSUER, audience=AUDIENCE, key_resolver=BrokenResolver(),
        max_lifetime_seconds=120, max_token_bytes=16384,
        database_path=path, clock=lambda: int(time.time()),
    )
    with pytest.raises(AccessTokenKeyResolutionError):
        service.save(
            credential=token(keys[0]), identity=IDENTITY, report=make_report(),
        )
    assert row_count(path) == 0
