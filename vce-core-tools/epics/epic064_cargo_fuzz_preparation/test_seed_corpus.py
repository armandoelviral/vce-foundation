from pathlib import Path


def test_seed_corpus_exists():

    corpus = Path(
        "epics/epic064_cargo_fuzz_preparation/corpus"
    )

    assert corpus.exists()


def test_seed_files_exist():

    files = [
        "replay_seed.txt",
        "hash_chain_seed.txt",
        "wal_recovery_seed.txt",
    ]

    for filename in files:

        path = Path(
            "epics/epic064_cargo_fuzz_preparation/corpus"
        ) / filename

        assert path.exists()
