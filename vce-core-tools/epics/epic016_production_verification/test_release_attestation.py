from epics.epic016_production_verification.release_attestation import (
    ReleaseArtifactAttestation
)


release = ReleaseArtifactAttestation()


artifact = {
    "name": "VCE Runtime",
    "version": "v0.1-rc",
    "build": "reproducible"
}


attestation = release.create(
    artifact
)


print(
    attestation["attestation_type"]
)


print(
    release.verify(
        attestation
    )
)


attestation["artifact"]["version"] = (
    "tampered"
)


print(
    release.verify(
        attestation
    )
)
