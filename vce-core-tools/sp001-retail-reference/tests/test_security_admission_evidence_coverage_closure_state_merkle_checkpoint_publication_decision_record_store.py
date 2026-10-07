import inspect
from typing import Protocol

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    create_record,
)


DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
DecisionRecordStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore
)


class CompleteStore:
    def __init__(self) -> None:
        self.records: dict[str, DecisionRecord] = {}

    def read(
        self,
        *,
        publication_id: str,
    ) -> DecisionRecord | None:
        return self.records.get(publication_id)

    def create(
        self,
        *,
        decision_record: DecisionRecord,
    ) -> bool:
        publication_id = (
            decision_record
            .publication_intent
            .publication_id
        )
        if publication_id in self.records:
            return False

        self.records[publication_id] = decision_record
        return True


class MissingRead:
    def create(
        self,
        *,
        decision_record: DecisionRecord,
    ) -> bool:
        return True


class MissingCreate:
    def read(
        self,
        *,
        publication_id: str,
    ) -> DecisionRecord | None:
        return None


def test_store_is_protocol() -> None:
    assert issubclass(DecisionRecordStore, Protocol)


def test_store_is_runtime_checkable() -> None:
    assert isinstance(CompleteStore(), DecisionRecordStore)


@pytest.mark.parametrize(
    "value",
    (
        object(),
        MissingRead(),
        MissingCreate(),
    ),
)
def test_incomplete_implementation_is_rejected(
    value: object,
) -> None:
    assert not isinstance(value, DecisionRecordStore)


def test_protocol_defines_exact_public_members() -> None:
    public_names = {
        name
        for name in DecisionRecordStore.__dict__
        if not name.startswith("_")
    }

    assert public_names == {
        "read",
        "create",
    }


def test_read_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        DecisionRecordStore.read
    )

    assert tuple(signature.parameters) == (
        "self",
        "publication_id",
    )
    assert (
        signature.parameters["publication_id"].kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert (
        signature.parameters["publication_id"].annotation
        is str
    )
    assert (
        signature.return_annotation
        == DecisionRecord | None
    )


def test_create_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        DecisionRecordStore.create
    )

    assert tuple(signature.parameters) == (
        "self",
        "decision_record",
    )
    assert (
        signature.parameters["decision_record"].kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert (
        signature.parameters["decision_record"].annotation
        is DecisionRecord
    )
    assert signature.return_annotation is bool


def test_complete_store_can_read_missing_decision() -> None:
    store = CompleteStore()

    assert store.read(
        publication_id="publication-001",
    ) is None


def test_complete_store_can_create_and_read_exact_record() -> None:
    store = CompleteStore()
    record = create_record()

    assert store.create(
        decision_record=record,
    ) is True
    assert store.read(
        publication_id=(
            record
            .publication_intent
            .publication_id
        ),
    ) is record


def test_complete_store_rejects_second_creation() -> None:
    store = CompleteStore()
    record = create_record()

    assert store.create(
        decision_record=record,
    ) is True
    assert store.create(
        decision_record=record,
    ) is False


def test_failed_second_creation_preserves_first_record() -> None:
    store = CompleteStore()
    first = create_record()
    second = create_record()

    assert store.create(
        decision_record=first,
    ) is True
    assert store.create(
        decision_record=second,
    ) is False
    assert store.read(
        publication_id="publication-001",
    ) is first


@pytest.mark.parametrize(
    "forbidden",
    (
        "update",
        "replace",
        "delete",
        "compare_and_swap",
        "commit",
        "abort",
        "prepare",
    ),
)
def test_protocol_exposes_no_mutation_or_effect_method(
    forbidden: str,
) -> None:
    assert not hasattr(
        DecisionRecordStore,
        forbidden,
    )


def test_protocol_defines_no_constructor_state() -> None:
    source = inspect.getsource(DecisionRecordStore)

    assert "def __init__(" not in source


def test_protocol_contains_no_storage_implementation() -> None:
    source = inspect.getsource(DecisionRecordStore).lower()

    for forbidden in (
        "sqlite",
        "database",
        "filesystem",
        "open(",
        "write(",
        "network",
        "http",
        "socket",
    ):
        assert forbidden not in source


def test_protocol_methods_define_no_behavior() -> None:
    assert inspect.getsource(
        DecisionRecordStore.read
    ).strip().endswith("...")
    assert inspect.getsource(
        DecisionRecordStore.create
    ).strip().endswith("...")
