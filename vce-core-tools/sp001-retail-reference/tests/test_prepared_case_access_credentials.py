from dataclasses import replace
import os

import jwt
import pytest
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.asymmetric import rsa

from test_sqlite_case_access_issuance_preparations import setup
from sp001.infrastructure.prepared_case_access_credentials import (
    PreparedCaseAccessSigner, PreparedCredentialProtector,
)


@pytest.fixture(scope="module")
def key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def signer(key):
    return PreparedCaseAccessSigner(
        signing_key_id="KEY-1", private_key=key, issuer="access", audience="coordinator",
    )


def test_signature_and_claims_match_exact_preparation(tmp_path, key):
    _, _, _, _, preparation = setup(tmp_path)
    token = signer(key).sign(preparation=preparation)
    # Fixture uses synthetic timestamps; only temporal checks are disabled here.
    claims = jwt.decode(
        token.credential, key.public_key(), algorithms=["RS256"],
        issuer="access", audience="coordinator",
        options={"verify_exp": False, "verify_iat": False, "verify_nbf": False},
    )
    assert claims == preparation.payload.to_claims()
    assert jwt.get_unverified_header(token.credential) == {
        "alg": "RS256", "kid": "KEY-1", "typ": "at+jwt",
    }


@pytest.mark.parametrize("change", ["key", "issuer", "audience"])
def test_signer_rejects_configuration_mismatch(tmp_path, key, change):
    _, _, _, _, preparation = setup(tmp_path)
    if change == "key":
        preparation = replace(preparation, signing_key_id="OTHER")
    else:
        preparation = replace(
            preparation, payload=replace(preparation.payload, **{change: "OTHER"}),
        )
    with pytest.raises(ValueError):
        signer(key).sign(preparation=preparation)


def test_protection_recovers_exact_token_without_plaintext_in_envelope(tmp_path, key):
    _, _, _, _, preparation = setup(tmp_path)
    token = signer(key).sign(preparation=preparation)
    protector = PreparedCredentialProtector(protection_key_id="PROTECT-1", key=os.urandom(32))
    protected = protector.protect(preparation=preparation, token=token)
    assert token.credential.encode() not in protected.ciphertext
    assert token.credential not in repr(protected)
    assert protector.recover(preparation=preparation, protected=protected) == token


@pytest.mark.parametrize("change", ["request", "key", "binding_revision"])
def test_protected_token_cannot_be_moved_to_different_preparation(tmp_path, key, change):
    _, _, _, _, preparation = setup(tmp_path)
    protector = PreparedCredentialProtector(protection_key_id="PROTECT-1", key=os.urandom(32))
    protected = protector.protect(
        preparation=preparation, token=signer(key).sign(preparation=preparation),
    )
    if change == "request":
        changed = replace(preparation, request_id="OTHER")
    elif change == "key":
        changed = replace(preparation, signing_key_id="OTHER")
    else:
        changed = replace(preparation, binding=replace(preparation.binding, revision=2))
    with pytest.raises(InvalidTag):
        protector.recover(preparation=changed, protected=protected)


def test_ciphertext_tampering_is_rejected(tmp_path, key):
    _, _, _, _, preparation = setup(tmp_path)
    protector = PreparedCredentialProtector(protection_key_id="PROTECT-1", key=os.urandom(32))
    protected = protector.protect(
        preparation=preparation, token=signer(key).sign(preparation=preparation),
    )
    damaged = replace(
        protected,
        ciphertext=bytes([protected.ciphertext[0] ^ 1]) + protected.ciphertext[1:],
    )
    with pytest.raises(InvalidTag):
        protector.recover(preparation=preparation, protected=damaged)
