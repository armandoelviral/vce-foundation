from epics.epic017_supply_chain.rekor_client import (
    RekorClient
)


rekor = RekorClient()


artifact = {
    "name": "vce-runtime",
    "version": "v0.1",
    "signature": "abc123"
}


entry = rekor.create_entry(
    artifact
)


print(
    rekor.verify_entry(
        entry
    )
)


entry[
    "inclusion_proof"
] = False


print(
    rekor.verify_entry(
        entry
    )
)
