import inspect

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore,
)


Confirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation
)
ConfirmationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet
)
ConfirmationStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore
)


class CompleteStore:
    def read(
        self,
        *,
        publication_id: str,
    ) -> ConfirmationSet:
        return ConfirmationSet(
            confirmations=(),
        )

    def create(
        self,
        *,
        confirmation: Confirmation,
    ) -> bool:
        return True


class MissingRead:
    def create(
        self,
        *,
        confirmation: Confirmation,
    ) -> bool:
        return True


class MissingCreate:
    def read(
        self,
        *,
        publication_id: str,
    ) -> ConfirmationSet:
        return ConfirmationSet(
            confirmations=(),
        )


def protocol():
    return ConfirmationStore


def test_protocol_is_runtime_checkable() -> None:
    assert isinstance(
        CompleteStore(),
        ConfirmationStore,
    )


def test_missing_read_does_not_implement_protocol() -> None:
    assert not isinstance(
        MissingRead(),
        ConfirmationStore,
    )


def test_missing_create_does_not_implement_protocol() -> None:
    assert not isinstance(
        MissingCreate(),
        ConfirmationStore,
    )


def test_protocol_defines_exact_public_surface() -> None:
    public_members = {
        name
        for name in protocol().__dict__
        if not name.startswith("_")
    }

    assert public_members == {
        "read",
        "create",
    }


def test_read_has_exact_keyword_only_surface() -> None:
    signature = inspect.signature(
        protocol().read
    )

    assert tuple(signature.parameters) == (
        "self",
        "publication_id",
    )
    assert (
        signature.parameters["publication_id"].kind
        is inspect.Parameter.KEYWORD_ONLY
    )


def test_read_annotations_are_exact() -> None:
    signature = inspect.signature(
        protocol().read
    )

    assert (
        signature.parameters["publication_id"].annotation
        is str
    )
    assert (
        signature.return_annotation
        is ConfirmationSet
    )


def test_create_has_exact_keyword_only_surface() -> None:
    signature = inspect.signature(
        protocol().create
    )

    assert tuple(signature.parameters) == (
        "self",
        "confirmation",
    )
    assert (
        signature.parameters["confirmation"].kind
        is inspect.Parameter.KEYWORD_ONLY
    )


def test_create_annotations_are_exact() -> None:
    signature = inspect.signature(
        protocol().create
    )

    assert (
        signature.parameters["confirmation"].annotation
        is Confirmation
    )
    assert signature.return_annotation is bool


def test_protocol_defines_no_explicit_constructor() -> None:
    source = inspect.getsource(
        protocol()
    )

    assert "def __init__(" not in source


def test_protocol_exposes_no_update() -> None:
    assert "update" not in protocol().__dict__


def test_protocol_exposes_no_delete() -> None:
    assert "delete" not in protocol().__dict__


def test_protocol_exposes_no_compare_and_swap() -> None:
    assert "compare_and_swap" not in protocol().__dict__


def test_protocol_exposes_no_bulk_replacement() -> None:
    members = set(protocol().__dict__)

    assert members.isdisjoint(
        {
            "replace",
            "set",
            "write",
            "upsert",
        }
    )


def test_protocol_defines_no_participant_effects() -> None:
    members = set(protocol().__dict__)

    assert members.isdisjoint(
        {
            "prepare",
            "commit",
            "abort",
            "apply",
            "coordinate",
        }
    )


def test_protocol_defines_no_decision_authority() -> None:
    members = set(protocol().__dict__)

    assert members.isdisjoint(
        {
            "derive",
            "decide",
            "verify",
            "authorize",
        }
    )


def test_protocol_defines_no_retry_policy() -> None:
    source = inspect.getsource(
        protocol()
    ).lower()

    assert "retry" not in source
    assert "backoff" not in source
    assert "timeout" not in source


def test_protocol_defines_no_sqlite_policy() -> None:
    source = inspect.getsource(
        protocol()
    ).lower()

    assert "sqlite" not in source
    assert "database" not in source
    assert "transaction" not in source


def test_read_contract_returns_canonical_set_not_none() -> None:
    signature = inspect.signature(
        protocol().read
    )

    assert signature.return_annotation is ConfirmationSet
    assert "None" not in str(
        signature.return_annotation
    )


def test_create_contract_is_append_once_boolean() -> None:
    source = inspect.getsource(
        protocol().create
    )

    assert "Append once" in source
    assert "False" in source


def test_protocol_defines_no_dynamic_execution() -> None:
    module = inspect.getmodule(
        protocol()
    )
    assert module is not None

    source = inspect.getsource(module)

    assert "subprocess" not in source
    assert "eval(" not in source
    assert "exec(" not in source
    assert "__import__" not in source
