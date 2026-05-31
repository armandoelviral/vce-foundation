from epics.epic013_external_trust.trust_pipeline import RuntimeExternalTrustPipeline


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


pipeline = RuntimeExternalTrustPipeline()

result = pipeline.execute(
    events,
    certificate
)

print(result["runtime_replay"])
print(result["attestation_signature"])
print(result["external_trust"])
print(result["ledger_admission"])
print(result["sequence_number"])
print(result["state_hash"])
