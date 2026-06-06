from epics.epic012_replay_runtime.hash_chain import HashChain

def verify_wal(records):

    chain = HashChain()

    expected_hashes = []

    for record in records:

        expected_hashes.append(
            chain.append(record)
        )

    return expected_hashes
