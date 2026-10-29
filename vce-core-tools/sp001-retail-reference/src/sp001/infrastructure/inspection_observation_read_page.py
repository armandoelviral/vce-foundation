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
<details id="technical" hidden>
<summary>Detalle técnico — documento original</summary>
<pre id="technical-document"></pre>
</details>
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
const technical = document.getElementById("technical");
const technicalDocument = document.getElementById("technical-document");

let generation = 0;
let active = null;

function reset() {
    generation += 1;
    if (active) active.abort();
    active = null;
    output.textContent = "";
    output.hidden = true;
    technicalDocument.textContent = "";
    technical.hidden = true;
    technical.open = false;
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


function readableObservation(document, caseId, observationId, version) {
    const root = JSON.parse(document);
    if (!root || root.schema_version !== 1 || !root.observation)
        throw new Error("Unsupported observation document.");
    const item = root.observation;

    function text(value) {
        if (typeof value !== "string") throw new Error("Invalid text.");
        return value;
    }
    function record(value, type) {
        if (!value || value.type !== type || !value.fields ||
            typeof value.fields !== "object" || Array.isArray(value.fields))
            throw new Error("Invalid record.");
        return value.fields;
    }
    function list(value) {
        if (!value || value.type !== "tuple" || !Array.isArray(value.items))
            throw new Error("Invalid list.");
        return value.items.map(text);
    }
    function instant(value) {
        if (!value || value.type !== "datetime")
            throw new Error("Invalid datetime.");
        return text(value.iso);
    }
    if (text(item.case_id) !== caseId ||
        text(item.observation_id) !== observationId)
        throw new Error("Unexpected identity.");

    const actor = record(item.declared_observer, "RetailProcessActor");
    const role = record(actor.role, "RetailProcessRole");
    const methods = {
        DIRECT_INSPECTION: "Inspección directa",
        EVIDENCE_REVIEW: "Revisión de evidencia"
    };
    const actorTypes = {
        HUMAN: "Persona", TEAM: "Equipo",
        SYSTEM: "Sistema", ORGANIZATION: "Organización"
    };
    if (!methods[item.method] || !actor.actor_type ||
        actor.actor_type.type !== "ActorType" ||
        !actorTypes[actor.actor_type.value])
        throw new Error("Unknown method or actor type.");

    const limitations = list(item.limitations);
    const evidence = list(item.evidence_ids);
    const lines = [
        "OBSERVACIÓN DESCRIPTIVA — SIN DICTAMEN",
        "",
        "Caso: " + caseId,
        "Observación: " + observationId,
        // Keep exact requested version as text. Never render the JSON number,
        // which may exceed JavaScript's safe integer range.
        "Versión consultada: " + version,
        "Objeto o zona: " + text(item.subject_reference),
        "Método declarado: " + methods[item.method],
        "",
        "DESCRIPCIÓN DECLARADA POR EL OPERADOR",
        "No se ha clasificado ni validado como dictamen.",
        text(item.description),
        "",
        "ALCANCE DECLARADO",
        text(item.scope),
        "",
        "LIMITACIONES REGISTRADAS",
        ...(limitations.length ? limitations : [
            "No se registraron limitaciones; no demuestra que no existan."
        ]),
        "",
        "REFERENCIAS DE EVIDENCIA",
        ...(evidence.length ? evidence : ["Sin referencias registradas."]),
        "Las referencias no acreditan archivos verificados.",
        "",
        "RESPONSABLE DECLARADO",
        "Responsable declarado: " + text(actor.actor_id),
        "Tipo: " + actorTypes[actor.actor_type.value],
        "Organización: " + text(actor.organization_id),
        "Cliente: " + text(actor.customer_id),
        "Función: " + text(role.role_name),
        "Identificador de función: " + text(role.role_id),
        "Cliente de la función: " + text(role.customer_id),
        "",
        "FECHAS DECLARADAS",
        "Inspección o revisión: " + instant(item.observed_at),
        "Registro: " + instant(item.recorded_at),
        "Estas fechas no acreditan captura de fotografía ni COMMIT.",
        "",
        "Esta ficha no acredita autoría, revisión independiente ni cumplimiento."
    ];
    return lines.join("\n");
}

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

            let readable;
            try {
                readable = readableObservation(
                    data.observation_document, caseId, observationId, version,
                );
            } catch (_) {
                status.textContent =
                    "Respuesta inválida; no se muestra una observación.";
                return;
            }
            output.textContent = readable;
            output.hidden = false;
            technicalDocument.textContent = data.observation_document;
            technical.hidden = false;
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
