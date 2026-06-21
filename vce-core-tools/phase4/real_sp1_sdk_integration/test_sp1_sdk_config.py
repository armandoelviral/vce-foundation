from phase4.real_sp1_sdk_integration.sp1_sdk_config import (
    SP1SDKConfig,
)


def test_contains_sdk_path():

    config = SP1SDKConfig(
        sdk_path="sp1",
        elf_path="program.elf",
        prover_mode="local",
    )

    assert config.sdk_path == "sp1"


def test_contains_elf_path():

    config = SP1SDKConfig(
        sdk_path="sp1",
        elf_path="program.elf",
        prover_mode="local",
    )

    assert config.elf_path == "program.elf"


def test_contains_prover_mode():

    config = SP1SDKConfig(
        sdk_path="sp1",
        elf_path="program.elf",
        prover_mode="local",
    )

    assert config.prover_mode == "local"


def test_serializes():

    config = SP1SDKConfig(
        sdk_path="sp1",
        elf_path="program.elf",
        prover_mode="local",
    )

    assert config.to_dict() == {
        "sdk_path": "sp1",
        "elf_path": "program.elf",
        "prover_mode": "local",
    }
