from epics.epic015_secure_runtime.audit_export import (
    AuditTrailExport
)


audit = AuditTrailExport()


result = {
    "execution": "VERIFIED",
    "trust": "ACCEPTED",
    "ledger": "COMMITTED"
}


export = audit.export(
    result
)


print(
    "audit_hash" in export
)


print(
    export["audit_record"]["execution"]["ledger"]
)
