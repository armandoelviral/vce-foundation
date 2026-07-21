from pathlib import Path

MODEL = Path(
    "research/specification_runtime/"
    "RUNTIME_ORCHESTRATION_MODEL.md"
)


def text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized() -> str:
    return " ".join(
        text().split()
    )


def test_model_exists() -> None:
    assert MODEL.is_file()


def test_runtime_components_exist() -> None:
    content = text()

    for component in (
        "Specification Runtime.",
        "Execution Planner.",
        "Execution Engine.",
        "Evidence Collector.",
    ):
        assert component in content


def test_runtime_responsibilities_exist() -> None:
    content = normalized()

    for responsibility in (
        "Coordinate execution.",
        "Delegate planning.",
        "Delegate execution.",
        "Delegate evidence collection.",
        "Produce one Execution Result.",
    ):
        assert responsibility in content


def test_execution_planner_definition() -> None:
    content = normalized()

    assert (
        "Transform one Specification into executable Execution Units."
        in content
    )


def test_execution_engine_definition() -> None:
    content = normalized()

    assert (
        "Execute every Execution Unit."
        in content
    )

    assert (
        "Produce deterministic execution decisions."
        in content
    )


def test_evidence_collector_definition() -> None:
    content = normalized()

    assert (
        "Collect execution evidence."
        in content
    )

    assert (
        "Produce deterministic evidence records."
        in content
    )


def test_execution_flow_exists() -> None:
    content = text()

    for item in (
        "Specification",
        "Execution Planner",
        "Execution Units",
        "Execution Engine",
        "Evidence Collector",
        "Execution Result",
    ):
        assert item in content


def test_runtime_constraints_exist() -> None:
    content = normalized()

    assert (
        "The Runtime shall remain an orchestrator."
        in content
    )

    assert (
        "Planning shall not execute Claims."
        in content
    )

    assert (
        "Execution shall not collect Evidence."
        in content
    )

    assert (
        "Evidence Collection shall not evaluate Claims."
        in content
    )


def test_runtime_invariants_exist() -> None:
    content = text()

    for invariant in (
        "Execution Determinism",
        "Evidence Completeness",
        "Verification Closure",
        "Behavior Preservation",
    ):
        assert invariant in content


def test_release_criteria_exist() -> None:
    content = normalized()

    assert "Release Criteria" in content

    for item in (
        "Responsibilities are explicitly separated.",
        "Execution flow is explicitly defined.",
        "Observable Runtime behavior is preserved.",
    ):
        assert item in content
