"""SIMULATED one-store beta launcher. Never loads Intel components."""
import argparse
from hashlib import sha256
import os
from pathlib import Path
import tempfile
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', type=Path, help='verify exported ZIP offline')
    parser.add_argument('--port', type=int, default=8768)
    args = parser.parse_args()
    from sp001.infrastructure.retail_beta_inspection import verify_export
    if args.verify:
        dossier = verify_export(args.verify.read_bytes())
        print('PASS: correspondencia de expediente, estándar y fotografía.')
        print('SIMULADO' if dossier['assignment']['simulated'] else 'Campo declarado')
        print('El manifiesto no está firmado; no prueba procedencia frente a reemplazo total.')
        return

    import jwt
    import uvicorn
    from cryptography.hazmat.primitives.asymmetric import rsa
    from sp001.contracts.case_access_context import CaseAccessOperation as Op, CaseAccessPermission
    from sp001.contracts.case_access_grant import CaseAccessGrant
    from sp001.contracts.case_access_grant_administration import GrantAdministrationAction as Action, GrantAdministrationRecord
    from sp001.contracts.case_read_access import AuthenticatedPrincipal
    from sp001.infrastructure.jwt_case_access_authenticator import JwtCaseAccessAuthenticator
    from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
    from sp001.infrastructure.retail_beta_inspection import RetailBetaInspection
    from sp001.infrastructure.retail_beta_http_host import create_retail_beta_app

    previous = os.umask(0o077)
    try:
        root = Path(tempfile.mkdtemp(prefix='sp001-retail-beta-'))
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        issuer, audience = 'retail-beta-simulation', 'retail-beta'
        auth = JwtCaseAccessAuthenticator(issuer=issuer, audience=audience,
            public_keys={'BETA':key.public_key()}, max_lifetime_seconds=3600, max_token_bytes=16384)
        backend = RetailBetaInspection(database_path=root/'beta.sqlite3',
            expected_audience=audience, clock=lambda:int(time.time()), authenticator=auth)
        person = lambda role: {'issuer':issuer, 'subject':role}
        document = 'SIMULADO. R1: etiqueta de precio visible. R2: inspeccionar parte posterior.'
        backend.provision(assignment={
            'assignment_id':'BETA-001','case_id':'BETA-STORE-001',
            'store':'TIENDA SIMULADA','corner':'CORNER SIMULADO', 'simulated':True,
            'inspector':person('INSPECTOR'), 'supervisor':person('SUPERVISOR'),
            'standard':{'standard_id':'VM-SIMULATED','revision':1,'document':document,
                'sha256':sha256(document.encode()).hexdigest(),
                'criteria':[{'rule_id':'R1','criterion_version':1,'statement':'Etiqueta visible'},
                            {'rule_id':'R2','criterion_version':1,'statement':'Parte posterior revisada'}],
                'approval_reference':'APROBACION SIMULADA, NO DOCUMENTO COMERCIAL',
                'approved_by':person('SUPERVISOR')}})
        grants=SqliteCaseAccessGrants(database_path=root/'beta.sqlite3')
        now=int(time.time())
        for role, ops in [('INSPECTOR',(Op.SAVE_RETAIL_OBSERVATION,)),
                          ('SUPERVISOR',(Op.READ_RETAIL_OBSERVATION,))]:
            principal=AuthenticatedPrincipal(**person(role))
            for op in ops:
                grant=CaseAccessGrant(role+'-'+op.value,principal,
                    CaseAccessPermission('BETA-STORE-001',op),now-1,now+3600)
                grants.apply(record=GrantAdministrationRecord('ADD-'+grant.grant_id,
                    principal,Action.GRANT,grant,now))
            token=jwt.encode({'iss':issuer,'sub':role,'aud':audience,'iat':now,
                'nbf':now,'exp':now+3600,'case_permissions':[
                    {'case_id':'BETA-STORE-001','operation':op.value} for op in ops]},
                key,algorithm='RS256',headers={'kid':'BETA','typ':'at+jwt'})
            (root/(role.lower()+'.txt')).write_text(token,encoding='ascii')
        del key, token
        app=create_retail_beta_app(backend=backend,authenticator=auth,
                                  audience=audience,clock=lambda:int(time.time()))
        print('CORRIDA SIMULADA. Aceptación en campo pendiente.',flush=True)
        print(f'Base y credenciales temporales: {root}',flush=True)
        print(f'Inspector y supervisor: http://127.0.0.1:{args.port}/retail-beta',flush=True)
        print('Usa sesiones separadas. Tokens válidos una hora. Ctrl+C detiene.',flush=True)
        try:
            uvicorn.run(app,host='127.0.0.1',port=args.port,access_log=False)
        finally:
            for role in ('inspector','supervisor'):
                (root/(role+'.txt')).unlink(missing_ok=True)
            print(f'Base conservada: {root / "beta.sqlite3"}. No se conserva clave de firma.')
    finally:
        os.umask(previous)


if __name__ == '__main__':
    main()
