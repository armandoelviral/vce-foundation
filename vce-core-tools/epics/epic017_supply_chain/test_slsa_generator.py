from epics.epic017_supply_chain.slsa_generator import (
    SLSAGenerator
)


generator = SLSAGenerator()


source = {
    "repository":
        "vce-foundation/vce-core-tools",

    "revision":
        "v0.1"
}


artifact = {
    "name":
        "vce-runtime",

    "digest":
        "abc123"
}


result = generator.generate(
    source,
    artifact
)


print(
    result["statement"]["predicateType"]
)


print(
    result["verified"]
)
