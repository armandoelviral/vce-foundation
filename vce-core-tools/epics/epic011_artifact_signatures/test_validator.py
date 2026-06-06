from cryptography.exceptions import InvalidSignature

from epics.epic011_artifact_signatures.signature_validator import (
    SignatureValidator,
)


class ValidKey:
    def verify(
        self,
        signature,
        payload,
    ):
        return None


class InvalidKey:
    def verify(
        self,
        signature,
        payload,
    ):
        raise InvalidSignature()


def test_accepts_valid_signature():

    validator = SignatureValidator()

    assert validator.validate(
        ValidKey(),
        b"signature",
        b"payload",
    ) is True


def test_rejects_invalid_signature():

    validator = SignatureValidator()

    assert validator.validate(
        InvalidKey(),
        b"signature",
        b"payload",
    ) is False
