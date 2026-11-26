"""One-assignment beta, behind a trusted JWT verifier and protected SQLite.

Provisioning is a trusted administrative action, never a client approval flag.
No claim of host isolation, third-party authorship, or immutable administrator log.
"""
from contextlib import closing, contextmanager
from dataclasses import asdict
from hashlib import sha256
from io import BytesIO
import json
import zipfile

from sp001.contracts.case_access_context import CaseAccessOperation as Op
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_rule_criterion import RetailRuleCriterion
from sp001.contracts.retail_context_rule_observation import RuleObservationStatus as Status
from sp001.infrastructure.sqlite_observation_operations import (
    SqliteObservationOperations, ObservationOperationIntegrityFailure as Integrity,
)
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    InspectionObservationAccessDenied as Denied,
    InspectionObservationAuthenticationRejected as Rejected,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    deserialize_retail_inspection_observation as deserialize,
)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False)


def exact(value, fields):
    if type(value) is not dict or set(value) != set(fields):
        raise ValueError("unexpected fields")


def text(value):
    if type(value) is not str or not value.strip() or len(value) > 10000:
        raise ValueError("invalid text")
    return value


class Conflict(ValueError):
    pass


class RetailBetaInspection(SqliteObservationOperations):
    """Reuses observation storage and live grant checks, adds explicit role scope.

    A trusted provisioner approves exactly one standard and assignment per DB.
    Every decision is immutable and references the persisted submission digest.
    """
    def __init__(self, *, authenticator, **kwargs):
        super().__init__(**kwargs)
        self.authenticator = authenticator
        with closing(self._connect()) as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS retail_beta_assignment (
                    singleton INTEGER PRIMARY KEY CHECK(singleton=1), document TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS retail_beta_submission (
                    singleton INTEGER PRIMARY KEY CHECK(singleton=1), document TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS retail_beta_decision (
                    singleton INTEGER PRIMARY KEY CHECK(singleton=1), document TEXT NOT NULL);
            ''')

    def provision(self, *, assignment):
        """Trusted local configuration, no HTTP provisioning endpoint."""
        exact(assignment, ('assignment_id', 'case_id', 'store', 'corner', 'inspector',
                           'supervisor', 'standard', 'simulated'))
        for field in ('assignment_id', 'case_id', 'store', 'corner'):
            text(assignment[field])
        for role in ('inspector', 'supervisor'):
            exact(assignment[role], ('issuer', 'subject'))
            AuthenticatedPrincipal(**assignment[role])
        if assignment['inspector'] == assignment['supervisor']:
            raise ValueError('inspector and supervisor must differ')
        if type(assignment['simulated']) is not bool:
            raise ValueError('simulated must be explicit')
        standard = assignment['standard']
        exact(standard, ('standard_id', 'revision', 'document', 'sha256', 'criteria',
                         'approval_reference', 'approved_by'))
        for field in ('standard_id', 'document', 'approval_reference'):
            text(standard[field])
        if type(standard['revision']) is not int or standard['revision'] < 1:
            raise ValueError('invalid revision')
        if standard['approved_by'] != assignment['supervisor']:
            raise ValueError('approval must identify configured supervisor')
        if sha256(standard['document'].encode()).hexdigest() != standard['sha256']:
            raise ValueError('standard digest mismatch')
        if type(standard['criteria']) is not list or not standard['criteria']:
            raise ValueError('criteria required')
        rules = [RetailRuleCriterion(**item) for item in standard['criteria']]
        if len({r.rule_id for r in rules}) != len(rules):
            raise ValueError('duplicate criterion')
        encoded = canonical(assignment)
        with closing(self._connect()) as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT document FROM retail_beta_assignment').fetchone()
            if row and row[0] != encoded:
                raise Conflict('assignment is immutable; use a separate database')
            db.execute('INSERT OR IGNORE INTO retail_beta_assignment VALUES (1, ?)', (encoded,))
            db.commit()

    @contextmanager
    def session(self, credential, role=None, write=False):
        access = self.authenticator.authenticate(credential=credential)
        if access is None:
            raise Rejected('credential rejected')
        with closing(self._connect()) as db:
            db.execute('BEGIN IMMEDIATE' if write else 'BEGIN')
            row = db.execute('SELECT document FROM retail_beta_assignment').fetchone()
            if not row:
                raise Denied('not assigned')
            assignment = json.loads(row[0])
            who = asdict(access.principal)
            if role is not None and who != assignment[role]:
                raise Denied('wrong assignment role')
            if who not in (assignment['inspector'], assignment['supervisor']):
                raise Denied('not assigned')
            operation = Op.SAVE_RETAIL_OBSERVATION if who == assignment['inspector'] else Op.READ_RETAIL_OBSERVATION
            self._authorize(db, access, assignment['case_id'], operation)
            yield db, assignment, access
            self._authorize(db, access, assignment['case_id'], operation)
            db.commit()

    def assigned(self, *, credential):
        with self.session(credential) as (_, assignment, _):
            return assignment

    def _effect(self, db, assignment, request_id):
        principal = assignment['inspector']
        row = db.execute('''SELECT observation_id, observation_version, document,
                                   disposition, photo_sha256
                            FROM retail_observation_operations
                            WHERE issuer=? AND subject=? AND case_id=? AND request_id=?''',
                         (principal['issuer'], principal['subject'], assignment['case_id'], request_id)).fetchone()
        if not row:
            raise ValueError('save observation first')
        try:
            item = deserialize(row[2])
        except (ValueError, TypeError) as error:
            raise Integrity('invalid stored observation') from error
        if row[3] not in ('CREATED', 'REUSED'):
            raise Integrity('invalid stored disposition')
        effect = db.execute('''SELECT document FROM retail_inspection_observations
                              WHERE observation_id=? AND observation_version=?''', row[:2]).fetchone()
        if (not effect or effect[0] != row[2] or item.case_id != assignment['case_id']
                or item.observation_id != row[0] or str(item.observation_version) != row[1]):
            raise Integrity('effect mismatch')
        photo = self._read_photo(db, assignment['case_id'], row[:2], row[4])
        return {'request_id': request_id, 'observation_document': row[2],
                'disposition': row[3], 'photo_sha256': row[4]}, photo

    def submit(self, *, credential, request_id, outcomes):
        text(request_id)
        with self.session(credential, 'inspector', True) as (db, assignment, _):
            receipt, photo = self._effect(db, assignment, request_id)
            rules = {r['rule_id']: r for r in assignment['standard']['criteria']}
            if type(outcomes) is not dict or set(outcomes) != set(rules):
                raise ValueError('every assigned criterion needs an explicit outcome')
            for rule_id, outcome in outcomes.items():
                exact(outcome, ('status', 'rationale'))
                status = Status(outcome['status'])
                text(outcome['rationale'])
                if status in (Status.CONFORMANT, Status.NON_CONFORMANT) and photo is None:
                    raise ValueError('conclusive assessment requires photo')
            content = {'assignment_sha256': sha256(canonical(assignment).encode()).hexdigest(),
                       'receipt': receipt, 'outcomes': outcomes}
            encoded = canonical(content)
            old = db.execute('SELECT document FROM retail_beta_submission').fetchone()
            if old and old[0] != encoded:
                raise Conflict('submission is immutable')
            db.execute('INSERT OR IGNORE INTO retail_beta_submission VALUES (1, ?)', (encoded,))
            return content

    def _recover(self, db, assignment):
        row = db.execute('SELECT document FROM retail_beta_submission').fetchone()
        if row is None:
            return {'assignment': assignment, 'submission': None, 'decision': None}, None
        submission = json.loads(row[0])
        try:
            receipt, photo = self._effect(db, assignment, submission['receipt']['request_id'])
        except ValueError as error:
            raise Integrity('submitted receipt missing or invalid') from error
        if (receipt != submission['receipt'] or submission['assignment_sha256'] !=
                sha256(canonical(assignment).encode()).hexdigest()):
            raise Integrity('submission binding mismatch')
        row = db.execute('SELECT document FROM retail_beta_decision').fetchone()
        decision = json.loads(row[0]) if row else None
        if decision and decision['submission_sha256'] != sha256(canonical(submission).encode()).hexdigest():
            raise Integrity('decision binding mismatch')
        return {'assignment': assignment, 'submission': submission, 'decision': decision}, photo

    def recover(self, *, credential):
        with self.session(credential) as (db, assignment, _):
            return self._recover(db, assignment)[0]

    def photo(self, *, credential):
        with self.session(credential) as (db, assignment, _):
            dossier, photo = self._recover(db, assignment)
            if dossier['submission'] is None or photo is None:
                raise ValueError('submitted photo required')
            return photo

    def decide(self, *, credential, action, rationale):
        if action not in ('REVIEW_ACCEPTED', 'FOLLOW_UP_REQUIRED'):
            raise ValueError('invalid decision')
        text(rationale)
        with self.session(credential, 'supervisor', True) as (db, assignment, access):
            dossier, _ = self._recover(db, assignment)
            submission = dossier['submission']
            if submission is None:
                raise ValueError('no submission')
            if action == 'REVIEW_ACCEPTED' and any(
                o['status'] in ('INSUFFICIENT_EVIDENCE', 'DISPUTED')
                for o in submission['outcomes'].values()
            ):
                raise ValueError('unverifiable or disputed criteria require follow-up')
            decision = {'action': action, 'rationale': rationale,
                        'supervisor': asdict(access.principal),
                        'submission_sha256': sha256(canonical(submission).encode()).hexdigest(),
                        'decided_at': self._clock()}
            row = db.execute('SELECT document FROM retail_beta_decision').fetchone()
            if row:
                old = json.loads(row[0])
                if old['action'] != action or old['rationale'] != rationale:
                    raise Conflict('decision is immutable')
                return old
            db.execute('INSERT INTO retail_beta_decision VALUES (1, ?)', (canonical(decision),))
            return decision

    def export(self, *, credential):
        with self.session(credential, 'supervisor') as (db, assignment, _):
            dossier, photo = self._recover(db, assignment)
            if dossier['submission'] is None or dossier['decision'] is None:
                raise ValueError('review required before export')
            files = {'dossier.json': canonical(dossier).encode(),
                     'standard.txt': assignment['standard']['document'].encode()}
            if photo is not None:
                files['photo.bin'] = photo
            manifest = {name: sha256(data).hexdigest() for name, data in files.items()}
            files['manifest.json'] = canonical(manifest).encode()
            output = BytesIO()
            with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
                for name, data in files.items():
                    archive.writestr(name, data)
            return output.getvalue()


def verify_export(data):
    """Offline consistency only. Manifest is unsigned, not a trusted attestation."""
    with zipfile.ZipFile(BytesIO(data)) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) not in (
            {'dossier.json', 'standard.txt', 'manifest.json'},
            {'dossier.json', 'standard.txt', 'manifest.json', 'photo.bin'},
        ):
            raise Integrity('unexpected archive members')
        if any(info.file_size > 10 * 1024 * 1024 for info in archive.infolist()):
            raise Integrity('archive member too large')
        files = {name: archive.read(name) for name in names}
    manifest = json.loads(files.pop('manifest.json'))
    if manifest != {name: sha256(value).hexdigest() for name, value in files.items()}:
        raise Integrity('export digest mismatch')
    dossier = json.loads(files['dossier.json'])
    a, s, d = dossier['assignment'], dossier['submission'], dossier['decision']
    if (files['standard.txt'].decode() != a['standard']['document']
            or sha256(files['standard.txt']).hexdigest() != a['standard']['sha256']
            or s['assignment_sha256'] != sha256(canonical(a).encode()).hexdigest()
            or d['submission_sha256'] != sha256(canonical(s).encode()).hexdigest()
            or (sha256(files['photo.bin']).hexdigest() if 'photo.bin' in files else None)
               != s['receipt']['photo_sha256']):
        raise Integrity('export correspondence mismatch')
    observation = deserialize(s['receipt']['observation_document'])
    if (observation.case_id != a['case_id'] or d['supervisor'] != a['supervisor']
            or d['action'] not in ('REVIEW_ACCEPTED', 'FOLLOW_UP_REQUIRED')
            or set(s['outcomes']) != {r['rule_id'] for r in a['standard']['criteria']}):
        raise Integrity('export scope mismatch')
    for outcome in s['outcomes'].values():
        exact(outcome, ('status', 'rationale'))
        status = Status(outcome['status'])
        text(outcome['rationale'])
        if status in (Status.CONFORMANT, Status.NON_CONFORMANT) and 'photo.bin' not in files:
            raise Integrity('missing evidence')
        if d['action'] == 'REVIEW_ACCEPTED' and status in (Status.INSUFFICIENT_EVIDENCE, Status.DISPUTED):
            raise Integrity('unresolved criterion')
    return dossier
