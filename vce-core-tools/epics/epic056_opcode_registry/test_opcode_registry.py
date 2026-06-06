from epics.epic056_opcode_registry.opcode_registry import (
    OpcodeRegistry,
)


def test_registers_and_executes_opcode():

    registry = OpcodeRegistry()

    def handler(payload):
        return {
            "handled": True,
            "payload": payload,
        }

    registry.register(
        "TEST_OPCODE",
        handler,
    )

    result = registry.execute(
        "TEST_OPCODE",
        {"value": 1},
    )

    assert result == {
        "handled": True,
        "payload": {"value": 1},
    }


def test_rejects_unknown_opcode():

    registry = OpcodeRegistry()

    result = registry.execute(
        "UNKNOWN_OPCODE",
        {"value": 1},
    )

    assert result is False
