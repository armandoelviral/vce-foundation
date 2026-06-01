from epics.epic017_supply_chain.fulcio_verifier import (
    FulcioVerifier
)


verifier = FulcioVerifier()


valid_cert = {
    "issuer": "https://fulcio.sigstore.dev",
    "subject": "repo:vce-foundation/vce-core-tools",
    "repository": "vce-foundation/vce-core-tools",
    "workflow": "release.yml"
}


invalid_cert = {
    "issuer": "unknown",
    "repository": "vce-foundation/vce-core-tools"
}


print(
    verifier.verify(
        valid_cert
    )["certificate_valid"]
)


print(
    verifier.verify(
        invalid_cert
    )["certificate_valid"]
)
