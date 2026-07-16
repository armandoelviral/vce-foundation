from pathlib import Path


RELEASE_GATES = Path(
    "research/specifications/RELEASE_GATES.md"
)

INVARIANT_GATE_COMMAND = (
    "python -m pytest tests/runtime/invariants -q"
)

RUNTIME_GATE_COMMAND = (
    "python -m pytest tests/runtime -q"
)


def release_gates_text() -> str:
    return RELEASE_GATES.read_text(
        encoding="utf-8",
    )


def test_release_gates_document_exists() -> None:
    assert RELEASE_GATES.is_file()


def test_defines_runtime_invariant_gate() -> None:
    text = release_gates_text()

    assert "Runtime Invariant Gate" in text
    assert INVARIANT_GATE_COMMAND in text


def test_defines_runtime_gate() -> None:
    text = release_gates_text()

    assert "Runtime Gate" in text
    assert RUNTIME_GATE_COMMAND in text


def test_defines_exactly_two_official_pytest_commands() -> None:
    text = release_gates_text()

    commands = tuple(
        line.strip()
        for line in text.splitlines()
        if line.strip().startswith("python -m pytest")
    )

    assert commands == (
        INVARIANT_GATE_COMMAND,
        RUNTIME_GATE_COMMAND,
    )
