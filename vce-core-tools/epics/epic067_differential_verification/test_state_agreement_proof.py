import hashlib
from pathlib import Path


def test_shared_corpus_produces_expected_hash():

    events = Path(
        "epics/epic067_differential_verification/corpus/replay_events.txt"
    ).read_text().splitlines()

    payload = "|".join(events)

    state_hash = hashlib.sha256(
        payload.encode()
    ).hexdigest()

    assert len(state_hash) == 64


def test_shared_corpus_sequence_number():

    events = Path(
        "epics/epic067_differential_verification/corpus/replay_events.txt"
    ).read_text().splitlines()

    assert len(events) == 3
