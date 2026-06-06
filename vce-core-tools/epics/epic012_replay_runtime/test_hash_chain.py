from epics.epic012_replay_runtime.hash_chain import HashChain


def test_hash_chain_appends_multiple_records():

    chain = HashChain()

    r1 = chain.append(
        "1|APPEND_EVIDENCE|artifact-TAMPERED"
    )

    r2 = chain.append(
        "2|REGISTER_ARTIFACT|artifact-001"
    )

    r3 = chain.append(
        "3|SEAL_SNAPSHOT|snapshot-001"
    )

    assert r1 is not None
    assert r2 is not None
    assert r3 is not None


def test_hash_chain_generates_distinct_hashes():

    chain = HashChain()

    r1 = chain.append(
        "1|APPEND_EVIDENCE|artifact-TAMPERED"
    )

    r2 = chain.append(
        "2|REGISTER_ARTIFACT|artifact-001"
    )

    assert r1 != r2
