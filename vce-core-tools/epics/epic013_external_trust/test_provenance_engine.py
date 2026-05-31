from epics.epic013_external_trust.provenance_engine import ProvenanceEngine


events = [
    {
        "lsn": 1,
        "opcode": "APPEND_EVIDENCE",
        "payload": "github-workflow-run-001"
    },
    {
        "lsn": 2,
        "opcode": "REGISTER_ARTIFACT",
        "payload": "runtime-attestation-001"
    },
    {
        "lsn": 3,
        "opcode": "SEAL_SNAPSHOT",
        "payload": "snapshot-001"
    }
]


certificate = {
    "issuer": "github-actions",
    "subject": "repo:vce-foundation",
    "repository": "vce-core-tools",
    "expires_at": "2026-12-31"
}


engine = ProvenanceEngine()

result = engine.execute(
    events,
    certificate
)

print(result)
