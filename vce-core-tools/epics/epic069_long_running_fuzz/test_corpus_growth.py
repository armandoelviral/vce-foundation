from pathlib import Path


CORPUS = Path(
    "fuzz-runtime/fuzz/corpus/fuzz_target_1"
)


def test_corpus_directory_exists():

    assert CORPUS.exists()


def test_corpus_contains_generated_inputs():

    files = list(CORPUS.iterdir())

    assert len(files) > 3


def test_seed_files_exist():

    assert (CORPUS / "replay_seed").exists()
    assert (CORPUS / "hash_chain_seed").exists()
    assert (CORPUS / "wal_recovery_seed").exists()
