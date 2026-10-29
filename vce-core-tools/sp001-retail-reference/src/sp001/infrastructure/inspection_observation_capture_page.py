from html import escape

from fastapi.responses import HTMLResponse, Response
from sp001.infrastructure.retail_report_read_page import STYLE


FIELDS = (
    ("case_id", "Caso"),
    ("observation_id", "Identificador de observación"),
    ("observation_version", "Versión positiva"),
    ("subject_reference", "Objeto o zona observada"),
    ("actor_id", "Identificador del responsable declarado"),
    ("customer_id", "Identificador del cliente u organización usuaria"),
    ("organization_id", "Identificador de organización del responsable"),
    ("role_id", "Identificador de función declarada"),
    ("role_name", "Nombre de función declarada"),
    ("observed_at", "Fecha de inspección o revisión, con desplazamiento UTC"),
    ("recorded_at", "Fecha declarada de registro, con desplazamiento UTC"),
)


def _section_inputs(names):
    labels = dict(FIELDS)
    return "".join(
        f'<label for="{name}">{escape(labels[name])}</label>'
        f'<input id="{name}" required autocomplete="off">'
        for name in names
    )

PAGE = """<!doctype html>
<html lang="es"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Captura de observación descriptiva</title>
<link rel="stylesheet" href="/inspection-observations/capture/assets/form.css">
<script defer src="/inspection-observations/capture/assets/form.js"></script>
</head><body><main>
<h1>Captura de observación — sin dictamen</h1>
<p>Responsable y fechas declarados. Guardar no acredita autoría,
verificación de evidencia, aprobación ni cumplimiento.</p>
<p>El borrador se conserva al cambiar de sección y ante errores.
Recargar o cerrar puede perderlo.</p>
<p id="step-status" role="status" aria-live="polite"></p>
<button id="view-mode" type="button">Mostrar formulario completo</button>
<form id="capture" autocomplete="off" novalidate>
<fieldset id="draft"><legend>Datos de la observación</legend>
<section id="step-0">
<h2>1. Caso y objeto observado</h2>
<p>Identifica dónde y sobre qué realizaste la observación.
La versión no se incrementa automáticamente.</p>
""" + _section_inputs((
    "case_id", "observation_id", "observation_version", "subject_reference",
)) + """
</section>
<section id="step-1" hidden>
<h2>2. Responsable declarado</h2>
<p>Estos datos describen al responsable indicado; no verifican su identidad
ni le conceden autoridad.</p>
""" + _section_inputs((
    "actor_id", "customer_id", "organization_id", "role_id", "role_name",
)) + """
<label for="actor_type">Tipo de responsable declarado</label>
<select id="actor_type" required>
<option value="">Seleccionar</option>
<option value="HUMAN">Persona</option><option value="TEAM">Equipo</option>
<option value="SYSTEM">Sistema</option>
<option value="ORGANIZATION">Organización</option>
</select>
</section>
<section id="step-2" hidden>
<h2>3. Hecho, alcance y evidencia</h2>
<label for="method">¿Cómo realizaste la observación?</label>
<select id="method" required>
<option value="">Seleccionar</option>
<option value="DIRECT_INSPECTION">Inspección directa</option>
<option value="EVIDENCE_REVIEW">Revisión de evidencia</option>
</select>
<label for="description">¿Qué observaste?</label>
<p>Describe elementos, ubicación o condición visibles. Registrar una frase
no la convierte en hecho verificado ni en dictamen.</p>
<textarea id="description" rows="4" required></textarea>
<label for="scope">¿Qué parte revisaste?</label>
<textarea id="scope" rows="3" required></textarea>
<label for="limitations">¿Qué no pudiste comprobar? — una limitación por línea</label>
<textarea id="limitations" rows="3"></textarea>
<label for="evidence_ids">Referencias de evidencia — una por línea</label>
<textarea id="evidence_ids" rows="3"></textarea>
<p>Las líneas vacías se omiten. Las referencias no suben ni verifican archivos.
No registrar limitaciones no significa que no existan.</p>
</section>
<section id="step-3" hidden>
<h2>4. Fechas y envío</h2>
<p>Registra la fecha de inspección o revisión separada de la captura fotográfica.
La fecha de registro declarada no es una confirmación de COMMIT.</p>
""" + _section_inputs(("observed_at", "recorded_at")) + """
<p>Formato: AAAA-MM-DDTHH:MM:SS±HH:MM.
Se admite una fracción de segundo de hasta seis dígitos.</p>
</section>
</fieldset>
<div id="access-panel" hidden>
<label for="credential">Credencial — solo el token</label>
<input id="credential" type="password" autocomplete="off" spellcheck="false">
<p>La credencial no forma parte del borrador. Se elimina del campo al enviar.</p>
</div>
<div class="actions">
<button id="previous" type="button" hidden>Anterior</button>
<button id="next" type="button">Continuar</button>
<button id="save" type="submit" hidden>Guardar</button>
<button id="retry" type="button" disabled hidden>Reintentar envío exacto</button>
</div>
</form>
<div id="field-errors" role="alert" hidden><ul></ul></div>
<p id="status" role="status" aria-live="polite"></p>
<pre id="receipt" hidden></pre>
<a href="/inspection-observations">Consultar una versión guardada</a>
</main></body></html>
"""


SCRIPT = r"""
"use strict";
const form = document.getElementById("capture");
const draft = document.getElementById("draft");
const credential = document.getElementById("credential");
const status = document.getElementById("status");
const receipt = document.getElementById("receipt");
const saveButton = document.getElementById("save");
const retryButton = document.getElementById("retry");

let busy = false;
let lastAttempt = null;
let unconfirmed = false;
let dirty = false;
const value = id => document.getElementById(id).value;

draft.addEventListener("input", () => { dirty = true; });
draft.addEventListener("change", () => { dirty = true; });

window.addEventListener("beforeunload", event => {
    if (busy || dirty || unconfirmed) {
        event.preventDefault();
        event.returnValue = "";
    }
});
window.addEventListener("pagehide", () => { credential.value = ""; });

function asciiString(text) {
    return JSON.stringify(text).replace(/[\u007f-\uffff]/g, character =>
        "\\u" + character.charCodeAt(0).toString(16).padStart(4, "0"));
}
function canonical(item) {
    if (typeof item === "string") return asciiString(item);
    if (typeof item === "bigint") return item.toString();
    if (typeof item === "number" && Number.isSafeInteger(item))
        return String(item);
    if (item === null) return "null";
    if (Array.isArray(item)) return "[" + item.map(canonical).join(",") + "]";
    if (item && typeof item === "object")
        return "{" + Object.keys(item).sort().map(key =>
            asciiString(key) + ":" + canonical(item[key])).join(",") + "}";
    throw new Error("Tipo no admitido.");
}
function tuple(items) { return {type: "tuple", items}; }
function record(type, fields) { return {type, fields}; }
function text(id) {
    const item = value(id);
    if (!item.trim()) throw new Error("Completa los campos obligatorios.");
    return item;
}
function lines(id) {
    return value(id).split(/\r?\n/).filter(line => line.length > 0);
}
function dateValue(id) {
    const raw = text(id);
    const match = /^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d{1,6}))?(Z|[+-]\d{2}:\d{2})$/.exec(raw);
    if (!match) throw new Error("Introduce fechas completas con desplazamiento UTC.");
    let fraction = (match[2] || "").padEnd(6, "0");
    fraction = /^0+$/.test(fraction) ? "" : "." + fraction;
    const offset = ["Z", "-00:00"].includes(match[3]) ? "+00:00" : match[3];
    return {type: "datetime", iso: match[1] + fraction + offset, fold: 0, zone: null};
}

const fieldLabels = {
    case_id: "Caso",
    observation_id: "Identificador de observación",
    observation_version: "Versión",
    subject_reference: "Objeto o zona observada",
    actor_id: "Responsable declarado",
    customer_id: "Cliente u organización usuaria",
    organization_id: "Organización del responsable",
    role_id: "Identificador de función",
    role_name: "Nombre de función",
    actor_type: "Tipo de responsable",
    method: "Método",
    description: "Descripción",
    scope: "Alcance",
    observed_at: "Fecha de inspección o revisión",
    recorded_at: "Fecha de registro",
    evidence_ids: "Referencias de evidencia",
    credential: "Credencial"
};

function clearFieldErrors() {
    const box = document.getElementById("field-errors");
    box.querySelector("ul").replaceChildren();
    box.hidden = true;
    for (const id of Object.keys(fieldLabels)) {
        const field = document.getElementById(id);
        field.removeAttribute("aria-invalid");
        field.removeAttribute("aria-describedby");
    }
}
function showFieldErrors(errors) {
    clearFieldErrors();
    const box = document.getElementById("field-errors");
    const list = box.querySelector("ul");
    for (const [id, message] of errors) {
        const line = document.createElement("li");
        line.id = "error-" + id;
        line.textContent = fieldLabels[id] + ": " + message;
        list.appendChild(line);
        const field = document.getElementById(id);
        field.setAttribute("aria-invalid", "true");
        field.setAttribute("aria-describedby", line.id);
    }
    box.hidden = false;
    show("Revisa los campos indicados. El borrador se conserva.");
    revealField(errors[0][0]);
    document.getElementById(errors[0][0]).focus();
}
function validTimestamp(raw) {
    const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,6})?(Z|([+-])(\d{2}):(\d{2}))$/.exec(raw);
    if (!match) return false;
    const [year, month, day, hour, minute, second] =
        match.slice(1, 7).map(Number);
    if (year < 1 || month < 1 || month > 12 ||
        hour > 23 || minute > 59 || second > 59) return false;
    const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
    const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    if (day < 1 || day > days[month - 1]) return false;
    if (match[7] !== "Z" && (Number(match[9]) > 23 || Number(match[10]) > 59))
        return false;
    return Number.isFinite(Date.parse(raw));
}
function validateDraft() {
    const errors = [];
    for (const id of Object.keys(fieldLabels)) {
        if (["evidence_ids", "credential"].includes(id)) continue;
        if (!value(id).trim()) errors.push([id, "Completa este campo."]);
    }
    const version = value("observation_version");
    if (version.trim() && (
        !/^[1-9][0-9]*$/.test(version) || version.length > 1000
    )) errors.push(["observation_version", "Escribe un entero positivo, sin espacios ni ceros iniciales."]);

    const datesValid = {};
    for (const id of ["observed_at", "recorded_at"]) {
        datesValid[id] = validTimestamp(value(id));
        if (value(id).trim() && !datesValid[id])
            errors.push([id, "Usa una fecha válida: AAAA-MM-DDTHH:MM:SS±HH:MM."]);
    }
    // Date.parse compares to milliseconds; the server retains and validates
    // the full microsecond precision of the canonical document.
    if (datesValid.observed_at && datesValid.recorded_at &&
        Date.parse(value("recorded_at")) < Date.parse(value("observed_at")))
        errors.push(["recorded_at", "No puede ser anterior a la inspección o revisión."]);

    const references = lines("evidence_ids");
    if (value("method") === "EVIDENCE_REVIEW" && references.length === 0)
        errors.push(["evidence_ids", "Añade al menos una referencia de la evidencia revisada."]);
    else if (references.some(reference => !/[\p{L}\p{N}]/u.test(reference)))
        errors.push(["evidence_ids", "Identifica la evidencia; no uses solo signos como ---- o ..."]);
    else if (new Set(references).size !== references.length)
        errors.push(["evidence_ids", "Elimina las referencias duplicadas."]);

    if (errors.length) {
        const error = new Error("Invalid draft.");
        error.fieldErrors = errors;
        throw error;
    }
}

function prepare() {
    validateDraft();
    const version = text("observation_version");
    if (!/^[1-9][0-9]*$/.test(version) || version.length > 1000)
        throw new Error("La versión debe ser un entero positivo sin ceros iniciales.");
    const customer = text("customer_id");
    const actorType = text("actor_type");
    const method = text("method");
    const observation = {
        observation_id: text("observation_id"),
        observation_version: BigInt(version),
        case_id: text("case_id"),
        subject_reference: text("subject_reference"),
        description: text("description"),
        scope: text("scope"),
        limitations: tuple(lines("limitations")),
        evidence_ids: tuple(lines("evidence_ids")),
        observed_at: dateValue("observed_at"),
        recorded_at: dateValue("recorded_at"),
        method,
        declared_observer: record("RetailProcessActor", {
            actor_id: text("actor_id"),
            customer_id: customer,
            actor_type: {type: "ActorType", value: actorType},
            organization_id: text("organization_id"),
            role: record("RetailProcessRole", {
                role_id: text("role_id"),
                customer_id: customer,
                role_name: text("role_name")
            })
        })
    };
    const document = canonical({schema_version: 1, observation});
    return Object.freeze({
        document,
        observationId: observation.observation_id,
        version,
        url: "/v1/cases/" + encodeURIComponent(observation.case_id) +
            "/inspection-observations/" + encodeURIComponent(observation.observation_id) +
            "/versions/" + version
    });
}
function stateBusy(active) {
    busy = active;
    draft.disabled = active;
    saveButton.disabled = active;
    retryButton.disabled = active || !lastAttempt;
    updateSections();
}
function show(message) { status.textContent = message; }

async function send(attempt) {
    if (busy) return;
    let token = credential.value;
    credential.value = "";
    receipt.textContent = "";
    receipt.hidden = true;
    if (!token || !/^[\x21-\x7e]+$/.test(token)) {
        token = "";
        showFieldErrors([["credential", "Pega la clave de acceso, sin Bearer, comillas ni espacios."]]);
        return;
    }
    lastAttempt = attempt;
    unconfirmed = true;
    stateBusy(true);
    show("Enviando; el guardado todavía no está confirmado.");
    try {
        const response = await fetch(attempt.url, {
            method: "PUT",
            headers: {
                Authorization: "Bearer " + token,
                "Content-Type": "application/json",
                Accept: "application/json"
            },
            body: attempt.document,
            credentials: "omit", cache: "no-store", redirect: "error"
        });
        token = "";
        let data;
        try { data = await response.json(); }
        catch (_) {
            show("Respuesta inválida. Guardado sin confirmar; conserva el borrador y reintenta el envío exacto.");
            return;
        }
        if (response.status === 200 && data && data.status === "saved" &&
            data.observation_id === attempt.observationId &&
            data.observation_version === attempt.version) {
            unconfirmed = false;
            // If this was an older exact retry, newer draft edits remain unsaved.
            let matchesDraft = false;
            try { matchesDraft = prepare().document === attempt.document; }
            catch (_) {}
            dirty = !matchesDraft;
            show(matchesDraft
                ? "Guardado confirmado. El contenido se conserva en el formulario."
                : "Envío anterior confirmado. El borrador actual contiene cambios sin guardar.");
            receipt.textContent = "Observación: " + data.observation_id +
                "\nVersión: " + data.observation_version +
                "\nSin dictamen; responsable declarado.";
            receipt.hidden = false;
            return;
        }
        if (response.status === 409 && data && data.status === "observation_conflict") {
            unconfirmed = false;
            show("Conflicto: esa identidad y versión conservan otro contenido. El borrador se conserva; no se cambia la versión automáticamente.");
            return;
        }
        const messages = {
            400: ["invalid_request", "Documento inválido o distinto de la ruta."],
            413: ["request_too_large", "El documento supera el límite permitido."],
            415: ["unsupported_content", "Formato de envío no admitido."],
            401: ["credential_rejected", "Credencial rechazada o vencida."],
            403: ["access_denied", "Acceso denegado."],
            503: ["save_unconfirmed", "No se recibió confirmación de guardado."]
        };
        const expected = messages[response.status];
        if (expected && data && data.status === expected[0]) {
            if ([400, 413, 415].includes(response.status)) unconfirmed = false;
            show(expected[1] + (unconfirmed
                ? " Guardado sin confirmar; conserva el borrador y reintenta el envío exacto."
                : " El borrador se conserva."));
        } else {
            show("Respuesta inesperada. Guardado sin confirmar; conserva el borrador.");
        }
    } catch (_) {
        show("Error de conexión. Guardado sin confirmar; conserva el borrador y reintenta el envío exacto.");
    } finally {
        token = "";
        stateBusy(false);
    }
}
form.addEventListener("submit", event => {
    event.preventDefault();
    if (busy) return;
    receipt.textContent = "";
    receipt.hidden = true;
    clearFieldErrors();
    try {
        const attempt = prepare();
        if (unconfirmed && lastAttempt && attempt.document !== lastAttempt.document) {
            credential.value = "";
            show("Existe un envío sin confirmar. Usa Reintentar envío exacto antes de enviar cambios.");
            return;
        }
        send(attempt);
    } catch (error) {
        credential.value = "";
        if (error.fieldErrors) showFieldErrors(error.fieldErrors);
        else show(error.message + " El borrador se conserva.");
    }
});
retryButton.addEventListener("click", () => {
    if (!busy && lastAttempt) send(lastAttempt);
});


let sectionIndex = 0;
let fullForm = false;
const sectionFields = [
    ["case_id", "observation_id", "observation_version", "subject_reference"],
    ["actor_id", "customer_id", "organization_id", "role_id", "role_name", "actor_type"],
    ["method", "description", "scope", "limitations", "evidence_ids"],
    ["observed_at", "recorded_at", "credential"]
];
const previousButton = document.getElementById("previous");
const nextButton = document.getElementById("next");
const viewModeButton = document.getElementById("view-mode");

function updateSections() {
    for (let index = 0; index < sectionFields.length; index++)
        document.getElementById("step-" + index).hidden =
            !fullForm && index !== sectionIndex;
    const finalStep = fullForm || sectionIndex === 3;
    document.getElementById("access-panel").hidden = !finalStep;
    saveButton.hidden = !finalStep;
    retryButton.hidden = !finalStep;
    previousButton.hidden = fullForm || sectionIndex === 0;
    nextButton.hidden = finalStep;
    previousButton.disabled = busy;
    nextButton.disabled = busy;
    viewModeButton.disabled = busy;
    document.getElementById("step-status").textContent = fullForm
        ? "Formulario completo"
        : "Sección " + (sectionIndex + 1) + " de 4";
    viewModeButton.textContent = fullForm
        ? "Volver a captura por secciones"
        : "Mostrar formulario completo";
}
function revealField(id) {
    const index = sectionFields.findIndex(fields => fields.includes(id));
    if (!fullForm && index >= 0) {
        sectionIndex = index;
        updateSections();
    }
}
viewModeButton.addEventListener("click", () => {
    if (busy) return;
    fullForm = !fullForm;
    updateSections();
});
previousButton.addEventListener("click", () => {
    if (busy || sectionIndex === 0) return;
    clearFieldErrors();
    sectionIndex -= 1;
    updateSections();
});
nextButton.addEventListener("click", () => {
    if (busy) return;
    clearFieldErrors();
    let errors = [];
    try { validateDraft(); }
    catch (error) {
        if (!error.fieldErrors) {
            show("No se pudo validar esta sección. El borrador se conserva.");
            return;
        }
        errors = error.fieldErrors.filter(([id]) =>
            sectionFields[sectionIndex].includes(id));
    }
    if (errors.length) {
        showFieldErrors(errors);
        return;
    }
    show("");
    sectionIndex = Math.min(sectionIndex + 1, 3);
    updateSections();
});
updateSections();
"""


def install_inspection_observation_capture_page(app):
    """Expose capture only when explicitly installed by the read/write factory."""
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

    @app.get("/inspection-observations/capture", include_in_schema=False)
    def capture_page():
        return HTMLResponse(PAGE, headers=headers)

    @app.get("/inspection-observations/capture/assets/form.js", include_in_schema=False)
    def capture_script():
        return Response(SCRIPT, media_type="text/javascript", headers=headers)

    @app.get("/inspection-observations/capture/assets/form.css", include_in_schema=False)
    def capture_style():
        return Response(STYLE, media_type="text/css", headers=headers)
