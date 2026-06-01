from epics.epic017_supply_chain.cosign_adapter import (
    CosignAdapter
)


cosign = CosignAdapter()


artifact = {
    "name": "vce-runtime",
    "version": "v0.1",
    "digest": "abc123"
}


certificate = {
    "issuer": "https://fulcio.sigstore.dev",
    "subject": "repo:vce-foundation/vce-core-tools",
    "repository": "vce-foundation/vce-core-tools",
    "workflow": "release.yml"
}


result = cosign.verify(
    artifact,
    certificate
)


print(
    result["verified"]
)


print(
    result["certificate"]
)


print(
    result["rekor"]
)
