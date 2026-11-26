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
    parser.add_argument('--resume', type=Path, help='resume this exact protected simulated lab directory')
    parser.add_argument('--adopt-legacy-lab', action='store_true', help='explicit local replacement of the unavailable legacy key')
    args = parser.parse_args()
    if args.adopt_legacy_lab and not args.resume:
        parser.error('--adopt-legacy-lab requires --resume')
    from sp001.infrastructure.retail_beta_inspection import verify_export
    if args.verify:
        dossier = verify_export(args.verify.read_bytes())
        print('PASS: correspondencia de expediente, estándar y fotografía.')
        print('SIMULADO' if dossier['assignment']['simulated'] else 'Campo declarado')
        print('El manifiesto no está firmado; no prueba procedencia frente a reemplazo total.')
        return

    import fcntl
    import socket
    import uvicorn
    from sp001.infrastructure.retail_beta_lab_identity import (
        prepare_identity, protected, ISSUER, AUDIENCE,
    )
    from sp001.infrastructure.retail_beta_http_host import create_retail_beta_app

    previous = os.umask(0o077)
    listener = socket.socket()
    lock = None
    try:
        # Reserve before touching keys, credentials or grants. Occupied port is a stop.
        listener.bind(('127.0.0.1', args.port))
        listener.listen(32)
        if args.resume and args.resume.is_symlink():
            raise ValueError('resume directory must not be a symlink')
        root = args.resume.resolve() if args.resume else Path(tempfile.mkdtemp(prefix='sp001-retail-beta-'))
        protected(root, directory=True)
        lock_path = root / '.lab.lock'
        if lock_path.exists() or lock_path.is_symlink():
            protected(lock_path)
        lock = lock_path.open('a')
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        issuer = ISSUER
        person = lambda role: {'issuer':issuer, 'subject':role}
        document = 'SIMULADO. R1: etiqueta de precio visible. R2: inspeccionar parte posterior.'
        assignment = {
            'assignment_id':'BETA-001','case_id':'BETA-STORE-001',
            'store':'TIENDA SIMULADA','corner':'CORNER SIMULADO', 'simulated':True,
            'inspector':person('INSPECTOR'), 'supervisor':person('SUPERVISOR'),
            'standard':{'standard_id':'VM-SIMULATED','revision':1,'document':document,
                'sha256':sha256(document.encode()).hexdigest(),
                'criteria':[{'rule_id':'R1','criterion_version':1,'statement':'Etiqueta visible'},
                            {'rule_id':'R2','criterion_version':1,'statement':'Parte posterior revisada'}],
                'approval_reference':'APROBACION SIMULADA, NO DOCUMENTO COMERCIAL',
                'approved_by':person('SUPERVISOR')}}
        backend, auth, event = prepare_identity(root=root, resume=bool(args.resume),
            adopt_legacy=args.adopt_legacy_lab, clock=lambda:int(time.time()), assignment=assignment)
        app=create_retail_beta_app(backend=backend,authenticator=auth,
                                  audience=AUDIENCE,clock=lambda:int(time.time()))
        if args.resume:
            print('Identidad de laboratorio conservada;' if not args.adopt_legacy_lab else
                  'Recuperación administrativa LEGACY: nueva clave local; no acredita autoría histórica.', flush=True)
            print('Expediente conservado. Copia previa: ' + event['backup'], flush=True)
        print('CORRIDA SIMULADA. Aceptación en campo pendiente.',flush=True)
        print(f'Base y credenciales temporales: {root}',flush=True)
        print(f'Inspector y supervisor: http://127.0.0.1:{args.port}/retail-beta',flush=True)
        print('Usa sesiones separadas. Tokens válidos una hora. Ctrl+C detiene.',flush=True)
        try:
            server = uvicorn.Server(uvicorn.Config(app, access_log=False))
            server.run(sockets=[listener])
        finally:
            for role in ('inspector','supervisor'):
                (root/(role+'.txt')).unlink(missing_ok=True)
            print(f'Base conservada: {root / "beta.sqlite3"}. Clave local conservada con permisos privados; uso exclusivo de simulación.')
    finally:
        listener.close()
        if lock is not None:
            lock.close()
        os.umask(previous)


if __name__ == '__main__':
    main()
