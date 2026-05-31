from transparency_log import TransparencyLog


log = TransparencyLog()


artifact = {
    "name": "vce-runtime-attestation",
    "state_hash": "abc123"
}


entry = log.create_entry(
    artifact
)


print(
    entry
)


print(
    log.verify_inclusion(
        entry
    )
)
