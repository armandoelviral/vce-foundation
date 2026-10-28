from sp001.infrastructure.retail_report_read_page import install_retail_report_read_page

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportIdentity,
)
from sp001.services.authenticated_retail_reports import (
    RetailReportAccessDenied,
    RetailReportAuthenticationRejected,
)
from sp001.services.retail_vm_report_text import render_retail_vm_report_text
from sp001.infrastructure.retail_rule_evaluation_serialization import (
    serialize_retail_rule_evaluation_report,
)
from sp001.infrastructure.retail_rule_evaluation_admission_serialization import (
    serialize_retail_rule_evaluation_admission,
)


def create_retail_report_read_app(*, service, max_token_bytes=16384):
    """HTTP read adapter; authentication and authorization belong to service."""

    if not callable(getattr(service, "recover_with_admissions", None)):
        raise TypeError("service must support admission recovery")

    if type(max_token_bytes) is not int or max_token_bytes < 1:
        raise ValueError("max_token_bytes must be a positive integer")

    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    def response(status_code, status, **values):
        return JSONResponse(
            status_code=status_code,
            content={"status": status, **values},
            headers={"Cache-Control": "no-store"},
        )

    @app.get("/v1/cases/{case_id}/retail-reports/{report_id}")
    def read_report(case_id: str, report_id: str, request: Request):
        headers = request.headers.getlist("authorization")

        if len(headers) != 1:
            return response(401, "credential_rejected")

        parts = headers[0].split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return response(401, "credential_rejected")

        credential = parts[1]
        try:
            size = len(credential.encode("ascii"))
        except UnicodeEncodeError:
            return response(401, "credential_rejected")

        if size == 0 or size > max_token_bytes:
            return response(401, "credential_rejected")

        try:
            identity = RetailRuleEvaluationReportIdentity(report_id)
            recovered = service.recover_with_admissions(
                credential=credential,
                identity=identity,
                case_id=case_id,
            )

            if recovered is None:
                return response(404, "report_not_found")

            rendered = render_retail_vm_report_text(
                identity=identity,
                recovered=recovered,
            )

            # Reautenticar y autorizar después de preparar la salida.
            confirmed = service.recover_with_admissions(
                credential=credential,
                identity=identity,
                case_id=case_id,
            )
            if confirmed is None:
                raise ValueError("report disappeared before response")

            if (
                serialize_retail_rule_evaluation_report(confirmed.report)
                != serialize_retail_rule_evaluation_report(recovered.report)
                or tuple(
                    serialize_retail_rule_evaluation_admission(item)
                    for item in confirmed.admissions
                ) != tuple(
                    serialize_retail_rule_evaluation_admission(item)
                    for item in recovered.admissions
                )
            ):
                raise ValueError("recovered content changed before response")

            return response(200, "ok", report_text=rendered)

        except RetailReportAuthenticationRejected:
            return response(401, "credential_rejected")
        except RetailReportAccessDenied:
            return response(403, "access_denied")
        except Exception:
            # No detalles internos ni contenido del reporte en el error.
            return response(503, "backend_unavailable")

    install_retail_report_read_page(app)
    return app
