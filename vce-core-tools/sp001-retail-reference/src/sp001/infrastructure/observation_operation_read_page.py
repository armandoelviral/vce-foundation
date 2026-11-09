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



PAGE = _replace(
    PAGE,
    '<pre id="output" hidden></pre>',
    '<pre id="output" hidden></pre>'
    '<div id="photo-actions" hidden>'
    '<p>Para descargar la foto de esta observación, vuelve a pegar '
    'la credencial de lectura en el campo anterior.</p>'
    '<button id="download-photo" type="button">Descargar foto</button>'
    '<p id="photo-status" role="status" aria-live="polite"></p>'
    '</div>',
)

SCRIPT = _replace(
    SCRIPT,
    "function reset() {",
    "function reset() {\n"
    "    clearPhotoDownload();",
)
SCRIPT = _replace(
    SCRIPT,
    '            status.textContent = "Recibo y observación recuperados.";',
    '            setPhotoTarget(caseId, requestId);\n'
    '            status.textContent = "Recibo y observación recuperados.";',
)

SCRIPT += r"""
const photoActions = document.getElementById("photo-actions");
const photoButton = document.getElementById("download-photo");
const photoStatus = document.getElementById("photo-status");
const caseField = document.getElementById("case");
const requestField = document.getElementById("request");
let photoTarget = null;
let photoController = null;

function clearPhotoDownload() {
    photoTarget = null;
    if (photoController) photoController.abort();
    photoController = null;
    photoButton.disabled = false;
    photoActions.hidden = true;
    photoStatus.textContent = "";
}

function setPhotoTarget(caseId, requestId) {
    if (caseField.value.trim() !== caseId || requestField.value !== requestId)
        return;
    photoTarget = "/v1/cases/" + encodeURIComponent(caseId) +
        "/inspection-observation-operations/" +
        encodeURIComponent(requestId) + "/photo";
    photoActions.hidden = false;
}

for (const field of [caseField, requestField]) {
    field.addEventListener("input", () => {
        reset();
        credential.value = "";
    });
}

photoButton.addEventListener("click", async () => {
    if (!photoTarget || photoController) return;
    let token = credential.value;
    credential.value = "";
    if (!/^[\x21-\x7e]+$/.test(token)) {
        token = "";
        photoStatus.textContent = "Pega la credencial de lectura sin espacios.";
        credential.focus();
        return;
    }

    const controller = new AbortController();
    const target = photoTarget;
    photoController = controller;
    photoButton.disabled = true;
    photoStatus.textContent = "Recuperando foto…";
    const current = () => photoController === controller && photoTarget === target;

    try {
        const pending = fetch(target, {
            method: "GET",
            headers: {Authorization: "Bearer " + token},
            credentials: "omit",
            cache: "no-store",
            redirect: "error",
            signal: controller.signal
        });
        token = "";
        const response = await pending;
        if (!current()) return;

        if (response.status !== 200) {
            const data = await response.json().catch(() => null);
            if (!current()) return;
            const messages = {
                "401:credential_rejected": "Credencial rechazada o vencida.",
                "403:access_denied": "Acceso denegado para descargar la foto.",
                "404:photo_not_found": "Esta operación no tiene foto adjunta.",
                "404:operation_not_found": "La operación ya no está disponible.",
                "503:integrity_failure": "Fallo de integridad: no se descargó la foto."
            };
            photoStatus.textContent =
                messages[response.status + ":" + data?.status] ??
                "No se pudo recuperar la foto.";
            return;
        }

        if (response.headers.get("content-type") !== "application/octet-stream")
            throw new Error("Unexpected photo response.");
        const file = await response.blob();
        if (!current()) return;
        if (!file.size || file.size > 5 * 1024 * 1024)
            throw new Error("Unexpected photo size.");

        const prefix = new Uint8Array(await file.slice(0, 8).arrayBuffer());
        if (!current()) return;

        const png = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
        const isPng = png.every((byte, index) => prefix[index] === byte);
        const isJpeg = prefix[0] === 0xff && prefix[1] === 0xd8 && prefix[2] === 0xff;
        if (!isPng && !isJpeg) throw new Error("Unexpected photo format.");

        const url = URL.createObjectURL(file);
        const link = document.createElement("a");
        link.href = url;
        link.download = isPng ? "observation-photo.png" : "observation-photo.jpg";
        document.body.append(link);
        try {
            link.click();
        } finally {
            link.remove();
            setTimeout(() => URL.revokeObjectURL(url), 1000);
        }
        photoStatus.textContent = "Descarga iniciada.";
    } catch (_) {
        if (current()) photoStatus.textContent = "No se pudo recuperar la foto.";
    } finally {
        token = "";
        if (current()) {
            photoController = null;
            photoButton.disabled = false;
        }
    }
});
"""

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
