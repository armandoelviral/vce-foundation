from epics.epic015_secure_runtime.secure_execution_engine import (
    SecureExecutionEngine
)


events = [
    {
        "lsn": 1,
        "opcode": "APPEND_EVIDENCE",
        "payload": "artifact"
    }
]


certificate = {
    "issuer": "github-actions",
    "subject": "repo:vce-foundation",
    "repository": "vce-core-tools",
    "expires_at": "2026-12-31"
}


engine = SecureExecutionEngine()

result = engine.execute(
    events,
    certificate
)

print(
    result["status"]
)

print(
    result["result"]
)
