import inspect
from typing import get_type_hints

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipant,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)


class CompleteParticipant:
    @property
    def participant_id(self) -> str:
        return "participant-001"

    def prepare(
        self,
        *,
        publication_intent,
    ):
        raise NotImplementedError

    def commit(
        self,
        *,
        publication_id,
    ):
        raise NotImplementedError

    def abort(
        self,
        *,
        publication_id,
    ):
        raise NotImplementedError


class MissingParticipantIdentity:
    def prepare(
        self,
        *,
        publication_intent,
    ):
        raise NotImplementedError

    def commit(
        self,
        *,
        publication_id,
    ):
        raise NotImplementedError

    def abort(
        self,
        *,
        publication_id,
    ):
        raise NotImplementedError


class MissingPrepare:
    participant_id = "participant-001"

    def commit(
        self,
        *,
        publication_id,
    ):
        raise NotImplementedError

    def abort(
        self,
        *,
        publication_id,
    ):
        raise NotImplementedError


class MissingCommit:
    participant_id = "participant-001"

    def prepare(
        self,
        *,
        publication_intent,
    ):
        raise NotImplementedError

    def abort(
        self,
        *,
        publication_id,
    ):
        raise NotImplementedError


class MissingAbort:
    participant_id = "participant-001"

    def prepare(
        self,
        *,
        publication_intent,
    ):
        raise NotImplementedError

    def commit(
        self,
        *,
        publication_id,
    ):
        raise NotImplementedError


def protocol():
    return SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipant


def test_protocol_is_runtime_checkable() -> None:
    assert isinstance(
        CompleteParticipant(),
        protocol(),
    )


@pytest.mark.parametrize(
    "value",
    (
        object(),
        MissingParticipantIdentity(),
        MissingPrepare(),
        MissingCommit(),
        MissingAbort(),
    ),
)
def test_incomplete_implementations_do_not_satisfy_protocol(
    value: object,
) -> None:
    assert not isinstance(
        value,
        protocol(),
    )


def test_protocol_defines_exact_public_surface() -> None:
    public_names = {
        name
        for name in protocol().__dict__
        if not name.startswith("_")
    }

    assert public_names == {
        "participant_id",
        "prepare",
        "commit",
        "abort",
    }


def test_participant_identity_is_read_only_property() -> None:
    descriptor = protocol().__dict__["participant_id"]

    assert isinstance(descriptor, property)
    assert descriptor.fset is None
    assert descriptor.fdel is None


def test_participant_identity_return_type_is_exact() -> None:
    descriptor = protocol().__dict__["participant_id"]
    hints = get_type_hints(descriptor.fget)

    assert hints == {
        "return": str,
    }


def test_prepare_has_exact_keyword_only_surface() -> None:
    signature = inspect.signature(
        protocol().prepare
    )

    assert tuple(signature.parameters) == (
        "self",
        "publication_intent",
    )
    assert (
        signature.parameters[
            "publication_intent"
        ].kind
        is inspect.Parameter.KEYWORD_ONLY
    )


def test_prepare_annotations_are_exact() -> None:
    hints = get_type_hints(protocol().prepare)

    assert hints == {
        "publication_intent": (
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent
        ),
        "return": (
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
        ),
    }


@pytest.mark.parametrize(
    "method_name",
    (
        "commit",
        "abort",
    ),
)
def test_decision_methods_have_exact_keyword_only_surface(
    method_name: str,
) -> None:
    signature = inspect.signature(
        getattr(protocol(), method_name)
    )

    assert tuple(signature.parameters) == (
        "self",
        "publication_id",
    )
    assert (
        signature.parameters[
            "publication_id"
        ].kind
        is inspect.Parameter.KEYWORD_ONLY
    )


@pytest.mark.parametrize(
    "method_name",
    (
        "commit",
        "abort",
    ),
)
def test_decision_method_annotations_are_exact(
    method_name: str,
) -> None:
    hints = get_type_hints(
        getattr(protocol(), method_name)
    )

    assert hints == {
        "publication_id": str,
        "return": (
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
        ),
    }


def test_protocol_defines_no_explicit_constructor() -> None:
    import ast

    tree = ast.parse(
        inspect.getsource(protocol())
    )
    class_definition = next(
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    )
    method_names = {
        node.name
        for node in class_definition.body
        if isinstance(node, ast.FunctionDef)
    }

    assert "__init__" not in method_names


def test_protocol_defines_no_coordinator_behavior() -> None:
    source = inspect.getsource(protocol())

    assert "coordinator" not in source.lower()
    assert "quorum" not in source.lower()
    assert "decision" not in source.lower()


def test_protocol_defines_no_transport_behavior() -> None:
    import sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant as module

    source = inspect.getsource(module)

    for forbidden in (
        "http",
        "grpc",
        "socket",
        "requests",
        "urllib",
    ):
        assert forbidden not in source.lower()


def test_protocol_defines_no_persistence_behavior() -> None:
    import sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant as module

    source = inspect.getsource(module)

    for forbidden in (
        "sqlite",
        "database",
        "commit(",
        "rollback",
        "journal_mode",
    ):
        if forbidden == "commit(":
            assert source.count(forbidden) == 1
        else:
            assert forbidden not in source.lower()


def test_protocol_defines_no_retry_or_timeout_policy() -> None:
    import sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant as module

    source = inspect.getsource(module).lower()

    assert "retry" not in source
    assert "timeout" not in source
    assert "sleep" not in source


def test_protocol_defines_no_signing_capability() -> None:
    import sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant as module

    source = inspect.getsource(module).lower()

    assert "private_key" not in source
    assert "sign(" not in source
    assert "signer" not in source


def test_protocol_defines_no_unsafe_dynamic_execution() -> None:
    import sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant as module

    source = inspect.getsource(module)

    assert "pickle" not in source
    assert "eval(" not in source
    assert "exec(" not in source
