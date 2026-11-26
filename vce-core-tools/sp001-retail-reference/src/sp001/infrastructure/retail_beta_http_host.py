"""Beta composition: existing capture pages plus assigned criterion review."""
import json
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from sp001.infrastructure.observation_operation_http_host import create_observation_operation_app
from sp001.infrastructure.retail_beta_inspection import Conflict, Integrity, Denied, Rejected
from sp001.services.authenticated_observation_operations import AuthenticatedObservationOperations

PAGE = '''<!doctype html><html lang="es"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Beta de inspección Retail</title><script defer src="/retail-beta.js"></script>
<style>body{font:18px system-ui;max-width:850px;margin:2em auto;padding:1em}input,textarea,select,button{font:inherit;display:block;margin:.5em 0 1em;width:100%;box-sizing:border-box}fieldset{margin:1em 0}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style>
<h1>Expediente de inspección Retail</h1>
<p id="scope">La aprobación del estándar es una declaración de la administración configurada. No acredita cumplimiento ni autoría de la foto.</p>
<label>Credencial de esta acción<input id="token" type="password" autocomplete="off"></label>
<button id="load">Abrir asignación y expediente</button>
<p id="status" role="status"></p><pre id="dossier"></pre>
<a href="/inspection-observations/capture" target="_blank" rel="noopener">Capturar observación y foto</a>
<p>En Captura usa el caso de esta asignación. Conserva la solicitud mostrada en el recibo. Después vuelve aquí para registrar cada criterio.</p>
<label>Solicitud guardada<input id="request" autocomplete="off"></label>
<form id="outcomes"></form><button id="submit">Entregar revisión del inspector</button>
<button id="photo">Ver foto del expediente entregado</button>
<img id="photo-preview" hidden alt="Foto adjunta declarada por el inspector" style="max-width:100%">
<label>Decisión del supervisor<select id="action"><option value="FOLLOW_UP_REQUIRED">Seguimiento requerido</option><option value="REVIEW_ACCEPTED">Revisión aceptada (no declara cumplimiento)</option></select></label>
<label>Motivo de la decisión<textarea id="rationale"></textarea></label>
<button id="decide">Registrar decisión del supervisor</button>
<button id="export">Exportar expediente revisado</button>
<p id="action-status" role="status" aria-live="polite"></p>
<p>Vuelve a pegar la credencial antes de cada acción. No se conserva en almacenamiento del navegador. Un criterio no verificable exige seguimiento.</p></html>'''
SCRIPT = r'''"use strict";
let dossier = null;
let busy = false;
let photoUrl = null;
const el = id => document.getElementById(id);
function show(message) {
  el('status').textContent = message;
  el('action-status').textContent = message;
}
function controls() {
  for (const button of document.querySelectorAll('button')) button.disabled = busy;
  el('submit').disabled = busy || !dossier || !!dossier.submission;
  el('decide').disabled = busy || !dossier?.submission || !!dossier.decision;
  el('photo').disabled = busy || !dossier?.submission;
  el('export').disabled = busy || !dossier?.decision;
}
function clearPhoto() {
  if (photoUrl) URL.revokeObjectURL(photoUrl);
  photoUrl = null;
  el('photo-preview').hidden = true;
  el('photo-preview').removeAttribute('src');
}
async function call(action, body) {
  let token = el('token').value;
  el('token').value = '';
  if (!/^[\x21-\x7e]+$/.test(token)) throw Error('Pega una credencial sin espacios.');
  const pending = fetch('/v1/retail-beta/' + action, {
    method: body ? 'POST' : 'GET',
    headers: {Authorization:'Bearer ' + token, ...(body ? {'Content-Type':'application/json'} : {})},
    body: body ? JSON.stringify(body) : undefined,
    credentials:'omit', cache:'no-store', redirect:'error'
  });
  token = '';
  const response = await pending;
  if (!response.ok) {
    const error = await response.json();
    const messages = {
      credential_rejected:'Credencial rechazada o vencida. Requiere una credencial vigente de esta corrida.',
      conflict:'Ya existe un registro distinto. Abre el expediente para recuperar lo guardado; no cambies la solicitud.',
      access_denied:'Esta credencial no autoriza la acción. Comprueba inspector o supervisor.',
      invalid_request:'Datos no válidos para esta acción. Un criterio no verificable exige seguimiento.'
    };
    throw Error(messages[error.status] || error.status);
  }
  return response;
}
async function perform(fn) {
  if (busy) return;
  busy = true; controls();
  try {show('Procesando…'); await fn();}
  catch (error) {
    show('Acción sin confirmar: ' + error.message + ' Los campos se conservan. La vista anterior no confirma el resultado de esta acción.');
  } finally {busy = false; controls();}
}
function render(data) {
  dossier = data;
  const assignment = data.assignment;
  el('dossier').textContent = JSON.stringify(data, null, 2);
  el('scope').textContent = (assignment.simulated ? 'CORRIDA SIMULADA. Aceptación en campo pendiente. ' : 'Corrida de campo declarada. ') +
    'Caso: ' + assignment.case_id + ' | Tienda: ' + assignment.store + ' | Corner: ' + assignment.corner +
    ' | Estándar: ' + assignment.standard.standard_id + ' revisión ' + assignment.standard.revision;
  el('outcomes').replaceChildren();
  el('request').disabled = !!data.submission;
  if (data.submission) el('request').value = data.submission.receipt.request_id;
  for (const criterion of assignment.standard.criteria) {
    const field = document.createElement('fieldset');
    field.disabled = !!data.submission;
    const legend = document.createElement('legend');
    legend.textContent = criterion.rule_id + ' v' + criterion.criterion_version + ': ' + criterion.statement;
    field.append(legend);
    const select = document.createElement('select');
    select.dataset.rule = criterion.rule_id;
    select.setAttribute('aria-label', 'Resultado de ' + criterion.rule_id);
    for (const [value, label] of [['','Seleccionar'],['NON_CONFORMANT','Discrepancia'],['CONFORMANT','Conforme declarado'],['INSUFFICIENT_EVIDENCE','No verificable'],['DISPUTED','En disputa']]) {
      const option = document.createElement('option');option.value = value;option.textContent = label;select.append(option);
    }
    const note = document.createElement('textarea');
    note.placeholder = 'Sustento o razón por la que no se pudo verificar';
    note.setAttribute('aria-label','Sustento de ' + criterion.rule_id);
    const saved = data.submission?.outcomes[criterion.rule_id];
    if (saved) {select.value = saved.status;note.value = saved.rationale;}
    field.append(select,note);el('outcomes').append(field);
  }
  el('action').disabled = !!data.decision;
  el('rationale').disabled = !!data.decision;
  if (data.decision) {
    el('action').value = data.decision.action;
    el('rationale').value = data.decision.rationale;
  } else if (data.submission && Object.values(data.submission.outcomes).some(o => ['INSUFFICIENT_EVIDENCE','DISPUTED'].includes(o.status))) {
    el('action').value = 'FOLLOW_UP_REQUIRED';
  }
}
el('load').onclick = () => perform(async () => {
  // Replace the draft only after a successful read. A rejected credential preserves it.
  const data = await (await call('dossier')).json();
  clearPhoto();render(data);
  show(data.submission ? 'Expediente recuperado. Revisión del inspector registrada: criterios en solo lectura.' :
       'Expediente recuperado. La captura y el envío de criterios son pasos separados.');
});
el('submit').onclick = () => perform(async () => {
  if (!dossier || dossier.submission) throw Error('Abre el expediente y consulta la revisión registrada.');
  const outcomes = {};
  for (const field of el('outcomes').children) {
    const select = field.querySelector('select');
    outcomes[select.dataset.rule] = {status:select.value, rationale:field.querySelector('textarea').value};
  }
  const submission = await (await call('submission', {request_id:el('request').value, outcomes})).json();
  render({...dossier, submission});
  show('Revisión del inspector registrada; falta decisión del supervisor. Criterios en solo lectura.');
});
el('photo').onclick = () => perform(async () => {
  clearPhoto();const file = await (await call('photo')).blob();photoUrl = URL.createObjectURL(file);
  el('photo-preview').src = photoUrl;el('photo-preview').hidden = false;
  show('Foto recuperada para revisión; no acredita autoría.');
});
el('decide').onclick = () => perform(async () => {
  const decision = await (await call('decision', {action:el('action').value, rationale:el('rationale').value})).json();
  render({...dossier, decision});show('Decisión registrada. Recupera el expediente desde otra sesión.');
});
el('export').onclick = () => perform(async () => {
  const file = await (await call('export')).blob();const url = URL.createObjectURL(file);
  const link = document.createElement('a');link.href = url;link.download = 'retail-beta-expediente.zip';
  document.body.append(link);link.click();link.remove();setTimeout(() => URL.revokeObjectURL(url), 60000);
  show('Exportación iniciada. Comprueba el archivo con el verificador.');
});
controls();
'''


def create_retail_beta_app(*, backend, authenticator, audience, clock):
    service = AuthenticatedObservationOperations(
        authenticator=authenticator, backend=backend, expected_audience=audience, clock=clock)
    app = create_observation_operation_app(service=service, max_request_bytes=8*1024*1024)
    headers = {'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff',
               'Content-Security-Policy': "default-src 'none'; script-src 'self'; style-src 'unsafe-inline'; connect-src 'self'; img-src blob:; base-uri 'none'; frame-ancestors 'none'; form-action 'self'"}

    @app.get('/retail-beta')
    def page():
        return HTMLResponse(PAGE, headers=headers)

    @app.get('/retail-beta.js')
    def script():
        return Response(SCRIPT, media_type='text/javascript', headers=headers)

    @app.api_route('/v1/retail-beta/{action}', methods=['GET', 'POST'])
    async def workflow(action: str, request: Request):
        try:
            auth = request.headers.getlist('authorization')
            if len(auth) != 1 or not auth[0].startswith('Bearer '):
                raise Rejected('credential rejected')
            token = auth[0][7:]
            if not token or len(token) > 16384 or not token.isascii() or any(c.isspace() for c in token):
                raise Rejected('credential rejected')
            if request.url.query:
                raise ValueError('query not supported')
            if action in ('submission', 'decision') and request.method == 'POST':
                if request.headers.get('content-type') != 'application/json':
                    raise ValueError('JSON required')
                raw = bytearray()
                async for chunk in request.stream():
                    if len(raw) + len(chunk) > 65536:
                        return JSONResponse({'status':'request_too_large'}, status_code=413, headers=headers)
                    raw.extend(chunk)
                from sp001.infrastructure.observation_operation_http_host import _unique_object
                data = json.loads(raw, object_pairs_hook=_unique_object,
                                  parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
                if type(data) is not dict:
                    raise ValueError('object required')
                expected = {'request_id','outcomes'} if action == 'submission' else {'action','rationale'}
                if set(data) != expected:
                    raise ValueError('unexpected fields')
                method = backend.submit if action == 'submission' else backend.decide
                from starlette.concurrency import run_in_threadpool
                result = await run_in_threadpool(method, credential=token, **data)
            elif action == 'dossier' and request.method == 'GET':
                from starlette.concurrency import run_in_threadpool
                result = await run_in_threadpool(backend.recover, credential=token)
            elif action == 'photo' and request.method == 'GET':
                from starlette.concurrency import run_in_threadpool
                from PIL import Image
                from io import BytesIO
                data = await run_in_threadpool(backend.photo, credential=token)
                with Image.open(BytesIO(data)) as image:
                    media_type = {'JPEG':'image/jpeg', 'PNG':'image/png'}[image.format]
                return Response(data, media_type=media_type, headers=headers)
            elif action == 'export' and request.method == 'GET':
                from starlette.concurrency import run_in_threadpool
                data = await run_in_threadpool(backend.export, credential=token)
                return Response(data, media_type='application/zip', headers={**headers,
                    'Content-Disposition':'attachment; filename="retail-beta-expediente.zip"'})
            else:
                return JSONResponse({'status':'not_found'}, status_code=404, headers=headers)
            return JSONResponse(result, headers=headers)
        except Rejected:
            code, status = 401, 'credential_rejected'
        except Denied:
            code, status = 403, 'access_denied'
        except Conflict:
            code, status = 409, 'conflict'
        except Integrity:
            code, status = 503, 'integrity_failure'
        except (ValueError, TypeError, UnicodeError):
            code, status = 400, 'invalid_request'
        except Exception:
            code, status = 503, 'outcome_unknown'
        return JSONResponse({'status':status}, status_code=code, headers=headers)
    return app
