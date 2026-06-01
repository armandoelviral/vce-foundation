from epics.epic016_production_verification.reproducible_build import (
    ReproducibleBuildProof
)


builder = ReproducibleBuildProof()


manifest = {
    "source": "vce-runtime",
    "version": "v0.1-rc",
    "dependencies": [
        "runtime-core",
        "trust-engine",
        "hardening-layer"
    ]
}


build_a = builder.build_hash(
    manifest
)


build_b = builder.build_hash(
    manifest
)


tampered_manifest = {
    "source": "vce-runtime",
    "version": "modified"
}


build_c = builder.build_hash(
    tampered_manifest
)


print(
    builder.verify(
        build_a,
        build_b
    )
)


print(
    builder.verify(
        build_a,
        build_c
    )
)
