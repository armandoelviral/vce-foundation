"""Trusted local SIMULATION administration; not an external trust authority.

Legacy adoption deliberately changes the verifier key. It does not authenticate
historical authorship. Business records are backed up and never rewritten here.
"""
from contextlib import closing
from hashlib import sha256
import json
import os
from pathlib import Path
import sqlite3
import stat
import uuid

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from sp001.contracts.case_access_context import CaseAccessOperation as Op, CaseAccessPermission
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_grant_administration import GrantAdministrationAction as Action, GrantAdministrationRecord
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.infrastructure.jwt_case_access_authenticator import JwtCaseAccessAuthenticator
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.infrastructure.retail_beta_inspection import RetailBetaInspection, canonical

ISSUER = 'retail-beta-simulation'
AUDIENCE = 'retail-beta'
BUSINESS_TABLES = ('retail_beta_assignment', 'retail_beta_submission',
                   'retail_beta_decision', 'retail_inspection_observations',
                   'retail_observation_operations', 'retail_observation_photos')


def protected(path, *, directory=False):
    info = path.lstat()
    kind = stat.S_ISDIR if directory else stat.S_ISREG
    if not kind(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError('lab path must be owned by this user and private: ' + str(path))


def write_secret(path, data):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'wb') as output:
        output.write(data)
        output.flush()
        os.fsync(output.fileno())


def business_digest(path):
    with closing(sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)) as db:
        db.execute('BEGIN')
        values = {}
        for table in BUSINESS_TABLES:
            rows = db.execute('SELECT * FROM ' + table).fetchall()
            values[table] = sorted(repr(row) for row in rows)
        return sha256(canonical(values).encode()).hexdigest()


def prepare_identity(*, root, resume, adopt_legacy, clock, assignment):
    """Caller holds an exclusive process lock and the listening socket.

    Explicit resume renews only the two original, non-revoked lab grants.
    No HTTP endpoint invokes this trusted administrative capability.
    """
    root = Path(root)
    if root.is_symlink():
        raise ValueError('lab directory must not be a symlink')
    root = root.resolve()
    protected(root, directory=True)
    path = root / 'beta.sqlite3'
    key_path = root / 'lab-signing-key.pem'
    if resume:
        protected(path)
        with closing(sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)) as db:
            row = db.execute('SELECT document FROM retail_beta_assignment WHERE singleton=1').fetchone()
            if not row or row[0] != canonical(assignment) or assignment['simulated'] is not True:
                raise ValueError('only the exact original simulated assignment can be resumed')
            for role, op in [('INSPECTOR', Op.SAVE_RETAIL_OBSERVATION), ('SUPERVISOR', Op.READ_RETAIL_OBSERVATION)]:
                rows = db.execute('''SELECT revoked FROM case_access_grants
                    WHERE issuer=? AND subject=? AND case_id=? AND operation=?''',
                    (ISSUER, role, assignment['case_id'], op.value)).fetchall()
                if not rows or any(row[0] != 0 for row in rows):
                    raise ValueError('missing or revoked grant; resume cannot restore authority')
        if not key_path.exists() and not adopt_legacy:
            raise ValueError('legacy key unavailable; explicit --adopt-legacy-lab required')
        if key_path.exists() and adopt_legacy:
            raise ValueError('identity already exists; omit --adopt-legacy-lab')
        before = business_digest(path)
        backup = root / ('backup-before-resume-' + uuid.uuid4().hex + '.sqlite3')
        write_secret(backup, b'')
        with closing(sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)) as source:
            with closing(sqlite3.connect(backup)) as destination:
                source.backup(destination)
    elif path.exists() or key_path.exists():
        raise ValueError('new lab requires an empty directory')
    else:
        before, backup = None, None

    if key_path.exists():
        protected(key_path)
        key = serialization.load_pem_private_key(key_path.read_bytes(), password=None)
        if not isinstance(key, rsa.RSAPrivateKey) or key.key_size < 2048:
            raise ValueError('invalid lab key')
    else:
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        write_secret(key_path, key.private_bytes(serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    fingerprint = sha256(key.public_key().public_bytes(serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo)).hexdigest()
    if resume and not adopt_legacy:
        events = list(root.glob('lab-event-*.json'))
        if not events:
            raise ValueError('missing identity event; cannot confirm key continuity')
        latest = max(events, key=lambda p: p.lstat().st_mtime_ns)
        protected(latest)
        recorded = json.loads(latest.read_text())
        if recorded.get('public_key_sha256') != fingerprint:
            raise ValueError('lab key differs from last recorded identity')
    auth = JwtCaseAccessAuthenticator(issuer=ISSUER, audience=AUDIENCE,
        public_keys={'BETA':key.public_key()}, max_lifetime_seconds=3600, max_token_bytes=16384)
    backend = RetailBetaInspection(database_path=path, expected_audience=AUDIENCE,
                                  clock=clock, authenticator=auth)
    if not resume:
        path.chmod(0o600)
    backend.provision(assignment=assignment)
    grants = SqliteCaseAccessGrants(database_path=path)
    now = clock()
    actor = AuthenticatedPrincipal(ISSUER, 'LOCAL-LAB-ADMIN')
    for role, op in [('INSPECTOR', Op.SAVE_RETAIL_OBSERVATION), ('SUPERVISOR', Op.READ_RETAIL_OBSERVATION)]:
        principal = AuthenticatedPrincipal(ISSUER, role)
        grant = CaseAccessGrant('LAB-' + uuid.uuid4().hex, principal,
            CaseAccessPermission(assignment['case_id'], op), now-1, now+3600)
        grants.apply(record=GrantAdministrationRecord('ADD-' + grant.grant_id,
            actor, Action.GRANT, grant, now))
        token = jwt.encode({'iss':ISSUER, 'sub':role, 'aud':AUDIENCE, 'iat':now,
            'nbf':now, 'exp':now+3600, 'case_permissions':[
                {'case_id':assignment['case_id'], 'operation':op.value}]},
            key, algorithm='RS256', headers={'kid':'BETA', 'typ':'at+jwt'})
        target = root / (role.lower()+'.txt')
        # Replace a token atomically; never follow an existing symlink.
        if target.exists() or target.is_symlink():
            protected(target)
        temporary = root / ('.credential-' + uuid.uuid4().hex)
        write_secret(temporary, token.encode('ascii'))
        temporary.replace(target)
    after = business_digest(path)
    if before is not None and before != after:
        raise RuntimeError('business records changed during resume; inspect backup')
    event = {'action':'LEGACY_KEY_ADOPTED' if adopt_legacy else ('RESUMED' if resume else 'CREATED'),
        'recorded_at':now, 'public_key_sha256':fingerprint,
        'business_sha256':after, 'backup':str(backup) if backup else None,
        'notice':'SIMULATION: local administrative declaration; not independent attestation'}
    write_secret(root / ('lab-event-' + uuid.uuid4().hex + '.json'), canonical(event).encode())
    return backend, auth, event
