"""Commercial documentary verification boundary tests."""

import hashlib
from dataclasses import replace

import pytest

from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
)
from sp001.contracts.product001_documentary_commitment_reading import (
    Product001DocumentaryCommitmentReadResult,
    Product001DocumentaryCommitmentReadStatus as Status,
)
from sp001.services.product001_commercial_document_verification import (
    CommercialDocumentVerificationRejected,
    Product001CommercialDocumentVerifier,
)
from sp001.services.product001_documentary_commitment_storage import (
    write_product001_documentary_commitment,
)

from test_authenticated_product001_commercial_approval import (
    decision,
)


CONTENT = b"commercial planogram version one"


def matching_decision():
    original = decision()
    identity = replace(
        original.document_identity,
        source_content_digest=replace(
            original.document_identity.source_content_digest,
            value=hashlib.sha256(CONTENT).hexdigest(),
        ),
    )
    return replace(original, document_identity=identity)


def test_published_document_accepted(tmp_path):
    document = matching_decision()
    verifier = Product001CommercialDocumentVerifier(
        storage_root=tmp_path
    )

    from sp001.contracts.product001_documentary_commitment_storage_location import (
        Product001DocumentaryCommitmentStorageLocation,
    )

    key = Product001DocumentaryCommitmentKey(
        organization_id=document.document_scope.organization_id,
        source_identity=document.document_identity,
    )
    location = Product001DocumentaryCommitmentStorageLocation(
        storage_root=tmp_path,
        key=key,
    )
    write_product001_documentary_commitment(
        location=location,
        content=CONTENT,
    )

    assert verifier.verify(decision=document) is None


def test_absent_document_rejected(tmp_path):
    verifier = Product001CommercialDocumentVerifier(
        storage_root=tmp_path
    )
    with pytest.raises(
        CommercialDocumentVerificationRejected
    ) as error:
        verifier.verify(decision=matching_decision())

    assert error.value.status == "ABSENT"


@pytest.mark.parametrize(
    "status",
    [
        Status.CONFLICT,
        Status.INVALID,
        Status.IO_FAILURE,
    ],
)
def test_nonpresent_status_rejected(tmp_path, status):
    def reader(*, location):
        return Product001DocumentaryCommitmentReadResult(
            key=location.key,
            status=status,
        )

    verifier = Product001CommercialDocumentVerifier(
        storage_root=tmp_path,
        reader=reader,
    )

    with pytest.raises(
        CommercialDocumentVerificationRejected
    ) as error:
        verifier.verify(decision=matching_decision())

    assert error.value.status == status.value


def test_wrong_identity_rejected(tmp_path):
    def reader(*, location):
        wrong_key = replace(
            location.key,
            organization_id="different-organization",
        )
        return Product001DocumentaryCommitmentReadResult(
            key=wrong_key,
            status=Status.PRESENT,
            content=CONTENT,
        )

    verifier = Product001CommercialDocumentVerifier(
        storage_root=tmp_path,
        reader=reader,
    )

    with pytest.raises(
        CommercialDocumentVerificationRejected
    ) as error:
        verifier.verify(decision=matching_decision())

    assert error.value.status == "IDENTITY_MISMATCH"


def test_altered_content_rejected(tmp_path):
    def reader(*, location):
        return Product001DocumentaryCommitmentReadResult(
            key=location.key,
            status=Status.PRESENT,
            content=b"altered content",
        )

    verifier = Product001CommercialDocumentVerifier(
        storage_root=tmp_path,
        reader=reader,
    )

    with pytest.raises(
        CommercialDocumentVerificationRejected
    ) as error:
        verifier.verify(decision=matching_decision())

    assert error.value.status == "CONTENT_DIGEST_MISMATCH"


def test_invalid_reader_result_rejected(tmp_path):
    verifier = Product001CommercialDocumentVerifier(
        storage_root=tmp_path,
        reader=lambda *, location: object(),
    )

    with pytest.raises(
        CommercialDocumentVerificationRejected
    ) as error:
        verifier.verify(decision=matching_decision())

    assert error.value.status == "INVALID_READER_RESULT"


def test_invalid_decision_rejected(tmp_path):
    verifier = Product001CommercialDocumentVerifier(
        storage_root=tmp_path
    )
    with pytest.raises(TypeError):
        verifier.verify(decision=object())


def test_invalid_reader_rejected(tmp_path):
    with pytest.raises(TypeError):
        Product001CommercialDocumentVerifier(
            storage_root=tmp_path,
            reader=object(),
        )
