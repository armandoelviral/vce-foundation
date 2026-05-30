from hash_chain import HashChain

chain = HashChain()

print(
    chain.append(
        "1|APPEND_EVIDENCE|artifact-TAMPERED"
    )
)

print(
    chain.append(
        "2|REGISTER_ARTIFACT|artifact-001"
    )
)

print(
    chain.append(
        "3|SEAL_SNAPSHOT|snapshot-001"
    )
)
