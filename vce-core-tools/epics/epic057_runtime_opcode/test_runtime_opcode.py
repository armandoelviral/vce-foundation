from epics.epic057_runtime_opcode.runtime_opcode import (
    RuntimeOpcode,
)


def test_runtime_opcode_stores_name_and_payload():

    opcode = RuntimeOpcode(
        name="SEAL_SNAPSHOT",
        payload={
            "sequence": 42,
        },
    )

    assert opcode.name == "SEAL_SNAPSHOT"

    assert opcode.payload == {
        "sequence": 42,
    }
