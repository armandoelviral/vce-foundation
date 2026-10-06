import ast
import inspect
from pathlib import Path
from typing import get_type_hints

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateStore,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    create_state,
)


PublicationState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
)
StateStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateStore
)


class CompleteStateStore:
    def read(
        self,
        *,
        publication_id: str,
    ) -> PublicationState | None:
        return None

    def create(
        self,
        *,
        state: PublicationState,
    ) -> bool:
        return True

    def compare_and_swap(
        self,
        *,
        expected_revision: int,
        next_state: PublicationState,
    ) -> bool:
        return True


class ConflictStateStore:
    def read(
        self,
        *,
        publication_id: str,
    ) -> PublicationState | None:
        return None

    def create(
        self,
        *,
        state: PublicationState,
    ) -> bool:
        return False

    def compare_and_swap(
        self,
        *,
        expected_revision: int,
        next_state: PublicationState,
    ) -> bool:
        return False


class FailingStateStore:
    def read(
        self,
        *,
        publication_id: str,
    ) -> PublicationState | None:
        raise RuntimeError("backend unavailable")

    def create(
        self,
        *,
        state: PublicationState,
    ) -> bool:
        raise RuntimeError("backend unavailable")

    def compare_and_swap(
        self,
        *,
        expected_revision: int,
        next_state: PublicationState,
    ) -> bool:
        raise RuntimeError("backend unavailable")


class MissingRead:
    def create(
        self,
        *,
        state: PublicationState,
    ) -> bool:
        return True

    def compare_and_swap(
        self,
        *,
        expected_revision: int,
        next_state: PublicationState,
    ) -> bool:
        return True


class MissingCreate:
    def read(
        self,
        *,
        publication_id: str,
    ) -> PublicationState | None:
        return None

    def compare_and_swap(
        self,
        *,
        expected_revision: int,
        next_state: PublicationState,
    ) -> bool:
        return True


class MissingCompareAndSwap:
    def read(
        self,
        *,
        publication_id: str,
    ) -> PublicationState | None:
        return None

    def create(
        self,
        *,
        state: PublicationState,
    ) -> bool:
        return True


def test_state_store_is_runtime_checkable_protocol() -> None:
    assert StateStore._is_protocol
    assert StateStore._is_runtime_protocol


def test_complete_structural_implementation_is_accepted() -> None:
    assert isinstance(CompleteStateStore(), StateStore)


@pytest.mark.parametrize(
    "incomplete",
    (
        MissingRead(),
        MissingCreate(),
        MissingCompareAndSwap(),
        object(),
    ),
)
def test_incomplete_structural_implementation_is_rejected(
    incomplete: object,
) -> None:
    assert not isinstance(incomplete, StateStore)


def test_protocol_has_exact_public_operations() -> None:
    public_names = {
        name
        for name in vars(StateStore)
        if not name.startswith("_")
    }

    assert public_names == {
        "read",
        "create",
        "compare_and_swap",
    }


@pytest.mark.parametrize(
    "method_name,parameter_names",
    (
        (
            "read",
            (
                "self",
                "publication_id",
            ),
        ),
        (
            "create",
            (
                "self",
                "state",
            ),
        ),
        (
            "compare_and_swap",
            (
                "self",
                "expected_revision",
                "next_state",
            ),
        ),
    ),
)
def test_operations_have_exact_parameters(
    method_name: str,
    parameter_names: tuple[str, ...],
) -> None:
    signature = inspect.signature(
        getattr(StateStore, method_name)
    )

    assert tuple(signature.parameters) == parameter_names


@pytest.mark.parametrize(
    "method_name",
    (
        "read",
        "create",
        "compare_and_swap",
    ),
)
def test_operation_inputs_are_keyword_only(
    method_name: str,
) -> None:
    parameters = tuple(
        inspect.signature(
            getattr(StateStore, method_name)
        ).parameters.values()
    )

    assert (
        parameters[0].kind
        is inspect.Parameter.POSITIONAL_OR_KEYWORD
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in parameters[1:]
    )


def test_read_has_exact_type_contract() -> None:
    hints = get_type_hints(StateStore.read)

    assert hints == {
        "publication_id": str,
        "return": PublicationState | None,
    }


def test_create_has_exact_type_contract() -> None:
    hints = get_type_hints(StateStore.create)

    assert hints == {
        "state": PublicationState,
        "return": bool,
    }


def test_compare_and_swap_has_exact_type_contract() -> None:
    hints = get_type_hints(StateStore.compare_and_swap)

    assert hints == {
        "expected_revision": int,
        "next_state": PublicationState,
        "return": bool,
    }


def test_read_uses_opaque_publication_identifier() -> None:
    store = CompleteStateStore()

    assert store.read(
        publication_id="tenant://region/publication-001"
    ) is None


def test_create_conflict_is_distinct_false_result() -> None:
    store = ConflictStateStore()

    result = store.create(
        state=create_state(),
    )

    assert result is False


def test_compare_and_swap_conflict_is_distinct_false_result() -> None:
    store = ConflictStateStore()

    result = store.compare_and_swap(
        expected_revision=1,
        next_state=create_state(revision=2),
    )

    assert result is False


@pytest.mark.parametrize(
    "operation",
    (
        "read",
        "create",
        "compare_and_swap",
    ),
)
def test_backend_failure_remains_an_exception(
    operation: str,
) -> None:
    store = FailingStateStore()

    with pytest.raises(
        RuntimeError,
        match="backend unavailable",
    ):
        if operation == "read":
            store.read(publication_id="publication-001")
        elif operation == "create":
            store.create(state=create_state())
        else:
            store.compare_and_swap(
                expected_revision=1,
                next_state=create_state(revision=2),
            )


def test_protocol_is_not_a_concrete_store() -> None:
    with pytest.raises(TypeError):
        StateStore()


def test_protocol_operations_are_synchronous() -> None:
    assert not inspect.iscoroutinefunction(StateStore.read)
    assert not inspect.iscoroutinefunction(StateStore.create)
    assert not inspect.iscoroutinefunction(
        StateStore.compare_and_swap
    )


def test_module_imports_no_storage_backend() -> None:
    module_path = Path(
        "src/sp001/services/"
        "security_admission_evidence_coverage_closure_state_"
        "merkle_checkpoint_publication_state_store.py"
    )
    tree = ast.parse(
        module_path.read_text(encoding="utf-8")
    )

    imported_roots = {
        alias.name.split(".", maxsplit=1)[0]
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_roots.update(
        node.module.split(".", maxsplit=1)[0]
        for node in tree.body
        if (
            isinstance(node, ast.ImportFrom)
            and node.module is not None
        )
    )

    assert imported_roots == {
        "typing",
        "sp001",
    }


@pytest.mark.parametrize(
    "forbidden_term",
    (
        "sqlite",
        "postgres",
        "mysql",
        "redis",
        "dynamodb",
        "firestore",
        "cosmos",
        "wal",
        "transaction",
        "rollback",
        "lock",
        "retry",
    ),
)
def test_protocol_claims_no_concrete_backend_capability(
    forbidden_term: str,
) -> None:
    module_path = Path(
        "src/sp001/services/"
        "security_admission_evidence_coverage_closure_state_"
        "merkle_checkpoint_publication_state_store.py"
    )
    source = module_path.read_text(encoding="utf-8").lower()

    assert forbidden_term not in source
