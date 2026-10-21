import argparse
import os
from pathlib import Path
import sys
import time

from cryptography.hazmat.primitives.serialization import load_pem_public_key

from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportIdentity,
)
from sp001.infrastructure.configured_access_token_keys import (
    ConfiguredAccessTokenKeys,
)
from sp001.infrastructure.retail_report_composition import (
    compose_transactional_retail_reports,
)
from sp001.services.authenticated_retail_reports import (
    RetailReportAccessDenied, RetailReportAuthenticationRejected,
)
from sp001.services.retail_vm_report_text import render_retail_vm_report_text


def _positive_integer(value):
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def main(argv=None, *, environment=None, stdin=None, stdout=None, stderr=None):
    environment = os.environ if environment is None else environment
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr

    parser = argparse.ArgumentParser(
        description="Recover an authorized VM report. Read bearer token from stdin.",
    )
    parser.add_argument("--database", required=True)
    parser.add_argument("--issuer", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--key-id", required=True)
    parser.add_argument("--public-key-env", required=True)
    parser.add_argument(
        "--max-lifetime-seconds", required=True, type=_positive_integer,
    )
    parser.add_argument("--max-token-bytes", required=True, type=_positive_integer)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--report-id", required=True)
    args = parser.parse_args(argv)

    try:
        if not Path(args.database).is_file():
            raise ValueError("database must already exist")
        pem = environment.get(args.public_key_env)
        if not isinstance(pem, str) or not pem.strip():
            raise ValueError("missing public verification key")
        public_key = load_pem_public_key(pem.encode("ascii"))
        resolver = ConfiguredAccessTokenKeys(
            issuer=args.issuer, public_keys={args.key_id: public_key},
        )
        identity = RetailRuleEvaluationReportIdentity(args.report_id)
        if not args.case_id.strip():
            raise ValueError("case identity must not be empty")
    except (TypeError, ValueError, UnicodeError):
        print("Configuración inválida del lector VM.", file=stderr)
        return 2

    try:
        # Bound input consumption; token must occupy a single line.
        credential = stdin.read(args.max_token_bytes + 3)
        if credential.endswith("\r\n"):
            credential = credential[:-2]
        elif credential.endswith("\n"):
            credential = credential[:-1]
        if (
            not credential
            or len(credential.encode("ascii")) > args.max_token_bytes
            or "\n" in credential or "\r" in credential
        ):
            raise RetailReportAuthenticationRejected("invalid credential input")

        service = compose_transactional_retail_reports(
            issuer=args.issuer, audience=args.audience, key_resolver=resolver,
            max_lifetime_seconds=args.max_lifetime_seconds,
            max_token_bytes=args.max_token_bytes,
            database_path=args.database, clock=lambda: int(time.time()),
        )
        recovered = service.recover_with_admissions(
            credential=credential, identity=identity, case_id=args.case_id,
        )
        if recovered is None:
            print("Reporte no encontrado para la consulta autorizada.", file=stderr)
            return 5
        rendered = render_retail_vm_report_text(
            identity=identity, recovered=recovered,
        )
    except RetailReportAuthenticationRejected:
        print("Credencial rechazada o fuera de vigencia.", file=stderr)
        return 3
    except RetailReportAccessDenied:
        print("Acceso al reporte denegado.", file=stderr)
        return 4
    except UnicodeError:
        print("Credencial rechazada o fuera de vigencia.", file=stderr)
        return 3
    except Exception:
        print("No fue posible recuperar o preparar el reporte.", file=stderr)
        return 6

    try:
        stdout.write(rendered)
        stdout.flush()
    except Exception:
        print("No fue posible completar la salida del reporte.", file=stderr)
        return 6
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
