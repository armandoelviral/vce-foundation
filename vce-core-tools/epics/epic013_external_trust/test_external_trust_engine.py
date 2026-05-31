from external_trust_engine import ExternalTrustEngine


engine = ExternalTrustEngine()


certificate = {
    "issuer": "github-actions",
    "subject": "repo:vce-foundation",
    "repository": "vce-core-tools",
    "expires_at": "2026-12-31"
}


artifact = {
    "name": "runtime-attestation",
    "hash": "abc123"
}


print(
    engine.verify(
        certificate,
        artifact
    )
)
