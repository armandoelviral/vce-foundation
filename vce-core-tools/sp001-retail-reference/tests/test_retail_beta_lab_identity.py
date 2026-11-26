"""Local simulation recovery does not rewrite an existing business dossier."""
from contextlib import closing
from copy import deepcopy
from pathlib import Path
import socket
import sqlite3
import time

import jwt
import pytest
from fastapi.testclient import TestClient
from cryptography.hazmat.primitives import serialization

from test_retail_beta_inspection import beta, keys, upload, submit, headers
from sp001.infrastructure.retail_beta_lab_identity import (
    prepare_identity, business_digest, ISSUER, AUDIENCE,
)
from sp001.infrastructure.retail_beta_http_host import create_retail_beta_app


@pytest.fixture
def lab(tmp_path, beta):
    assignment = deepcopy(beta[-1])
    for role in ('inspector','supervisor'):
        assignment[role]['issuer'] = ISSUER
    assignment['standard']['approved_by']['issuer'] = ISSUER
    root = tmp_path/'lab';root.mkdir(mode=0o700)
    clock = lambda:int(time.time())
    backend, auth, event = prepare_identity(root=root,resume=False,adopt_legacy=False,
                                           clock=clock,assignment=assignment)
    app = create_retail_beta_app(backend=backend,authenticator=auth,audience=AUDIENCE,clock=clock)
    with TestClient(app) as client:
        upload(client,(root/'inspector.txt').read_text())
        assert submit(client,(root/'inspector.txt').read_text()).status_code == 200
    return root, assignment, clock, event


def test_resume_preserves_key_and_entire_dossier_then_decides_and_exports(lab):
    root, assignment, clock, first = lab
    before = business_digest(root/'beta.sqlite3')
    original_key = (root/'lab-signing-key.pem').read_bytes()
    backend, auth, resumed = prepare_identity(root=root,resume=True,adopt_legacy=False,
                                             clock=clock,assignment=assignment)
    assert original_key == (root/'lab-signing-key.pem').read_bytes()
    assert resumed['public_key_sha256'] == first['public_key_sha256']
    assert before == business_digest(root/'beta.sqlite3')
    assert business_digest(Path(resumed['backup'])) == before
    credential = (root/'supervisor.txt').read_text()
    data = backend.recover(credential=credential)
    assert data['submission']['outcomes']['BACK']['status'] == 'INSUFFICIENT_EVIDENCE'
    assert data['decision'] is None
    backend.decide(credential=credential,action='FOLLOW_UP_REQUIRED',rationale='Seguimiento simulado')
    assert backend.export(credential=credential).startswith(b'PK')
    for name in ('inspector.txt','supervisor.txt','lab-signing-key.pem'):
        assert (root/name).stat().st_mode & 0o777 == 0o600


def test_legacy_requires_explicit_adoption_and_changes_only_local_trust(lab):
    root, assignment, clock, first = lab
    (root/'lab-signing-key.pem').unlink()
    before = business_digest(root/'beta.sqlite3')
    with pytest.raises(ValueError,match='adopt-legacy-lab'):
        prepare_identity(root=root,resume=True,adopt_legacy=False,clock=clock,assignment=assignment)
    assert not (root/'lab-signing-key.pem').exists()
    backend, _, event = prepare_identity(root=root,resume=True,adopt_legacy=True,
                                         clock=clock,assignment=assignment)
    assert event['action'] == 'LEGACY_KEY_ADOPTED'
    assert event['public_key_sha256'] != first['public_key_sha256']
    assert before == business_digest(root/'beta.sqlite3')
    assert backend.recover(credential=(root/'supervisor.txt').read_text())['submission'] is not None


def test_expired_tokens_remain_rejected_after_resume(lab):
    root, assignment, clock, _ = lab
    key = serialization.load_pem_private_key((root/'lab-signing-key.pem').read_bytes(),password=None)
    claims = jwt.decode((root/'supervisor.txt').read_text(),options={'verify_signature':False})
    now = clock();claims.update(iat=now-7200,nbf=now-7200,exp=now-3601)
    expired = jwt.encode(claims,key,algorithm='RS256',headers={'kid':'BETA','typ':'at+jwt'})
    _, auth, _ = prepare_identity(root=root,resume=True,adopt_legacy=False,clock=clock,assignment=assignment)
    assert auth.authenticate(credential=expired) is None
    assert auth.authenticate(credential=(root/'supervisor.txt').read_text()) is not None


@pytest.mark.parametrize('fault',['revoked','changed_standard','missing_database','public_key_permissions','replaced_key'])
def test_resume_fails_closed_without_changing_business(lab,fault):
    root, assignment, clock, _ = lab
    path=root/'beta.sqlite3'
    if fault=='revoked':
        with closing(sqlite3.connect(path)) as db:
            db.execute('UPDATE case_access_grants SET revoked=1');db.commit()
    elif fault=='changed_standard':
        assignment=deepcopy(assignment);assignment['standard']['revision']=2
    elif fault=='missing_database':
        path=root/'missing'/'beta.sqlite3';root=root/'missing';root.mkdir(mode=0o700)
    elif fault=='public_key_permissions':
        (root/'lab-signing-key.pem').chmod(0o644)
    else:
        from cryptography.hazmat.primitives.asymmetric import rsa
        replacement=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        (root/'lab-signing-key.pem').write_bytes(replacement.private_bytes(
            serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
    before=business_digest(path) if path.exists() else None
    with pytest.raises((ValueError,FileNotFoundError)):
        prepare_identity(root=root,resume=True,adopt_legacy=False,clock=clock,assignment=assignment)
    if before is not None:assert business_digest(path)==before
    else:assert not path.exists()


def test_occupied_port_stops_before_renewal(lab, monkeypatch):
    from sp001.infrastructure.retail_beta_lab import main
    root, _, _, _ = lab
    events=set(root.glob('lab-event-*'))
    token=(root/'supervisor.txt').read_bytes()
    with socket.socket() as listener:
        listener.bind(('127.0.0.1',0));listener.listen()
        monkeypatch.setattr('sys.argv',['retail_beta_lab','--resume',str(root),'--port',str(listener.getsockname()[1])])
        with pytest.raises(OSError):main()
    assert set(root.glob('lab-event-*'))==events
    assert (root/'supervisor.txt').read_bytes()==token
