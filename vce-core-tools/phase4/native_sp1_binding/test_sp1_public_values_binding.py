from phase4.native_sp1_binding.sp1_public_values_binding import (
    SP1PublicValuesBinding,
)


def test_contains_did():

    binding = SP1PublicValuesBinding(
        tcu_did="did:tcn:test:01",
        public_values={
            "n": 1,
            "a": 1,
            "b": 1,
        },
    )

    assert binding.tcu_did == (
        "did:tcn:test:01"
    )


def test_contains_public_values():

    binding = SP1PublicValuesBinding(
        tcu_did="did:tcn:test:01",
        public_values={
            "n": 1,
            "a": 1,
            "b": 1,
        },
    )

    assert binding.public_values["n"] == 1
    assert binding.public_values["a"] == 1
    assert binding.public_values["b"] == 1


def test_serializes():

    binding = SP1PublicValuesBinding(
        tcu_did="did:tcn:test:01",
        public_values={
            "n": 1,
            "a": 1,
            "b": 1,
        },
    )

    assert binding.to_dict() == {
        "tcu_did": "did:tcn:test:01",
        "public_values": {
            "n": 1,
            "a": 1,
            "b": 1,
        },
    }
