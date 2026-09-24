import ast
import inspect
from enum import StrEnum

import pytest

from sp001.contracts.security_admission_assessment_status import (
    SecurityAdmissionAssessmentStatus,
)


Status = SecurityAdmissionAssessmentStatus


def test_status_vocabulary_is_exact_and_closed() -> None:
    assert tuple(Status) == (
        Status.SATISFIED,
        Status.NOT_SATISFIED,
        Status.INDETERMINATE,
    )
    assert tuple(status.value for status in Status) == (
        "SATISFIED",
        "NOT_SATISFIED",
        "INDETERMINATE",
    )


def test_status_is_string_enum() -> None:
    assert issubclass(Status, StrEnum)


@pytest.mark.parametrize(
    "status",
    (
        Status.SATISFIED,
        Status.NOT_SATISFIED,
        Status.INDETERMINATE,
    ),
)
def test_each_status_preserves_exact_string_value(
    status: Status,
) -> None:
    assert str(status) == status.value
    assert Status(status.value) is status


@pytest.mark.parametrize(
    "invalid_value",
    (
        "RESOLVED",
        "IMPEDED",
        "NOT_EVALUATED",
        "REJECTED",
        "ADMITTED",
        "AUTHORIZED",
    ),
)
def test_nonassessment_states_are_not_members(
    invalid_value: str,
) -> None:
    with pytest.raises(ValueError):
        Status(invalid_value)


def test_closure_states_are_absent() -> None:
    assert not hasattr(Status, "RESOLVED")
    assert not hasattr(Status, "IMPEDED")
    assert not hasattr(Status, "NOT_EVALUATED")


def test_decision_states_are_absent() -> None:
    assert not hasattr(Status, "REJECTED")
    assert not hasattr(Status, "ADMITTED")
    assert not hasattr(Status, "AUTHORIZED")


def test_status_defines_no_implicit_precedence() -> None:
    assert not hasattr(Status, "rank")
    assert not hasattr(Status, "precedence")
    assert not hasattr(Status, "priority")


def test_module_defines_no_aggregation_or_decision_function() -> None:
    module = inspect.getmodule(Status)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    assert functions == []


def test_contract_imports_only_enum() -> None:
    module = inspect.getmodule(Status)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"enum"}
