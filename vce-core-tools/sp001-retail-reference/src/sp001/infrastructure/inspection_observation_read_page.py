from fastapi.responses import HTMLResponse, Response

from sp001.infrastructure.retail_report_read_page import STYLE


PAGE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Consulta de observaciones</title>
<link rel="stylesheet" href="/inspection-observations/assets/read.css">
<script defer src="/inspection-observations/assets/read.js"></script>
</head>
<body>
<main>
<h1>Consulta de observaciones</h1>
<p>Recuperación de una versión exacta. La aplicación no guarda la credencial
en almacenamiento del navegador.</p>
<p>El responsable del documento es declarado. Esta consulta no acredita
autoría, revisión independiente ni cumplimiento.</p>
<form id="query" autocomplete="off" novalidate>
<label for="case">Caso</label>
<input id="case" required autocomplete="off">
<label for="observation">Observación</label>
<input id="observation" required autocomplete="off">
<label for="version">Versión exacta</label>
<input id="version" inputmode="numeric" required autocomplete="off">
<label for="credential">Credencial — solo el token</label>
<input id="credential" type="password" required autocomplete="off"
       spellcheck="false">
<div class="actions">
<button type="submit">Consultar</button>
<button type="button" id="clear">Limpiar</button>
</div>
</form>
<p id="status" role="status" aria-live="polite"></p>
<pre id="output" hidden></pre>
</main>
</body>
</html>
"""


SCRIPT = r"""
"use strict";

const form = document.getElementById("query");
const output = document.getElementById("output");
const status = document.getElementById("status");
const credential = document.getElementById("credential");

let generation = 0;
let active = null;

function reset() {
    generation += 1;
    if (active) active.abort();
    active = null;
    output.textContent = "";
    output.hidden = true;
    status.textContent = "";
    return generation;
}

document.getElementById("clear").addEventListener("click", () => {
    reset();
    form.reset();
});

window.addEventListener("pagehide", () => {
    reset();
    credential.value = "";
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const current = reset();
    const caseId = document.getElementById("case").value.trim();
    const observationId = document.getElementById("observation").value.trim();
    const version = document.getElementById("version").value.trim();
    let token = credential.value;
    credential.value = "";

    // The URL version remains a decimal string, without JS number conversion.
    if (!caseId || !observationId || !/^[1-9][0-9]*$/.test(version) ||
        version.length > 1000 || !token || !/^[\x21-\x7e]+$/.test(token)) {
        token = "";
        status.textContent =
            "Completa caso, observación, versión positiva y un token sin espacios.";
        return;
    }

    const controller = new AbortController();
    active = controller;
    status.textContent = "Consultando…";

    try {
        const response = await fetch(
            "/v1/cases/" + encodeURIComponent(caseId) +
            "/inspection-observations/" + encodeURIComponent(observationId) +
            "/versions/" + version,
            {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + token,
                    "Accept": "application/json"
                },
                credentials: "omit",
                cache: "no-store",
                redirect: "error",
                signal: controller.signal
            }
        );

        token = "";
        if (current !== generation) return;
        let data;
        try {
            data = await response.json();
        } catch (_) {
            if (current !== generation) return;
            status.textContent = "Respuesta inválida; no se muestra una observación.";
            return;
        }
        if (current !== generation) return;

        if (response.status === 200 && data && data.status === "ok" &&
            typeof data.observation_document === "string" &&
            data.observation_document.length > 0) {
            // Display exact document text. Do not parse/reformat its numbers
            // or interpret declared content as an evaluation or verification.
            output.textContent =
                "OBSERVACIÓN DESCRIPTIVA — SIN DICTAMEN\n" +
                "Responsable declarado; evidencia referenciada, no verificada por esta pantalla.\n\n" +
                data.observation_document;
            output.hidden = false;
            status.textContent = "Observación recuperada.";
            return;
        }

        const messages = {
            400: ["invalid_request", "Datos de consulta inválidos."],
            401: ["credential_rejected", "Credencial rechazada o vencida."],
            403: ["access_denied", "Acceso denegado para esta consulta."],
            404: ["observation_not_found",
                  "Observación no encontrada en la consulta autorizada."],
            503: ["backend_unavailable",
                  "No fue posible recuperar o preparar la observación."]
        };
        const expected = messages[response.status];
        status.textContent = expected && data && data.status === expected[0]
            ? expected[1]
            : "Respuesta inválida; no se muestra una observación.";
    } catch (error) {
        if (current !== generation) return;
        status.textContent = error.name === "AbortError"
            ? "Consulta cancelada."
            : "No fue posible completar la consulta; revisa la conexión.";
    } finally {
        token = "";
        if (current === generation) active = null;
    }
});
"""


def install_inspection_observation_read_page(app):
    """Install a public shell; observation content requires API authorization."""
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

    @app.get("/inspection-observations", include_in_schema=False)
    def read_page():
        return HTMLResponse(PAGE, headers=headers)

    @app.get("/inspection-observations/assets/read.js", include_in_schema=False)
    def read_script():
        return Response(SCRIPT, media_type="text/javascript", headers=headers)

    @app.get("/inspection-observations/assets/read.css", include_in_schema=False)
    def read_style():
        return Response(STYLE, media_type="text/css", headers=headers)
