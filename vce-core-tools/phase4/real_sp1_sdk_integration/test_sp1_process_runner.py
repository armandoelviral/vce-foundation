from phase4.real_sp1_sdk_integration.sp1_process_runner import (
    SP1ProcessRunner,
)


def test_runner_stores_command():

    runner = SP1ProcessRunner()

    result = runner.run(
        [
            "sp1",
            "prove",
            "program.elf",
        ]
    )

    assert result["command"] == [
        "sp1",
        "prove",
        "program.elf",
    ]


def test_runner_returns_status():

    runner = SP1ProcessRunner()

    result = runner.run(
        [
            "sp1",
            "prove",
            "program.elf",
        ]
    )

    assert (
        result["status"]
        == "PROCESS_EXECUTED"
    )


def test_runner_returns_exit_code():

    runner = SP1ProcessRunner()

    result = runner.run(
        [
            "sp1",
            "prove",
            "program.elf",
        ]
    )

    assert (
        result["exit_code"]
        == 0
    )


def test_runner_returns_dict():

    runner = SP1ProcessRunner()

    result = runner.run(
        [
            "sp1",
            "prove",
            "program.elf",
        ]
    )

    assert isinstance(
        result,
        dict,
    )
