"""SIMULATED acceptance, no store visit or independently approved VM document."""
import base64
from contextlib import closing
from hashlib import sha256
from io import BytesIO
import json
import sqlite3
import time
import zipfile

import pytest
from fastapi.testclient import TestClient
from PIL import Image
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys
from test_retail_inspection_observation import observation
from sp001.contracts.case_access_context import CaseAccessOperation as Op, CaseAccessPermission
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_grant_administration import GrantAdministrationAction as Action, GrantAdministrationRecord
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.infrastructure.jwt_case_access_authenticator import JwtCaseAccessAuthenticator
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.infrastructure.retail_beta_inspection import RetailBetaInspection, verify_export, Integrity
from sp001.infrastructure.retail_beta_http_host import create_retail_beta_app
from sp001.infrastructure.observation_operation_http_host import PHOTO_CONTENT_TYPE
from sp001.infrastructure.retail_inspection_observation_serialization import serialize_retail_inspection_observation as serialize


@pytest.fixture
def beta(tmp_path, keys):
    path = tmp_path / 'beta.sqlite3'
    clock = lambda: int(time.time())
    auth = JwtCaseAccessAuthenticator(issuer=jwt_setup.ISSUER, audience=jwt_setup.AUDIENCE,
        public_keys={'KEY-1':keys[0].public_key()}, max_lifetime_seconds=120, max_token_bytes=16384)
    backend = RetailBetaInspection(database_path=path, expected_audience=jwt_setup.AUDIENCE,
                                  clock=clock, authenticator=auth)
    principal = lambda sub: {'issuer':jwt_setup.ISSUER, 'subject':sub}
    document = 'SIMULADO: frontal con etiqueta visible. Comprobar también zona posterior.'
    assignment = {'assignment_id':'ASSIGN-1', 'case_id':'CASE', 'store':'SIMULATED-STORE',
        'corner':'SIMULATED-CORNER', 'simulated':True,
        'inspector':principal('INSPECTOR'), 'supervisor':principal('SUPERVISOR'),
        'standard':{'standard_id':'VM-TEST','revision':1,'document':document,
                    'sha256':sha256(document.encode()).hexdigest(),
                    'criteria':[{'rule_id':r,'criterion_version':1,'statement':s} for r,s in
                                [('FRONT','Etiqueta visible'),('BACK','Zona posterior revisada')]],
                    'approval_reference':'SIMULATED-APPROVAL-1', 'approved_by':principal('SUPERVISOR')}}
    backend.provision(assignment=assignment)
    grants = SqliteCaseAccessGrants(database_path=path)
    for sub, ops in [('INSPECTOR',(Op.SAVE_RETAIL_OBSERVATION,)),('SUPERVISOR',(Op.READ_RETAIL_OBSERVATION,))]:
        for op in ops:
            now=clock()
            grant=CaseAccessGrant(sub+'-'+op.value,AuthenticatedPrincipal(**principal(sub)),CaseAccessPermission('CASE',op),now-5,now+120)
            grants.apply(record=GrantAdministrationRecord('ADD-'+grant.grant_id,grant.principal,Action.GRANT,grant,now))
    def token(sub, ops=None):
        return jwt_setup.token(keys[0],operations=ops or (Op.SAVE_RETAIL_OBSERVATION,Op.READ_RETAIL_OBSERVATION),overrides={'sub':sub})
    app=create_retail_beta_app(backend=backend,authenticator=auth,audience=jwt_setup.AUDIENCE,clock=clock)
    return backend, app, token, path, assignment


def headers(token): return {'Authorization':'Bearer '+token}


def upload(client, token):
    output=BytesIO()
    Image.new('RGB',(8,8),'red').save(output,format='PNG')
    photo=output.getvalue()
    result=client.put('/v1/cases/CASE/inspection-observation-operations/REQUEST',
        headers={**headers(token),'Content-Type':PHOTO_CONTENT_TYPE},json={
        'observation_document':serialize(observation(case_id='CASE')),
        'photo_base64':base64.b64encode(photo).decode()})
    assert result.status_code==200,result.text
    return photo


def submit(client, token, status='INSUFFICIENT_EVIDENCE'):
    return client.post('/v1/retail-beta/submission',headers=headers(token),json={
        'request_id':'REQUEST','outcomes':{
            'FRONT':{'status':'NON_CONFORMANT','rationale':'Etiqueta no visible en foto de prueba'},
            'BACK':{'status':status,'rationale':'La foto no muestra la parte posterior'}}})


def test_simulated_assign_capture_review_decide_recover_export(beta):
    backend,app,token,path,a=beta
    inspector,supervisor=token('INSPECTOR'),token('SUPERVISOR')
    with TestClient(app) as client:
        assert client.get('/v1/retail-beta/dossier',headers=headers(inspector)).json()['assignment']==a
        photo=upload(client,inspector)
        assert submit(client,inspector).status_code==200
        assert submit(client,inspector).status_code==200
        assert client.post('/v1/retail-beta/decision',headers=headers(supervisor),json={
            'action':'REVIEW_ACCEPTED','rationale':'pretend all complete'}).status_code==400
        decision=client.post('/v1/retail-beta/decision',headers=headers(supervisor),json={
            'action':'FOLLOW_UP_REQUIRED','rationale':'Revisar zona posterior y corregir etiqueta'})
        assert decision.status_code==200,decision.text
    # Fresh backend and HTTP client: persisted dossier, not a session cache.
    reopened=RetailBetaInspection(database_path=path,expected_audience=jwt_setup.AUDIENCE,
        clock=lambda:int(time.time()),authenticator=backend.authenticator)
    second=create_retail_beta_app(backend=reopened,authenticator=backend.authenticator,
                                 audience=jwt_setup.AUDIENCE,clock=lambda:int(time.time()))
    with TestClient(second) as client:
        data=client.get('/v1/retail-beta/dossier',headers=headers(supervisor)).json()
        assert data['decision']==decision.json()
        assert data['assignment']['standard']==a['standard']
        response=client.get('/v1/retail-beta/export',headers=headers(supervisor))
        assert response.status_code==200,response.text
        assert verify_export(response.content)==data
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            assert z.read('photo.bin')==photo
            assert sha256(photo).hexdigest()==data['submission']['receipt']['photo_sha256']


@pytest.mark.parametrize('action,sub,method,body',[
    ('dossier','OTHER','get',None),
    ('submission','SUPERVISOR','post',{'request_id':'REQUEST','outcomes':{}}),
    ('decision','INSPECTOR','post',{'action':'FOLLOW_UP_REQUIRED','rationale':'x'}),
    ('export','INSPECTOR','get',None)])
def test_roles_cannot_cross(beta,action,sub,method,body):
    _,app,token,_,_=beta
    with TestClient(app) as client:
        result=getattr(client,method)('/v1/retail-beta/'+action,headers=headers(token(sub)),**({'json':body} if body else {}))
        assert result.status_code==403,result.text


def test_missing_token_and_unsubmitted_decision(beta):
    _,app,token,_,_=beta
    with TestClient(app) as client:
        assert client.get('/v1/retail-beta/dossier').status_code==401
        assert client.post('/v1/retail-beta/decision',headers=headers(token('SUPERVISOR')),
            json={'action':'FOLLOW_UP_REQUIRED','rationale':'x'}).status_code==400


def test_revocation_same_token(beta):
    _,app,token,path,_=beta
    credential=token('SUPERVISOR')
    with TestClient(app) as client:
        assert client.get('/v1/retail-beta/dossier',headers=headers(credential)).status_code==200
        with closing(sqlite3.connect(path)) as db:
            db.execute("UPDATE case_access_grants SET revoked=1 WHERE subject='SUPERVISOR'")
            db.commit()
        assert client.get('/v1/retail-beta/dossier',headers=headers(credential)).status_code==403


def test_standard_and_submission_are_immutable(beta):
    backend,app,token,_,a=beta
    changed=json.loads(json.dumps(a));changed['standard']['revision']=2
    with pytest.raises(ValueError): backend.provision(assignment=changed)
    with TestClient(app) as client:
        upload(client,token('INSPECTOR'))
        assert submit(client,token('INSPECTOR')).status_code==200
        assert submit(client,token('INSPECTOR'),'CONFORMANT').status_code==409


def test_tampered_effect_fails_recovery(beta):
    _,app,token,path,_=beta
    with TestClient(app) as client:
        upload(client,token('INSPECTOR'));assert submit(client,token('INSPECTOR')).status_code==200
        with closing(sqlite3.connect(path)) as db:
            db.execute("UPDATE retail_observation_photos SET content=x'01'");db.commit()
        assert client.get('/v1/retail-beta/dossier',headers=headers(token('SUPERVISOR'))).status_code==503


def test_export_verifier_rejects_modified_member(beta):
    backend,app,token,_,_=beta
    with TestClient(app) as client:
        upload(client,token('INSPECTOR'));submit(client,token('INSPECTOR'))
        backend.decide(credential=token('SUPERVISOR'),action='FOLLOW_UP_REQUIRED',rationale='x')
        original=backend.export(credential=token('SUPERVISOR'))
        output=BytesIO()
        with zipfile.ZipFile(BytesIO(original)) as source,zipfile.ZipFile(output,'w') as dest:
            for name in source.namelist():dest.writestr(name,b'changed' if name=='photo.bin' else source.read(name))
        with pytest.raises(Integrity):verify_export(output.getvalue())


def test_supervisor_can_inspect_submitted_photo_before_decision(beta):
    _, app, token, _, _ = beta
    with TestClient(app) as client:
        image = upload(client, token('INSPECTOR'))
        # Saving alone does not deliver the review to the supervisor.
        assert client.get('/v1/retail-beta/photo', headers=headers(token('SUPERVISOR'))).status_code == 400
        assert submit(client, token('INSPECTOR')).status_code == 200
        response = client.get('/v1/retail-beta/photo', headers=headers(token('SUPERVISOR')))
        assert response.status_code == 200
        assert response.content == image
        assert response.headers['content-type'] == 'image/png'
        assert response.headers['cache-control'] == 'no-store'
        assert client.get('/v1/retail-beta/photo', headers=headers(token('OTHER'))).status_code == 403
        assert client.get('/v1/retail-beta/export', headers=headers(token('SUPERVISOR'))).status_code == 400


def test_expired_and_wrong_case_permissions_are_rejected(beta, keys):
    _, app, _, _, _ = beta
    now = int(time.time())
    expired = jwt_setup.token(keys[0], overrides={
        'sub': 'SUPERVISOR', 'iat': now-90, 'nbf': now-90, 'exp': now-30})
    other_case = jwt_setup.token(keys[0], overrides={'sub':'SUPERVISOR', 'case_permissions':[{'case_id':'OTHER','operation':Op.READ_RETAIL_OBSERVATION.value}]})
    with TestClient(app) as client:
        assert client.get('/v1/retail-beta/dossier', headers=headers(expired)).status_code == 401
        assert client.get('/v1/retail-beta/dossier', headers=headers(other_case)).status_code == 403


def test_missing_criterion_and_changed_decision_are_not_accepted(beta):
    _, app, token, _, _ = beta
    with TestClient(app) as client:
        upload(client, token('INSPECTOR'))
        assert client.post('/v1/retail-beta/submission', headers=headers(token('INSPECTOR')),
            json={'request_id':'REQUEST','outcomes':{}}).status_code == 400
        assert submit(client, token('INSPECTOR')).status_code == 200
        url='/v1/retail-beta/decision'
        body={'action':'FOLLOW_UP_REQUIRED','rationale':'Visita posterior requerida'}
        result=client.post(url,headers=headers(token('SUPERVISOR')),json=body)
        assert result.status_code == 200
        assert client.post(url,headers=headers(token('SUPERVISOR')),json=body).json() == result.json()
        body['rationale']='Otra decisión'
        assert client.post(url,headers=headers(token('SUPERVISOR')),json=body).status_code == 409


def test_expiration_before_commit_rolls_back_submission(beta):
    backend, app, token, path, _ = beta
    credential = token('INSPECTOR')
    with TestClient(app) as client:
        upload(client, credential)
        now = int(time.time())
        instants = iter([now, now + 500])
        backend._clock = lambda: next(instants)
        response = submit(client, credential)
        assert response.status_code == 401
    with closing(sqlite3.connect(path)) as db:
        assert db.execute('SELECT COUNT(*) FROM retail_beta_submission').fetchone()[0] == 0
