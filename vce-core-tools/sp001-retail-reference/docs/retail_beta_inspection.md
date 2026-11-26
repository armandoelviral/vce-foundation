# Beta Retail: inspección de una tienda y un corner

Base de entrega: `9d4e017bd8e67728444e6c5da2f9d661326ceb27`.
Rama de destino: `retail-beta-inspeccion`; worktree: `vce-retail-beta`.
Corrida de aceptación **SIMULADA**. Aceptación comercial en campo pendiente.

## Recorrido reutilizado y brecha cubierta

Se reutilizan captura por secciones, adjunto JPEG/PNG, envío y reintento exacto,
JWT verificado, permisos y revocación SQLite, observación canónica y recibo
atómico de SP001. `RetailRuleCriterion` y `RuleObservationStatus` representan
los criterios VM existentes. Una declaración de preparación/RACI no concede
permisos. La recuperación original del recibo pertenece al principal que lo
creó; conceder lectura al supervisor por sí solo no completa la revisión.

La nueva composición añade una asignación local inmutable con una tienda,
un corner, una revisión exacta del estándar, inspector y supervisor distintos.
El inspector primero guarda por la captura existente y después entrega el
recibo con el resultado explícito y motivo de **cada** criterio. No hay cierre
por omisión. Un resultado concluyente requiere foto; «No verificable» se
conserva como `INSUFFICIENT_EVIDENCE` y bloquea `REVIEW_ACCEPTED`.

El supervisor asignado puede recuperar el recibo del inspector y ver su foto
por la nueva ruta acotada a la asignación. Registra `FOLLOW_UP_REQUIRED` o
`REVIEW_ACCEPTED`; esta última acepta la revisión, no declara cumplimiento.
La decisión conserva principal autenticado, fecha del servidor y hash de la
entrega; ésta enlaza documento de observación, recibo, foto y asignación con
revisión exacta. Cambiar una entrega o decisión existente genera conflicto;
repetir idénticamente recupera el resultado. Una corrección posterior requiere
otra corrida: no se implementa ciclo de subsanación en esta beta.

## Aplicación y pruebas en la Mac

Descarga el parche como `retail-beta-inspeccion.patch` y aplica desde la raíz
**de este worktree**. No ejecutar en `vce-foundation`.

```bash
cd /Users/armandoelvira/dev/vce-retail-beta
[ "$(git branch --show-current)" = retail-beta-inspeccion ] &&
[ "$(git rev-parse HEAD)" = 9d4e017bd8e67728444e6c5da2f9d661326ceb27 ] &&
[ -z "$(git status --porcelain)" ] &&
git apply --check "$HOME/Downloads/retail-beta-inspeccion.patch" &&
git apply "$HOME/Downloads/retail-beta-inspeccion.patch"
```

Si las comprobaciones no pasan, detener y revisar el estado, sin reset ni stash.
Desde `vce-core-tools/sp001-retail-reference`, con Python 3.14 y dependencias
instaladas (puede usarse el intérprete del entorno existente):

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install -e '.[host,auth,dev,browser]'
.venv/bin/python -m playwright install chromium
PYTHONPATH=src:tests .venv/bin/python -m pytest -q tests/test_retail_beta_inspection.py
PYTHONPATH=src:tests:browser_tests .venv/bin/python -m pytest -q browser_tests/test_retail_beta_browser.py
PYTHONPATH=src .venv/bin/python -m pytest -q
PYTHONPATH=src:tests:browser_tests .venv/bin/python -m pytest -q browser_tests
git diff --check
```

La prueba nueva admite `SP001_TEST_CHROMIUM=/ruta/al/binario/chromium` como
alternativa explícita. Los demás tests mantienen su configuración existente.
Los archivos nuevos aparecen como no rastreados hasta `git add`; revisar también
su contenido y la lista completa de rutas antes de confirmar.

## Demostración reproducible, dos sesiones

```bash
PYTHONPATH=src .venv/bin/python -m sp001.infrastructure.retail_beta_lab --port 8768
```

El lanzador imprime una carpeta temporal protegida y la URL
`http://127.0.0.1:8768/retail-beta`. No imprime tokens. Cada ejecución crea una
base aislada; no modifica la base de laboratorio anterior. Mantener el servidor
abierto durante toda la corrida. Los tokens duran una hora; si vencen, conservar
la evidencia y repetir la corrida con nueva asignación, sin afirmar guardado.

1. Abrir la URL como inspector. Copiar el contenido de `inspector.txt` de la
   carpeta impresa, pegar en Credencial y abrir asignación.
2. Abrir «Capturar observación y foto». Usar caso `BETA-STORE-001`, solicitud
   `REQUEST-BETA-001`, observación `OBS-BETA-001`, versión `1`; completar datos
   declarados, fechas con offset y foto de prueba. Pegar credencial de inspector
   y guardar. Esperar «Guardado confirmado».
3. Volver al expediente, indicar `REQUEST-BETA-001`. R1: Discrepancia y motivo;
   R2: No verificable y motivo. Pegar credencial y entregar revisión.
4. En otro perfil de navegador o ventana privada abrir la misma URL con
   `supervisor.txt`. Recuperar expediente y comprobar estándar VM-SIMULATED,
   revisión 1, declaración de aprobación simulada y ambos criterios.
5. Volver a pegar credencial y pulsar «Ver foto». Compararla visualmente.
   Registrar «Seguimiento requerido» con motivo. Intentar aceptar todos los
   criterios no verificables debe ser rechazado.
6. Recargar en esa segunda sesión, recuperar la decisión y exportar ZIP
   con credencial de supervisor. Verificar el archivo descargado:

```bash
PYTHONPATH=src .venv/bin/python -m sp001.infrastructure.retail_beta_lab \
  --verify "$HOME/Downloads/retail-beta-expediente.zip"
```

Se espera PASS de correspondencia y la marca SIMULADO. El ZIP contiene
`dossier.json`, `standard.txt`, `photo.bin` y `manifest.json`. No contiene JWT
ni claves privadas. El verificador contrasta bytes, hashes y vínculos de
asignación, observación, criterios y decisión. El manifiesto **no está firmado**:
no demuestra procedencia contra reemplazo coordinado de todos los archivos.

Al detener con Ctrl+C se eliminan los archivos de credenciales y se conserva
la base temporal. La clave de simulación se conserva en `lab-signing-key.pem` con permisos 0600.
`--resume CARPETA` vuelve a abrir la misma base y emite credenciales de una hora
mediante nuevas concesiones registradas; no cambia el expediente. La renovación
es una intervención administrativa local explícita, no una concesión comercial.
Una implantación comercial deberá usar autoridad externa protegida.

## Administración y límites

`RetailBetaInspection.provision(assignment=...)` sólo está disponible como
configuración local de confianza; no existe endpoint para que un cliente se
autoasigne o declare aprobado un estándar. La revisión incluye documento,
SHA-256, criterios con versión, referencia de aprobación y supervisor aprobado.
Esta aprobación es una declaración registrada por el administrador, no una
firma independiente del aprobador. Una revisión VM comercial real debe ser
aportada y aprobada por el responsable antes de la aceptación en campo.

El privilegio de revisión es la combinación de principal supervisor explícito
en la asignación y permiso vigente READ_RETAIL_OBSERVATION en su caso. No es un
nuevo permiso global de supervisor ni permite mutar la observación del inspector.
El inspector usa SAVE_RETAIL_OBSERVATION. Los grants se comprueban al inicio y
al final de la transacción; la revocación posterior al snapshot de lectura rige
la siguiente petición, conforme al backend existente.

Una base contiene sólo una asignación y un expediente. Persistencia SQLite y
vínculos de integridad detectan inconsistencias parciales; no son un ledger
inmutable frente al administrador del host. No hay integración con ERP/POS,
planogramas 2D/3D, IA visual, campañas, geocerca, cámara exclusiva, modo offline,
SSO comercial ni garantías de carga. Intel permanece fuera del cambio.

El lanzador se limita a loopback HTTP; no habilita HTTPS ni acceso Android.
La prueba de navegador usa viewport móvil, no un teléfono físico. Quedan
pendientes infraestructura HTTPS, validación del dispositivo real, prueba con
estándar real y aceptación en tienda. No se declara cerrada la beta comercial.

## Resultados de esta entrega — 25 de noviembre de 2026

- CPython 3.14.10 en Linux; SQLite local; dependencias host instaladas.
- Regresión completa con `PYTHONPATH=src`: **11 979 passed**, 6 subtests,
  72.31 s. Después se agregó y pasó la prueba de rollback al vencer antes
  del commit; la batería específica final tiene **14 passed**, 1.01 s.
- Aceptación HTTP simulada con dos clientes, consulta previa de foto, decisión
  de seguimiento, recuperación y ZIP contrastado: PASS.
- Verificador CLI del ZIP: PASS. Sintaxis JavaScript: PASS con `node --check`.
- Lanzador en proceso real: HTTP 200 y limpieza de credenciales con Ctrl+C: PASS.
- Prueba nueva de navegador escrita, **pendiente de ejecución válida**. El
  intento falló antes de abrir página: Chromium no estaba instalado; su
  descarga con Playwright devolvió HTTP 403. No es aceptación visual.
  La suite completa de navegador tampoco se pudo validar aquí.
- No se ejecutó prueba en tienda ni en Android. No se modificó ni publicó
  la rama de la Mac. Se entrega parche sobre la instantánea recibida.

La primera corrida sin `PYTHONPATH=src` tuvo cinco fallos de importación en
subprocesos existentes. La repetición configurada pasó completa; no se cambió
código Intel ni se ocultaron tests para lograrlo.


## Corrección de continuidad del laboratorio — 26 de noviembre de 2026

Se conserva la misma asignación, revisión VM, observación, foto y criterios.
La reanudación requiere carpeta y base privadas del usuario, asignación simulada
exacta y concesiones previas sin revocaciones. Se detiene ante puerto ocupado,
base ausente o estándar distinto. No crea una base sustituta si `--resume` falla.
Se reserva el puerto antes de renovar y se mantiene un bloqueo durante el proceso.

Cada reanudación crea una copia consistente SQLite `backup-before-resume-*.sqlite3`,
conserva las concesiones previas y registra concesiones nuevas por una hora.
Un evento local `lab-event-*.json` registra huella de clave pública, digest de
registros de negocio y ruta de copia. Son declaraciones locales, no auditoría
inmutable ni prueba independiente contra el administrador del host.

### Corrida antigua sin clave guardada

El lanzador inicial eliminaba de memoria la clave privada y no la persistía.
No es posible recuperar esa clave ni mantener su continuidad criptográfica.
`--adopt-legacy-lab` autoriza explícitamente una nueva clave para esta simulación,
con los mismos principales declarados; no autentica retrospectivamente su autoría.
El evento se identifica como `LEGACY_KEY_ADOPTED`, nunca como continuidad de clave.
No modifica resultados ni concede permisos fuera de la asignación de prueba.
No se usa esta vía para una corrida comercial ni para restaurar un grant revocado.

Después de aplicar el parche de recuperación y pasar las pruebas, detener el
servidor anterior con Ctrl+C. En el worktree `vce-retail-beta`, ejecutar:

```bash
cd /Users/armandoelvira/dev/vce-retail-beta/vce-core-tools/sp001-retail-reference
PYTHONPATH=src \
  /Users/armandoelvira/dev/vce-foundation/vce-core-tools/.venv/bin/python \
  -m sp001.infrastructure.retail_beta_lab --port 8768 \
  --resume '/var/folders/ff/03kmd6n51vsd7jfzxnzdt7580000gn/T/sp001-retail-beta-mxhwn_c4' \
  --adopt-legacy-lab
```

Esperado: aviso de recuperación administrativa LEGACY, copia previa y carpeta.
Copiar el NUEVO `supervisor.txt` de esa carpeta y abrir una ventana privada en
`http://127.0.0.1:8768/retail-beta`. Abrir expediente, comprobar
`REQUEST-BETA-001`, R1 NON_CONFORMANT y R2 INSUFFICIENT_EVIDENCE con sus motivos
originales. Los criterios se muestran en solo lectura. Ver foto con una nueva
pegada de credencial; seleccionar Seguimiento requerido y explicar qué falta
comprobar. Volver a pegar credencial para registrar, recuperar desde otra sesión,
exportar y pasar el verificador. No volver a capturar ni entregar los criterios.

Para reanudaciones posteriores omitir `--adopt-legacy-lab`: se conserva la clave
local y aparece «Identidad de laboratorio conservada;». Los JWT vencidos siguen
rechazados; no se desactiva `exp` ni se amplía su vida. No copiar la clave privada
ni la base completa a este chat.

La interfaz ahora refleja la entrega/decisión confirmada de inmediato, muestra
los resultados registrados en solo lectura y conserva los campos ante una
consulta rechazada. Los mensajes aparecen arriba y junto a las acciones.
Los controles visuales no sustituyen las comprobaciones de autoridad del backend.

Pruebas específicas de recuperación y expediente:

```bash
PYTHONPATH=src:tests /ruta/al/python -m pytest -q \
  tests/test_retail_beta_lab_identity.py tests/test_retail_beta_inspection.py
PYTHONPATH=src:tests:browser_tests /ruta/al/python -m pytest -q \
  browser_tests/test_retail_beta_browser.py
```

Validación de la corrección en Linux/CPython 3.14.10: 23 pruebas específicas
aprobadas en 1.83 s; regresión final 11 989 passed y 6 subtests en 67.37 s.
Tres arranques reales con adopción legacy y posterior reanudación: PASS.
Se comprobó también el rechazo de una clave distinta de la última huella local.
Sintaxis JavaScript: PASS. La descarga de Chromium volvió a ser rechazada con
HTTP 403; la prueba de navegador ampliada se debe ejecutar en la Mac.
Estos resultados no constituyen aceptación comercial ni validación en campo.
