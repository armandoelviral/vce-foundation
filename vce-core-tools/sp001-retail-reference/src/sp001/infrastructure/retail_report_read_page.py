from fastapi.responses import HTMLResponse, Response

PAGE = '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>Consulta autorizada de reportes VM</title>\n<link rel="stylesheet" href="/retail-reports/assets/read.css">\n<script defer src="/retail-reports/assets/read.js"></script>\n</head>\n<body>\n<main>\n<h1>Consulta de reportes VM</h1>\n<p>La consulta requiere una credencial vigente y permiso para el caso.\nEsta pantalla no guarda la credencial.</p>\n<form id="query" autocomplete="off" novalidate>\n<label for="case">Caso</label>\n<input id="case" name="case" required autocomplete="off">\n<label for="report">Reporte</label>\n<input id="report" name="report" required autocomplete="off">\n<label for="credential">Credencial — solo el token</label>\n<input id="credential" type="password" required autocomplete="off"\n       spellcheck="false">\n<div class="actions">\n<button type="submit">Consultar</button>\n<button type="button" id="clear">Borrar consulta</button>\n</div>\n</form>\n<p id="status" role="status" aria-live="polite"></p>\n<pre id="output" hidden></pre>\n</main>\n</body>\n</html>\n'

SCRIPT = '\n"use strict";\n\nconst form = document.getElementById("query");\nconst output = document.getElementById("output");\nconst status = document.getElementById("status");\nconst credential = document.getElementById("credential");\n\nlet generation = 0;\nlet active = null;\n\nfunction reset() {\n    generation += 1;\n    if (active) active.abort();\n    active = null;\n    output.textContent = "";\n    output.hidden = true;\n    status.textContent = "";\n    return generation;\n}\n\ndocument.getElementById("clear").addEventListener("click", () => {\n    reset();\n    form.reset();\n});\n\nwindow.addEventListener("pagehide", () => {\n    reset();\n    credential.value = "";\n});\n\nform.addEventListener("submit", async (event) => {\n    event.preventDefault();\n    const current = reset();\n    const caseId = document.getElementById("case").value.trim();\n    const reportId = document.getElementById("report").value.trim();\n\n    let token = credential.value;\n    credential.value = "";\n\n    if (!caseId || !reportId || !token ||\n        !/^[\\x21-\\x7e]+$/.test(token)) {\n        token = "";\n        status.textContent = "Completa caso, reporte y un token sin espacios.";\n        return;\n    }\n\n    const controller = new AbortController();\n    active = controller;\n    status.textContent = "Consultando…";\n\n    try {\n        const response = await fetch(\n            "/v1/cases/" + encodeURIComponent(caseId) +\n            "/retail-reports/" + encodeURIComponent(reportId),\n            {\n                method: "GET",\n                headers: {\n                    "Authorization": "Bearer " + token,\n                    "Accept": "application/json"\n                },\n                credentials: "omit",\n                cache: "no-store",\n                redirect: "error",\n                signal: controller.signal\n            }\n        );\n\n        token = "";\n        if (current !== generation) return;\n\n        const data = await response.json();\n        if (current !== generation) return;\n\n        if (response.status === 200 &&\n            data.status === "ok" &&\n            typeof data.report_text === "string") {\n            output.textContent = data.report_text;\n            output.hidden = false;\n            status.textContent = "Reporte recuperado.";\n            return;\n        }\n\n        const messages = {\n            401: ["credential_rejected", "Credencial rechazada o vencida."],\n            403: ["access_denied", "Acceso denegado para esta consulta."],\n            404: ["report_not_found",\n                  "Reporte no encontrado en la consulta autorizada."],\n            503: ["backend_unavailable",\n                  "No fue posible recuperar o preparar el reporte."]\n        };\n        const expected = messages[response.status];\n\n        status.textContent = expected && data.status === expected[0]\n            ? expected[1]\n            : "Respuesta inválida o inesperada. No se muestra un reporte.";\n    } catch (error) {\n        if (current !== generation) return;\n        status.textContent = error.name === "AbortError"\n            ? "Consulta cancelada."\n            : "No fue posible completar la consulta; revisa la conexión.";\n    } finally {\n        token = "";\n        if (current === generation) active = null;\n    }\n});\n'

STYLE = '\n:root { font-family: system-ui, sans-serif; color: #183247; background: #f2f5f8; }\nmain { max-width: 800px; margin: 2rem auto; padding: 1.5rem;\n       background: white; border-radius: 12px; }\nlabel { display: block; margin-top: 1rem; }\ninput { box-sizing: border-box; width: 100%; padding: .7rem; font: inherit; }\nbutton { padding: .7rem 1rem; font: inherit; cursor: pointer; }\n.actions { display: flex; gap: .7rem; margin-top: 1rem; flex-wrap: wrap; }\npre { white-space: pre-wrap; overflow-wrap: anywhere; background: #eef4f7;\n      padding: 1rem; }\n#status { min-height: 1.5rem; }\n'

def install_retail_report_read_page(app):
    """Install a public shell; report content still requires API authorization."""
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

    @app.get("/retail-reports", include_in_schema=False)
    def read_page():
        return HTMLResponse(PAGE, headers=headers)

    @app.get("/retail-reports/assets/read.js", include_in_schema=False)
    def read_script():
        return Response(
            SCRIPT, media_type="text/javascript", headers=headers,
        )

    @app.get("/retail-reports/assets/read.css", include_in_schema=False)
    def read_style():
        return Response(STYLE, media_type="text/css", headers=headers)
