from epics.ztc23_security_validation_framework.fuzz_input_corpus import (
    FuzzInputCorpus,
)


def test_corpus_starts_empty():

    corpus = FuzzInputCorpus()

    assert corpus.count() == 0


def test_corpus_accepts_input():

    corpus = FuzzInputCorpus()

    corpus.add(
        {"opcode": "APPEND_EVENT"}
    )

    assert corpus.count() == 1


def test_corpus_returns_inputs():

    corpus = FuzzInputCorpus()

    payload = {
        "opcode": "APPEND_EVENT"
    }

    corpus.add(payload)

    assert corpus.all()[0] == payload
