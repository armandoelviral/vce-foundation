from epics.ztc23_security_validation_framework.fuzz_input_corpus import (
    FuzzInputCorpus,
)

from epics.ztc23_security_validation_framework.replay_fuzz_harness import (
    ReplayFuzzHarness,
)


def test_harness_runs_all_inputs():

    corpus = FuzzInputCorpus()

    corpus.add({"opcode": "APPEND_EVENT"})
    corpus.add({"opcode": "REPLAY_STATE"})

    harness = ReplayFuzzHarness(
        corpus=corpus,
    )

    results = harness.run(
        target=lambda payload: True,
    )

    assert len(results) == 2


def test_harness_records_success():

    corpus = FuzzInputCorpus()

    corpus.add({"opcode": "APPEND_EVENT"})

    harness = ReplayFuzzHarness(
        corpus=corpus,
    )

    results = harness.run(
        target=lambda payload: True,
    )

    assert results[0]["passed"] is True


def test_harness_records_failure_without_crashing():

    corpus = FuzzInputCorpus()

    corpus.add({"opcode": "INVALID"})

    def target(payload):
        raise ValueError("invalid opcode")

    harness = ReplayFuzzHarness(
        corpus=corpus,
    )

    results = harness.run(
        target=target,
    )

    assert results[0]["passed"] is False
    assert results[0]["error"] == "invalid opcode"
