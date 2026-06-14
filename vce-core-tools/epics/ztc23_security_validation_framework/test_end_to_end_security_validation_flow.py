from epics.ztc23_security_validation_framework.fuzz_input_corpus import (
    FuzzInputCorpus,
)

from epics.ztc23_security_validation_framework.replay_fuzz_harness import (
    ReplayFuzzHarness,
)

from epics.ztc23_security_validation_framework.state_corruption_detector import (
    StateCorruptionDetector,
)

from epics.ztc23_security_validation_framework.property_based_replay_testing import (
    PropertyBasedReplayTesting,
)

from epics.ztc23_security_validation_framework.consensus_fault_injection import (
    ConsensusFaultInjection,
)

from epics.ztc23_security_validation_framework.tamper_simulation_framework import (
    TamperSimulationFramework,
)

from epics.ztc23_security_validation_framework.security_validation_report import (
    SecurityValidationReport,
)


def test_end_to_end_security_validation_flow():

    corpus = FuzzInputCorpus()

    corpus.add(
        {"opcode": "APPEND_EVENT"}
    )

    harness = ReplayFuzzHarness(
        corpus=corpus,
    )

    fuzz_results = harness.run(
        target=lambda payload: True,
    )

    assert fuzz_results[0]["passed"]

    detector = StateCorruptionDetector()

    corruption_result = detector.detect(
        expected={
            "sequence": 1,
        },
        observed={
            "sequence": 1,
        },
    )

    assert not corruption_result[
        "corrupted"
    ]

    replay_state = {
        "previous_sequence": 1,
        "current_sequence": 2,
        "event_count": 5,
        "state_hash": "hash-001",
    }

    assert (
        PropertyBasedReplayTesting
        .validate(
            replay_state
        )
    )

    injector = (
        ConsensusFaultInjection()
    )

    votes = injector.inject(
        votes=[
            True,
            True,
            True,
        ],
        fault_type="offline",
    )

    assert len(votes) == 2

    tamper = (
        TamperSimulationFramework()
    )

    forged = tamper.tamper(
        record={
            "event_id": "event-001",
        },
        field="event_id",
        value="event-999",
    )

    assert (
        forged["event_id"]
        == "event-999"
    )

    report = (
        SecurityValidationReport(
            report_id="report-001",
            total_tests=5,
            failures=0,
        )
    )

    assert (
        report.successes()
        == 5
    )
