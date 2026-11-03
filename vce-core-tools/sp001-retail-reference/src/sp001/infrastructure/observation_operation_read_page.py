from fastapi.responses import HTMLResponse, Response

from sp001.infrastructure.inspection_observation_read_page import (
    PAGE as OBSERVATION_PAGE,
    SCRIPT as OBSERVATION_SCRIPT,
    STYLE,
)


def _replace(source, old, new):
    if source.count(old) != 1:
        raise RuntimeError("operation query page template changed")
    return source.replace(old, new, 1)


PAGE = OBSERVATION_PAGE.replace(
    "Consulta de observaciones", "Consulta de operaciones"
).replace(
    "/inspection-observations/assets/",
    "/inspection-observation-operations/assets/",
)
PAGE = _replace(
    PAGE,
    "Recuperación de una versión exacta.",
    "Recuperación de un recibo y su observación para la identidad autenticada.",
)
start = PAGE.index('<label for="observation">')
end = PAGE.index('<label for="credential">', start)
PAGE = (
    PAGE[:start]
    + '<label for="request">Identificador de solicitud</label>\n'
      '<input id="request" required autocomplete="off">\n'
    + PAGE[end:]
)

SCRIPT = OBSERVATION_SCRIPT
start = SCRIPT.index(
    '    const observationId = document.getElementById("observation")'
)
end = SCRIPT.index("    let token = credential.value;", start)
SCRIPT = (
    SCRIPT[:start]
    + '    const requestId = document.getElementById("request").value;\n'
    + SCRIPT[end:]
)

start = SCRIPT.index("    // The URL version")
end = SCRIPT.index("    const controller = new AbortController();", start)
SCRIPT = SCRIPT[:start] + r"""
    if (!caseId || !requestId ||
        /[\s\x00-\x1f\x7f]/u.test(requestId) ||
        !token || !/^[\x21-\x7e]+$/.test(token)) {
        token = "";
        status.textContent =
            "Completa caso, solicitud y un token sin espacios.";
        return;
    }

""" + SCRIPT[end:]

SCRIPT = _replace(
    SCRIPT,
    '"/inspection-observations/" + encodeURIComponent(observationId) +\n'
    '            "/versions/" + version,',
    '"/inspection-observation-operations/" + encodeURIComponent(requestId),',
)

# Preserve the exact integer token when reading the canonical document.
# Fail closed if this browser cannot provide the JSON source context.
SCRIPT = _replace(
    SCRIPT,
    "    const root = JSON.parse(document);",
    """    const root = JSON.parse(document, function (key, value, context) {
        if (key === "observation_version" && typeof value === "number") {
            if (!context || !/^[1-9][0-9]*$/.test(context.source))
                throw new Error("Exact version unavailable.");
            return context.source;
        }
        return value;
    });""",
)
SCRIPT = _replace(
    SCRIPT,
    "    const item = root.observation;",
    """    const item = root.observation;
    if (item.observation_version !== version)
        throw new Error("Unexpected observation version.");""",
)

SCRIPT = _replace(
    SCRIPT,
    """                readable = readableObservation(
                    data.observation_document, caseId, observationId, version,
                );""",
    """                if (data.case_id !== caseId ||
                    data.request_id !== requestId ||
                    typeof data.observation_id !== "string" ||
                    !data.observation_id.trim() ||
                    typeof data.observation_version !== "string" ||
                    !/^[1-9][0-9]*$/.test(data.observation_version) ||
                    data.observation_version.length > 1000 ||
                    !["CREATED", "REUSED"].includes(data.disposition))
                    throw new Error("Invalid recovered receipt.");

                readable = [
                    "RECIBO Y OBSERVACIÓN RECUPERADOS",
                    "Solicitud: " + requestId,
                    "Disposición registrada: " + data.disposition,
                    "CREATED: la operación registró la creación de la observación.",
                    "REUSED: la operación registró una observación ya existente.",
                    "La recuperación no acredita autoría ni revisión independiente.",
                    "",
                    readableObservation(
                        data.observation_document, caseId,
                        data.observation_id, data.observation_version,
                    ),
                ].join("\\n");""",
)
SCRIPT = _replace(
    SCRIPT,
    'status.textContent = "Observación recuperada.";',
    'status.textContent = "Recibo y observación recuperados.";',
)
SCRIPT = _replace(
    SCRIPT,
    '404: ["observation_not_found",\n'
    '                  "Observación no encontrada en la consulta autorizada."],',
    '404: ["operation_not_found",\n'
    '                  "Solicitud no encontrada en la consulta autorizada."],',
)
SCRIPT = _replace(
    SCRIPT,
    "        const expected = messages[response.status];",
    """        if (response.status === 503 && data &&
            data.status === "integrity_failure") {
            status.textContent =
                "Fallo de integridad: no se muestra el recibo ni la observación.";
            return;
        }
        const expected = messages[response.status];""",
)


def install_observation_operation_read_page(app):
    """Public shell; recovered content requires authenticated API access."""
    headers = {
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "no-referrer",
        "Content-Security-Policy": (
            "default-src 'none'; script-src 'self'; style-src 'self'; "
            "connect-src 'self'; form-action 'none'; "
            "frame-ancestors 'none'; base-uri 'none'"
        ),
    }

    @app.get("/inspection-observation-operations", include_in_schema=False)
    def operation_page():
        return HTMLResponse(PAGE, headers=headers)

    @app.get(
        "/inspection-observation-operations/assets/read.js",
        include_in_schema=False,
    )
    def operation_script():
        return Response(SCRIPT, media_type="text/javascript", headers=headers)

    @app.get(
        "/inspection-observation-operations/assets/read.css",
        include_in_schema=False,
    )
    def operation_style():
        return Response(STYLE, media_type="text/css", headers=headers)
