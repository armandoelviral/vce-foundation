from epics.ztc23_security_validation_framework.tamper_simulation_framework import (
    TamperSimulationFramework,
)


def test_tamper_payload_field():

    framework = TamperSimulationFramework()

    record = {
        "event_id": "event-001",
        "hash": "hash-001",
    }

    tampered = framework.tamper(
        record=record,
        field="event_id",
        value="event-999",
    )

    assert tampered["event_id"] == "event-999"


def test_original_record_remains_unchanged():

    framework = TamperSimulationFramework()

    record = {
        "event_id": "event-001",
    }

    tampered = framework.tamper(
        record=record,
        field="event_id",
        value="event-999",
    )

    assert record["event_id"] == "event-001"
    assert tampered["event_id"] == "event-999"


def test_add_new_tampered_field():

    framework = TamperSimulationFramework()

    record = {
        "event_id": "event-001",
    }

    tampered = framework.tamper(
        record=record,
        field="forged",
        value=True,
    )

    assert tampered["forged"] is True


def test_tampered_record_differs_from_original():

    framework = TamperSimulationFramework()

    record = {
        "event_id": "event-001",
    }

    tampered = framework.tamper(
        record=record,
        field="event_id",
        value="event-999",
    )

    assert tampered != record
