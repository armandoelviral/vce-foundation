from epics.epic013_external_trust.full_trust_pipeline import FullTrustPipeline


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


pipeline = FullTrustPipeline()

result = pipeline.execute(
    events,
    certificate
)


print(
    result["trust"]["external_trust"]
)

print(
    result["ledger"]["status"]
)
