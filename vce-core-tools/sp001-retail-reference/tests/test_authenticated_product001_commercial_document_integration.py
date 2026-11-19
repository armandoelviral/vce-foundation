"""Authenticated commercial approval with documentary verification."""

from dataclasses import replace

import pytest

from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
)
from sp001.contracts.product001_documentary_commitment_storage_location import (
    Product001DocumentaryCommitmentStorageLocation,
)
from sp001.infrastructure.sqlite_product001_commercial_approval import (
    SqliteProduct001CommercialApproval,
)
from sp001.infrastructure.sqlite_product001_commercial_decisions import (
    SqliteProduct001CommercialDecisionWriter,
)
from sp001.services.authenticated_product001_commercial_approval import (
    AuthenticatedProduct001CommercialApproval,
)
from sp001.services.product001_commercial_document_verification import (
    CommercialDocumentVerificationRejected,
    Product001CommercialDocumentVerifier,
)
from sp001.services.product001_documentary_commitment_storage import (
    write_product001_documentary_commitment,
)

from test_authenticated_product001_commercial_approval import (
    StubAuthenticator,
    context,
    grant,
)
from test_product001_commercial_document_verification import (
    CONTENT,
    matching_decision,
)


def build_environment(tmp_path, *, verifier=None):
    (tmp_path / "documents").mkdir(exist_ok=True)
    database = tmp_path / "commercial.sqlite"
    grants = SqliteProduct001CommercialApproval(
        database_path=database
    )
    grants.register_grant(event_id="g1", grant=grant())

    writer = SqliteProduct001CommercialDecisionWriter(
        database_path=database,
        clock=lambda: 150,
    )
    if verifier is None:
        verifier = Product001CommercialDocumentVerifier(
            storage_root=tmp_path / "documents"
        )

    service = AuthenticatedProduct001CommercialApproval(
        authenticator=StubAuthenticator(context()),
        writer=writer,
        document_verifier=verifier,
        expected_audience="commercial",
        clock=lambda: 150,
    )
    return database, service


def publish(tmp_path, document):
    (tmp_path / "documents").mkdir(exist_ok=True)
    key = Product001DocumentaryCommitmentKey(
        organization_id=document.document_scope.organization_id,
        source_identity=document.document_identity,
    )
    location = Product001DocumentaryCommitmentStorageLocation(
        storage_root=tmp_path / "documents",
        key=key,
    )
    write_product001_documentary_commitment(
        location=location,
        content=CONTENT,
    )


def decision_counts(database):
    import sqlite3

    with sqlite3.connect(database) as connection:
        decisions = connection.execute(
            "SELECT COUNT(*) FROM product001_commercial_decisions"
        ).fetchone()[0]
        audit = connection.execute(
            "SELECT COUNT(*) FROM product001_commercial_decision_audit"
        ).fetchone()[0]
    return decisions, audit


def test_published_document_persists_decision_and_audit(tmp_path):
    document = matching_decision()
    publish(tmp_path, document)
    database, service = build_environment(tmp_path)

    assert service.record(
        credential="valid", decision=document
    ) is True
    assert decision_counts(database) == (1, 1)


def test_absent_document_persists_nothing(tmp_path):
    database, service = build_environment(tmp_path)

    with pytest.raises(
        CommercialDocumentVerificationRejected
    ) as error:
        service.record(
            credential="valid",
            decision=matching_decision(),
        )

    assert error.value.status == "ABSENT"
    assert decision_counts(database) == (0, 0)


def test_document_rejected_inside_transaction_rolls_back(tmp_path):
    document = matching_decision()
    calls = [0]

    class ChangingVerifier:
        def verify(self, *, decision):
            calls[0] += 1
            if calls[0] == 2:
                raise CommercialDocumentVerificationRejected(
                    "INVALID"
                )

    database, service = build_environment(
        tmp_path, verifier=ChangingVerifier()
    )

    with pytest.raises(
        CommercialDocumentVerificationRejected
    ) as error:
        service.record(
            credential="valid", decision=document
        )

    assert error.value.status == "INVALID"
    assert calls[0] == 2
    assert decision_counts(database) == (0, 0)


def test_idempotent_replay_reverifies_document(tmp_path):
    document = matching_decision()
    publish(tmp_path, document)

    class CountingVerifier:
        def __init__(self):
            self.calls = 0
            self.delegate = Product001CommercialDocumentVerifier(
                storage_root=tmp_path / "documents"
            )

        def verify(self, *, decision):
            self.calls += 1
            self.delegate.verify(decision=decision)

    verifier = CountingVerifier()
    database, service = build_environment(
        tmp_path, verifier=verifier
    )

    assert service.record(
        credential="valid", decision=document
    ) is True
    assert service.record(
        credential="valid", decision=document
    ) is False

    assert verifier.calls == 4
    assert decision_counts(database) == (1, 1)



@pytest.mark.parametrize(
    "status",
    ["CONFLICT", "INVALID", "IO_FAILURE"],
)
def test_nonpresent_document_status_blocks_persistence(
    tmp_path, status
):
    class RejectingVerifier:
        def verify(self, *, decision):
            raise CommercialDocumentVerificationRejected(status)

    database, service = build_environment(
        tmp_path, verifier=RejectingVerifier()
    )

    with pytest.raises(
        CommercialDocumentVerificationRejected
    ) as error:
        service.record(
            credential="valid",
            decision=matching_decision(),
        )

    assert error.value.status == status
    assert decision_counts(database) == (0, 0)


def test_replay_rejected_when_document_becomes_invalid(tmp_path):
    document = matching_decision()
    publish(tmp_path, document)

    class StatefulVerifier:
        def __init__(self):
            self.calls = 0
            self.delegate = Product001CommercialDocumentVerifier(
                storage_root=tmp_path / "documents"
            )

        def verify(self, *, decision):
            self.calls += 1
            if self.calls == 4:
                raise CommercialDocumentVerificationRejected(
                    "INVALID"
                )
            self.delegate.verify(decision=decision)

    verifier = StatefulVerifier()
    database, service = build_environment(
        tmp_path, verifier=verifier
    )

    assert service.record(
        credential="valid", decision=document
    ) is True

    with pytest.raises(
        CommercialDocumentVerificationRejected
    ):
        service.record(
            credential="valid", decision=document
        )

    assert verifier.calls == 4
    assert decision_counts(database) == (1, 1)


def test_document_identity_mismatch_blocks_persistence(tmp_path):
    document = matching_decision()

    class WrongIdentityVerifier:
        def verify(self, *, decision):
            raise CommercialDocumentVerificationRejected(
                "IDENTITY_MISMATCH"
            )

    database, service = build_environment(
        tmp_path, verifier=WrongIdentityVerifier()
    )

    with pytest.raises(
        CommercialDocumentVerificationRejected
    ) as error:
        service.record(
            credential="valid", decision=document
        )

    assert error.value.status == "IDENTITY_MISMATCH"
    assert decision_counts(database) == (0, 0)


def test_content_digest_mismatch_blocks_persistence(tmp_path):
    document = matching_decision()

    class WrongDigestVerifier:
        def verify(self, *, decision):
            raise CommercialDocumentVerificationRejected(
                "CONTENT_DIGEST_MISMATCH"
            )

    database, service = build_environment(
        tmp_path, verifier=WrongDigestVerifier()
    )

    with pytest.raises(
        CommercialDocumentVerificationRejected
    ) as error:
        service.record(
            credential="valid", decision=document
        )

    assert error.value.status == "CONTENT_DIGEST_MISMATCH"
    assert decision_counts(database) == (0, 0)


def test_corrupted_published_artifact_blocks_approval(tmp_path):
    document = matching_decision()
    publish(tmp_path, document)

    key = Product001DocumentaryCommitmentKey(
        organization_id=document.document_scope.organization_id,
        source_identity=document.document_identity,
    )
    location = Product001DocumentaryCommitmentStorageLocation(
        storage_root=tmp_path / "documents",
        key=key,
    )

    # Deliberately corrupt the published artifact in the test sandbox.
    location.artifact_path.write_bytes(b"corrupted artifact")

    database, service = build_environment(tmp_path)

    with pytest.raises(
        CommercialDocumentVerificationRejected
    ) as error:
        service.record(
            credential="valid",
            decision=document,
        )

    assert error.value.status != "ABSENT"
    assert decision_counts(database) == (0, 0)

def test_invalid_verifier_rejected_at_construction(tmp_path):
    with pytest.raises(TypeError):
        build_environment(
            tmp_path, verifier=object()
        )
