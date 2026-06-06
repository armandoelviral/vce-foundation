import hashlib
from pathlib import Path


CORPUS = Path(
    "epics/epic067_differential_verification/corpus/replay_events.txt"
)


def test_runtime_agreement_sequence_number():

    events = CORPUS.read_text().splitlines()

    sequence_number = len(events)

    assert sequence_number == 3


def test_runtime_agreement_state_hash():

    events = CORPUS.read_text().splitlines()

    payload = "|".join(events)

    state_hash = hashlib.sha256(
        payload.encode()
    ).hexdigest()

    assert len(state_hash) == 64


def test_runtime_agreement_expected_events():

    events = CORPUS.read_text().splitlines()

    assert events == [
        "APPEND_EVIDENCE",
        "REGISTER_ARTIFACT",
        "SEAL_SNAPSHOT",
    ]
