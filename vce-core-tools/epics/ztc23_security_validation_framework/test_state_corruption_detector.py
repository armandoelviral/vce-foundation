from epics.ztc23_security_validation_framework.state_corruption_detector import (
    StateCorruptionDetector,
)


def test_accepts_identical_states():

    detector = StateCorruptionDetector()

    expected = {
        "sequence": 1,
        "event_count": 5,
    }

    observed = {
        "sequence": 1,
        "event_count": 5,
    }

    result = detector.detect(
        expected,
        observed,
    )

    assert result["corrupted"] is False


def test_detects_sequence_corruption():

    detector = StateCorruptionDetector()

    expected = {
        "sequence": 1,
    }

    observed = {
        "sequence": 99,
    }

    result = detector.detect(
        expected,
        observed,
    )

    assert result["corrupted"] is True


def test_reports_differences():

    detector = StateCorruptionDetector()

    expected = {
        "event_count": 5,
    }

    observed = {
        "event_count": 10,
    }

    result = detector.detect(
        expected,
        observed,
    )

    assert "event_count" in result["differences"]
