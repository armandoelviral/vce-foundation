from sp001.contracts.case_access_grant_administration import (
    CaseAccessGrantAdministrationStore,
    CaseGrantAdministrationPolicy,
    GrantAdministrationRecord,
)


def administer_case_access_grant(
    *,
    store: CaseAccessGrantAdministrationStore,
    policy: CaseGrantAdministrationPolicy,
    record: GrantAdministrationRecord,
) -> bool:
    """Authorize before invoking the trusted atomic persistence capability."""
    if not isinstance(store, CaseAccessGrantAdministrationStore):
        raise TypeError("store must implement CaseAccessGrantAdministrationStore")
    if not isinstance(policy, CaseGrantAdministrationPolicy):
        raise TypeError("policy must implement CaseGrantAdministrationPolicy")
    if not isinstance(record, GrantAdministrationRecord):
        raise TypeError("record must be a GrantAdministrationRecord")
    allowed = policy.may_administer(
        actor=record.actor, action=record.action, grant=record.grant,
    )
    if type(allowed) is not bool:
        raise TypeError("administration policy must return an exact bool")
    if not allowed:
        raise PermissionError("grant administration denied")
    result = store.apply(record=record)
    if type(result) is not bool:
        raise TypeError("administration store must return an exact bool")
    return result
