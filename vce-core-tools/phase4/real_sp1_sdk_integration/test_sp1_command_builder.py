from phase4.real_sp1_sdk_integration.sp1_sdk_config import (
    SP1SDKConfig,
)

from phase4.real_sp1_sdk_integration.sp1_command_builder import (
    SP1CommandBuilder,
)


def test_build_contains_sdk_path():

    config = SP1SDKConfig(
        sdk_path="sp1",
        elf_path="program.elf",
        prover_mode="local",
    )

    builder = SP1CommandBuilder(
        config
    )

    command = builder.build()

    assert command[0] == "sp1"


def test_build_contains_prove():

    config = SP1SDKConfig(
        sdk_path="sp1",
        elf_path="program.elf",
        prover_mode="local",
    )

    builder = SP1CommandBuilder(
        config
    )

    command = builder.build()

    assert "prove" in command


def test_build_contains_elf():

    config = SP1SDKConfig(
        sdk_path="sp1",
        elf_path="program.elf",
        prover_mode="local",
    )

    builder = SP1CommandBuilder(
        config
    )

    command = builder.build()

    assert "program.elf" in command


def test_build_returns_list():

    config = SP1SDKConfig(
        sdk_path="sp1",
        elf_path="program.elf",
        prover_mode="local",
    )

    builder = SP1CommandBuilder(
        config
    )

    command = builder.build()

    assert isinstance(
        command,
        list,
    )
