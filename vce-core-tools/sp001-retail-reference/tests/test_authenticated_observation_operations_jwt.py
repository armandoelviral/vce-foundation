import time
from dataclasses import replace

import pytest

import test_authenticated_inspection_observations_jwt as setup
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys  # pytest fixture
from sp001.contracts.retail_observation_operation import (
    RetailObservationSaveRequest as Request,
    RetailObservationEffectDisposition as Disposition,
    RetailObservationOperationConflict,
)
from sp001.infrastructure.sqlite_observation_operations import (
    SqliteObservationOperations as Backend,
)
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    InspectionObservationAuthenticationRejected as Rejected,
    InspectionObservationAccessDenied as Denied,
)
from sp001.services.authenticated_observation_operations import (
    AuthenticatedObservationOperations as Service,
)
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
    GrantAdministrationRecord,
)


def environment(tmp_path, keys):
    path, _, auth, grants, definitions = setup.environment(tmp_path, keys)
    backend = Backend(
        database_path=path,
        expected_audience=jwt_setup.AUDIENCE,
        clock=lambda: int(time.time()),
    )
    service = Service(
        authenticator=auth, backend=backend,
        expected_audience=jwt_setup.AUDIENCE,
        clock=lambda: int(time.time()),
    )
    return service, grants, definitions


def credential(keys, operations):
    return jwt_setup.token(keys[0], operations=operations)


def request():
    return Request("REQUEST", setup.observation(case_id=setup.CASE))


def test_signed_save_retry_and_recovery(tmp_path, keys):
    service, _, _ = environment(tmp_path, keys)
    item = request()
    write = credential(keys, (setup.SAVE,))
    read = credential(keys, (setup.READ,))
    receipt = service.save_operation(credential=write, request=item)
    assert receipt.disposition is Disposition.CREATED
    assert service.save_operation(credential=write, request=item) == receipt
    assert service.recover_operation(
        credential=read, case_id=setup.CASE, request_id=item.request_id,
    ) == receipt


@pytest.mark.parametrize("operation", ["save", "recover"])
def test_invalid_signature_is_rejected(tmp_path, keys, operation):
    service, _, _ = environment(tmp_path, keys)
    invalid = jwt_setup.token(
        keys[1], operations=(setup.SAVE, setup.READ),
    )
    with pytest.raises(Rejected):
        if operation == "save":
            service.save_operation(credential=invalid, request=request())
        else:
            service.recover_operation(
                credential=invalid, case_id=setup.CASE, request_id="REQUEST",
            )


def test_read_claim_cannot_write_and_write_claim_cannot_read(tmp_path, keys):
    service, _, _ = environment(tmp_path, keys)
    with pytest.raises(Denied):
        service.save_operation(
            credential=credential(keys, (setup.READ,)), request=request(),
        )
    with pytest.raises(Denied):
        service.recover_operation(
            credential=credential(keys, (setup.SAVE,)),
            case_id=setup.CASE, request_id="MISSING",
        )


def test_absence_is_returned_only_for_authorized_query(tmp_path, keys):
    service, _, _ = environment(tmp_path, keys)
    assert service.recover_operation(
        credential=credential(keys, (setup.READ,)),
        case_id=setup.CASE, request_id="MISSING",
    ) is None
    with pytest.raises(Denied):
        service.recover_operation(
            credential=credential(keys, (setup.READ,)),
            case_id="OTHER", request_id="MISSING",
        )


def test_same_token_is_denied_after_local_grant_revocation(tmp_path, keys):
    service, grants, definitions = environment(tmp_path, keys)
    token = credential(keys, (setup.SAVE, setup.READ))
    item = request()
    service.save_operation(credential=token, request=item)
    for index, grant in enumerate(definitions):
        assert grants.apply(record=GrantAdministrationRecord(
            f"OP-REVOKE-{index}", grant.principal, Action.REVOKE,
            grant, int(time.time()),
        ))
    with pytest.raises(Denied):
        service.save_operation(credential=token, request=item)
    with pytest.raises(Denied):
        service.recover_operation(
            credential=token, case_id=setup.CASE, request_id=item.request_id,
        )


def test_conflicting_retry_does_not_replace_receipt(tmp_path, keys):
    service, _, _ = environment(tmp_path, keys)
    token = credential(keys, (setup.SAVE, setup.READ))
    item = request()
    original = service.save_operation(credential=token, request=item)
    changed = replace(item, observation=replace(
        item.observation, description="Different content.",
    ))
    with pytest.raises(RetailObservationOperationConflict):
        service.save_operation(credential=token, request=changed)
    assert service.recover_operation(
        credential=token, case_id=setup.CASE, request_id=item.request_id,
    ) == original
