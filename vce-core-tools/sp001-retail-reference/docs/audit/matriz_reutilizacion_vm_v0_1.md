# Matriz de reutilización — VM Expert / SP001

**Versión 0.1 propuesta · Pendiente de validación y aprobación · 28 de octubre de 2026**

Marco neutral y multisectorial para retail y wholesale, sin marca, retailer, cliente ni destino comercial predeterminados. SP001 se analiza exclusivamente como implementación técnica candidata. Cada adopción define su ámbito, fuentes, estándares, tolerancias, autoridades, evidencias y aceptación.

## Base y significado de los estados

Esta es una matriz de diseño y brechas, basada en los archivos aportados y los resultados compartidos en la conversación. No es una nueva auditoría del repositorio actual: el repositorio del Mac no está montado aquí y no se han vuelto a ejecutar sus pruebas. Último checkpoint comunicado: `4f5ab1f`, rama `ckp010_security_boundary_foundation`, sincronizada. Resultados comunicados: **10,391 pruebas generales y 13 de navegador**, separados. El número de pruebas no mide preparación comercial ni certifica todas las reglas.

Fuentes: marco maestro «VM Expert — Retail & Wholesale» v1.0 propuesta; precisiones y Rule Contract del adjunto de las 18:19; código y salidas de pruebas compartidos previamente. Los nombres de módulos identifican candidatos conocidos; las pruebas propuestas no se presentan como archivos existentes.

- **IP parcial**: una parte delimitada tiene implementación y pruebas reportadas; no significa cumplimiento integral de la regla maestra.
- **RA**: reutilizable con adaptación; existe un componente o prototipo útil, sin control completo conectado.
- **P**: pendiente; no hay implementación operativa demostrada para este control.

## Componentes y evidencia de referencia

Todos los módulos Python están bajo `src/sp001/`, salvo indicación distinta.

| Clave | Componente existente o candidato | Evidencia y límite |
|---|---|---|
| C1 | `contracts/retail_rule_criterion.py`, `retail_rule_evaluation_record.py`, `retail_context_rule_observation.py`; `services/retail_rule_evaluation_report.py` | Identidades, criterio versionado, fundamento, actor y referencias. Reporte exige evaluaciones existentes. No valida aprobación, vigencia, contenido fotográfico ni umbrales VM. |
| C2 | `contracts/retail_inspection_preparation.py`; `tests/test_retail_inspection_preparation.py`, `test_retail_inspection_preparation_boundaries.py` | Preparación sin fabricar evaluaciones. No es motor de agregación, cobertura o cierre. Confirmar campos exactos antes de adaptar. |
| C3 | `contracts/retail_evaluator_binding.py`; `services/retail_evaluator_binding_validation.py`; `infrastructure/sqlite_retail_evaluator_bindings.py` | Vinculación principal–actor–caso, revisión, revocación, vigencia e historial. Administración de confianza, sin puerta administrativa de autorización demostrada. |
| C4 | `infrastructure/retail_report_composition.py`, `sqlite_authorized_retail_report_writer.py`, `sqlite_admitted_retail_report_writer.py`; `services/transactional_authenticated_retail_reports.py` | JWT, concesiones vigentes y admisión/reporte atómicos en SQLite; lectura en snapshot. Probados revocación, carreras, reintentos y recuperación. No implementa aprobación o cierre VM. |
| C5 | `infrastructure/retail_rule_evaluation_serialization.py`, `retail_rule_evaluation_admission_serialization.py`; `services/recovered_retail_rule_evaluation_report.py` | Serialización versionada y recuperación exacta de contenido admitido. No conserva por sí sola todo el expediente ni toda la autorización histórica. |
| C6 | `contracts/evidence_file_expectation.py`; `infrastructure/evidence_file_comparison.py`, `retail_evidence_manifest.py`; `services/retail_report_evidence_comparison.py` | Comparación acotada de bytes con tamaño/hash declarados, asociaciones a referencias y estados sin comprobar. No prueba veracidad, procedencia física ni anclaje externo. |
| C7 | `services/retail_vm_report_text.py`, `retail_vm_report_evidence_text.py`; `infrastructure/retail_vm_report_cli.py`, `retail_report_read_http_host.py`, `retail_report_host_bootstrap.py`, `retail_report_read_page.py` | Consulta/exportación autenticada, reautorización final, HTTPS de prueba y Chromium. Pruebas `browser_tests/test_retail_report_page_browser.py`, `..._failures.py`, `..._attribution.py`. Distingue declaración/admisión; no revisión independiente. |
| C8 | `contracts/retail_rule_evaluation_relation.py` y recuperación C5 | Relaciones explícitas conservan evaluaciones anteriores. No impone independencia del revisor ni autoriza un cambio de resultado. |
| C9 | `FederatedPrincipalBinding`, `infrastructure/sqlite_case_access_issuance_preparations.py` | Pruebas `test_federated_binding_subject_behavior.py`, `test_retail_evaluator_multiple_principals.py`, `test_retail_evaluator_actor_role_identity.py`. Dos cuentas pueden compartir sujeto interno; este puede cambiar de revisión. No prueba identidad humana estable. |
| C10 | `contracts/retail_context_rule_evaluation.py` y dependencias; laboratorio sintético de repetición | Disponibilidad/evaluabilidad de contexto, no cumplimiento VM. Repetición y paquete temporal reportados; no motor operativo de agregación ni reproducción histórica VM. |
| C11 | Prototipo HTML prototipo HTML visual existente | Referencia/foto, zonas, catálogo y datos manuales. Separado de SP001; historial del navegador alterable. No equivale a módulos comerciales integrados. |
| C12 | Familias existentes de digest, Merkle, checkpoint y publicación de la suite | Inventario detectó candidatos; no hay revisión completa ni integración una unidad auditada demostrada. Inspeccionar antes de construir otro registro. |

## RG-00 · Gobierno común

| Regla | Estado / componente existente | Adaptación o faltante | Prueba de aceptación pendiente | Límite de la garantía |
|---|---|---|---|---|
| G-01 Fuente | RA · C1/C2 | Fuente, aprobación y vigencia por versión exacta | Referencia no aprobada impide dictamen definitivo | Criterio versionado no acredita autoridad. |
| G-02 Alcance | RA · C2/C11 | Definir zonas, objetos y cambios autorizados | Cambio fuera de alcance queda rechazado o pendiente | No hay control geométrico conectado. |
| G-03 Sin criterios inventados | RA · C2 | Pendientes tipados y requisitos para activar regla | Campos faltantes no reciben tolerancias predeterminadas | Preparar no habilita evaluación. |
| G-04 Evidencia proporcional | RA · C1/C6 | Suficiencia por método y unidad revisada | Hash coincidente con foto ilegible no permite concluir | Identidad de bytes no es suficiencia. |
| G-05 Decisión trazable | IP parcial · C1/C5/C8 | Unir requisito, fuente, observaciones y resoluciones | Reconstruir decisión con referencias completas | Las referencias pueden no resolver a archivos. |
| G-06 Autoridad | IP parcial · C3/C4/C9 | Permisos específicos de excepción, aprobación y cierre | Invocación directa sin permiso se deniega | SAVE/READ no conceden aprobación. |
| G-07 Historial | IP parcial · C3/C4/C8 | Extender inmutabilidad a todo el expediente y revisiones | Conflicto no sobrescribe; corrección conserva original | Administrador local puede reescribir base. |
| G-08 Reconstrucción/reproducción | RA · C5/C10 | Contratos y evidencias independientes por proceso | Recuperar historia y repetir cálculo se califican separados | Juicio humano requiere concordancia aparte. |


## RG-01 · Marca y estándares visuales

| Regla | Estado / componente existente | Adaptación o faltante | Prueba de aceptación pendiente | Límite de la garantía |
|---|---|---|---|---|
| BR-01 Identidad | RA · C11/C6 | Catálogo aprobado de activos y confirmación humana | Activo correcto/incorrecto/ilegible contra versión | No hay reconocimiento visual validado. |
| BR-02 Concepto | RA · C1/C11 | Brief versionado con requisitos observables | Cada conclusión cita requisito y evidencia | Foto ilustrativa no es norma. |
| BR-03 Jerarquía | RA · C11 | Prioridades por zona y método de inspección | Comparar jerarquía con brief aprobado | No inferir intención comercial. |
| BR-04 Coherencia | RA · C1/C11 | Descomponer coherencia en condiciones verificables | Casos acordados con responsable VM | Evitar valoración estética sin criterio. |
| BR-05 Activos | RA · C6 | Derivados permitidos, medidas y transformaciones | Original y adaptación autorizada frente a alteración | Hash distinto no implica adaptación prohibida. |
| BR-06 Vigencia | RA · C2 | Periodo y aprobación de cada activo | Captura anterior/posterior a vigencia conserva incertidumbre | Fecha declarada no acredita aprobación. |


## RG-02 · Layout y espacio

| Regla | Estado / componente existente | Adaptación o faltante | Prueba de aceptación pendiente | Límite de la garantía |
|---|---|---|---|---|
| SP-01 Zonificación | RA · C11 | Persistir zonas y asignaciones versionadas | Producto y zona se vinculan a la misma referencia | Zonas visuales no son posiciones físicas medidas. |
| SP-02 Implantación | RA · C11 | Modelo de mueble, posiciones y restricciones | Plano y foto lado a lado sin mover originales | Dos dimensiones no definen la geometría completa. |
| SP-03 Circulación | P | Método físico y requisitos aplicables identificados | Medidas documentadas, evidencia insuficiente explícita | Una foto no demuestra seguridad/accesibilidad. |
| SP-04 Capacidad espacial | RA · C2/C11 | Dimensiones, ocupación y especificación técnica | Unidades compatibles y límites ausentes bloquean conclusión | No estimar capacidad desde apariencia. |
| SP-05 Proximidad comercial | P | Mapa autorizado de relaciones entre categorías | Comparación con alcance y tolerancia aprobados | No deducir impacto en ventas. |
| SP-06 Cambios layout | RA · C8/C11 | Revisiones de plano y permisos de modificación | Cambio conserva versión anterior y autorización | Relación declarada no autoriza modificación. |


## RG-03 · Presentación de producto

| Regla | Estado / componente existente | Adaptación o faltante | Prueba de aceptación pendiente | Límite de la garantía |
|---|---|---|---|---|
| PM-01 Agrupación | RA · C1/C11 | Categorías por zona y catálogo confirmado | Categoría confirmada frente a desconocida | Foto no confirma automáticamente SKU. |
| PM-02 Color | RA · C11 | Secuencia explícita y aprobación | Secuencia ausente no genera incumplimiento | No imponer preferencia cromática. |
| PM-03 Tallas | RA · C11 | Tabla SKU/talla, conteo, venta y cortes | Talla ilegible permanece sin confirmar; fuentes separadas | Una cantidad objetivo no constituye un conteo físico. |
| PM-04 Orientación | RA · C1/C11 | Requisito y visibilidad por posición | Visible/no visible y desviación según criterio | No extender muestra a prendas ocultas. |
| PM-05 Presentación | RA · C11 | Método de doblado/colgado por exhibición | Casos visuales acordados con VM | Sin criterio aprobado no hay conclusión oficial. |
| PM-06 Densidad | RA · C2 | Límite técnico, unidad, medición e instrumento | Límite kg requiere carga medida; conteo no sustituye | No inferir carga segura desde cantidad. |
| PM-07 Accesibilidad | RA · C2 | Procedimiento físico autorizado | Prueba de retiro/deslizamiento y límites documentados | Foto no acredita funcionamiento. |
| PM-08 Disponibilidad | RA · C11 | Fuentes inventario, físico, venta y tránsito | Hueco permanece; tránsito no cuenta como disponible | No hay conciliación comercial implementada. |


## RG-04 · Comunicación y POP

| Regla | Estado / componente existente | Adaptación o faltante | Prueba de aceptación pendiente | Límite de la garantía |
|---|---|---|---|---|
| VC-01 Señalización | RA · C11/C6 | Catálogo POP, ID, versión y vínculo con zona | Gráfico identificado o pendiente; referencia conservada | Presencia de marca no acredita gráfico correcto. |
| VC-02 Precios | P | Fuente comercial, moneda, producto y corte | Etiqueta se coteja con fuente del mismo contexto | No hay integración de precios. |
| VC-03 Promociones | P | Campaña, condiciones y surtido elegible | Fecha/producto fuera de campaña genera diferencia | No inferir vigencia del diseño. |
| VC-04 Legibilidad | RA · C11 | Condiciones y método de lectura definidos | Texto legible/ilegible según alcance real | No garantiza lectura desde cualquier distancia. |
| VC-05 Ubicación | RA · C11 | Posición autorizada y medidas verificadas | Zona y montaje coinciden o quedan pendientes | Dimensiones declaradas no equivalen a medidas verificadas. |
| VC-06 Retiro | P | Calendario, responsable y confirmación de retiro | Vencimiento crea pendiente, retiro exige evidencia | Fecha vencida no prueba retiro físico. |
| VC-07 Integridad gráfica | RA · C6 | Adaptaciones permitidas y activos versionados | Detectar diferencia y evaluar si está autorizada | Comparación de bytes no mide proporciones impresas. |


## RG-05 · Auditoría y cumplimiento

| Regla | Estado / componente existente | Adaptación o faltante | Prueba de aceptación pendiente | Límite de la garantía |
|---|---|---|---|---|
| AU-01 Plan | RA · C2 | Universo, selección, tamaño y posiciones excluidas | Muestra definida antes; cambios quedan versionados | No inventar mínimo universal. |
| AU-02 Cobertura | P · C2 candidato | Cálculos separados reglas/posiciones/prendas | Cero/desconocido no produce porcentaje; sin doble conteo | Muestra parcial no acredita todo el rack. |
| AU-03 Evidencia | IP parcial · C1/C6 | Vínculo persistente a archivo y requisito exacto | Referencia ausente/modificada/ilegible distinguida | Referencia opaca no prueba procedencia. |
| AU-04 Agregación | P · C1/C10 candidatos | Política versionada y resolución humana explícita | Desviación suficiente; contradicción mismo hecho; permutación | C10 calcula disponibilidad, no esta agregación. |
| AU-05 Aplicabilidad | P | Autorización por regla/alcance/versión | Sin permiso no puede declarar No aplica | Separada del resultado técnico. |
| AU-06 Criticidad | P | Matriz aprobada y bloqueos por versión | Pendiente crítico impide cierre según política | No asignar gravedad por defecto. |
| AU-07 Correctivas | RA · C11 | Persistencia, responsables, vencimientos y permisos | Cierre administrativo no completa acciones | Campos del prototipo son declarativos. |
| AU-08 Cierre | P | Decisión administrativa separada y autoridad vigente | Cierre con incumplimientos conserva resultados técnicos | No hay operación de cierre demostrada. |


## RG-06 · Evidencia y control de decisión

| Regla | Estado / componente existente | Adaptación o faltante | Prueba de aceptación pendiente | Límite de la garantía |
|---|---|---|---|---|
| EV-01 Identidad | IP parcial · C3/C4/C9 | IdP real, aprovisionamiento y persona estable | Firma/audiencia inválida; dos cuentas misma persona | JWT sintético probado no integra identidad corporativa real. |
| EV-02 Permisos | IP parcial · C4 | Extender a nuevas operaciones y API de escritura | Revocación bloquea siguiente acción directa y reintento | Garantía actual corresponde a guardar/leer reportes. |
| EV-03 Procedencia | RA · C1/C3/C5/C6 | Fuente, captura, ingreso, regla y autorización histórica | Reconstruir sin depender de lo que diga el agente | Captura y nombres siguen declarados si no se verifican. |
| EV-04 Integridad | IP parcial · C6; C12 candidato | Revisar sellado/publicación; referencia externa protegida | Alterar bytes; borrar/truncar; reescribir base contra ancla | Sin referencia externa no se detecta toda reescritura coherente. |
| EV-05 Historial | IP parcial · C3/C4/C8 | Completar eventos y autoridad administrativa | Conflictos, pérdida confirmación, caída antes/después COMMIT | Atomicidad no es inmutabilidad frente a administrador. |
| EV-06 Reconstrucción | RA · C5/C7 | Expediente completo y verificación independiente | Revisor recupera requisito/evidencia/decisión/autoridad | Admisión no demuestra toda la autorización histórica. |
| EV-07 Reproducción | RA · C10 | Paquete duradero con identidad ejecutable comprobable | Repetición en proceso separado; entrada alterada difiere | Solo laboratorio sintético de contexto demostrado. |
| EV-08 Aprobación | P · C4/C9 candidatos | Permiso específico, objeto/versión y separación funciones | Misma persona con dos cuentas no aprueba como independiente | Nombre, rol o principal distintos no prueban independencia. |
| EV-09 Cierre | P | Operación transaccional y política de bloqueos | Revocación/cambio concurrente; rechazo sin evento de cierre | No reutilizar SAVE como permiso de cerrar. |


## RG-07 · Desempeño retail y wholesale

| Regla | Estado / componente existente | Adaptación o faltante | Prueba de aceptación pendiente | Límite de la garantía |
|---|---|---|---|---|
| KP-01 Disponibilidad | RA · C11 | Conectores/cargas con SKU/talla/ubicación/corte | Mostrar físico, sistema, expuesto y tránsito separados | No sumar fuentes que se solapan. |
| KP-02 Rotación | P | Definición, unidad, periodo y fuente | Conciliar cálculo con fuente y devoluciones | Sin fuentes no hay KPI real. |
| KP-03 Sell-through | P | Ventas netas, base acordada y periodo comparable | Denominador cero; devoluciones; recepciones y cortes | Venta confirmada no prueba existencia física actual. |
| KP-04 Productividad | P | Ventas/margen y superficie medidos | Mismo periodo, moneda y alcance; sin duplicados | No atribuir resultado a VM sin diseño causal. |
| KP-05 Conversión | P | Tráfico medido y transacciones compatibles | Fuente ausente no produce tasa ni heatmap | Tránsito constante es descripción cualitativa. |
| KP-06 Ejecución VM | P · C1 candidato | Agregación aprobada y porcentaje separado | C+NC=0 no calculable; indeterminados visibles | No extender un mueble al total tienda. |
| KP-07 Reposición | P | Reglas versionadas y autorización de orden separada | Sugerencia no ejecuta compra; fuentes atrasadas advertidas | Primera tabla conjunta no genera recomendaciones automáticas. |
| KP-08 Calidad dato | RA · C11 | Fuente, corte, frecuencia, frescura y limitaciones | Dato vencido/ausente/conflictivo identificado | No anunciar tiempo real sin integración demostrada. |

## Contrato transversal propuesto y ajustes al adjunto

La arquitectura separa el núcleo de gobierno, los parámetros por implementación y los expedientes de unidades auditadas. Las diferencias de canal, sector y formato se configuran sin cambiar los principios de identidad, permisos, evidencia, historial y separación de decisiones. SKU/talla es una especialización opcional: el núcleo admite producto/variante y otras unidades de inspección. Ninguna tolerancia, criticidad o aprobación se incorpora por defecto.

La ficha Rule Contract es una especificación candidata, no un módulo implementado. Debe añadir identidad y versión propias de la regla, además de la versión de la fuente; cada aprobación debe referenciar exactamente el contenido aprobado. Los pendientes deben ser tipados y distinguir desconocido, por definir y no aplicable con fundamento; una cadena `PENDING` no debe ocupar un campo numérico o una fecha.

Mantener dimensiones independientes:

| Dimensión | Valores propuestos y condición |
|---|---|
| Aplicabilidad | Pendiente de determinar; aplicable; no aplica autorizado. La exclusión conserva fundamento y autorización. |
| Ejecución | No ejecutado; en ejecución; ejecutado. Una comprobación no realizada no crea una observación indeterminada. |
| Resultado | Pendiente; cumple; no cumple; indeterminado, con invariantes entre dimensiones. No aplica o no ejecutado no debe conservar un resultado concluyente vigente. Las revisiones históricas se preservan. |
| Evidencia | Suficiencia y contradicciones documentadas por hecho; una desviación independiente puede bastar aunque exista otra discrepancia pendiente. |
| Administración | Abierto; pendiente de resolución/autorización; cerrado con incumplimientos; cerrado sin incumplimientos, sujeto al protocolo aprobado. |
| Reproducción | No probada; probada; fallida; no aplicable justificada; siempre con proceso, versión, condiciones y evidencia. |

El ciclo DRAFT → REVIEW → APPROVED → TESTED → ACTIVE debe revisarse: aprobación y verificación son condiciones independientes. Un cambio del requisito invalida la aprobación o las pruebas afectadas según política; no basta una etiqueta TESTED histórica para activar contenido diferente. Debe contemplar también suspensión o revocación y conservar las versiones sustituidas. Este diseño no está implementado.

La expresión «método reproducible de inspección» del adjunto no garantiza repetición del juicio humano: distinguir procedimiento repetible, reproducción computacional y concordancia entre evaluadores.

El ejemplo RACK-01 del adjunto se interpreta únicamente como plantilla genérica. Toda aplicación exige una fuente identificada, versión y aprobación documentadas; no incorpora políticas particulares como reglas universales.

## Secuencia de integración propuesta para una implementación

1. **Observación real sin dictamen.** Preservar foto, referencia, alcance, fundamento, autoría declarada y fecha de revisión de una unidad auditada. Comprobar primero una representación compatible: el reporte actual exige evaluaciones con estados; no forzar CONFORMANT ni fabricar INSUFFICIENT_EVIDENCE. Registrar la fecha de revisión separada de la captura y del ingreso al sistema.
2. **Unión visual.** Comparación lado a lado, zonas persistidas y catálogo de producto/POP/mueble vinculados a la misma referencia. Guardado de borrador explícito y pruebas de pérdida de observaciones. No elevar el historial local del HTML a registro confiable.
3. **Guardado y consulta reales.** Conectar cuenta y permisos efectivos de prueba, revisar representación de la observación y recuperar el caso desde la página existente. Identidad declarada, autenticada y admisión histórica deben mostrarse de forma distinta.
4. **Tabla SKU/talla.** Físico, inventario, venta confirmada y tránsito con corte/fuente/responsable. Sin sumas, conciliaciones ni conclusiones automáticas hasta aprobar contratos y pruebas.
5. **Reglas operativas.** Agregación, cobertura, aplicabilidad, criticidad, excepciones y cierre: contratos separados, implementación y pruebas específicas antes de habilitarlos.
6. **Piloto de aceptación.** Operador real, revisión independiente con identidad y permiso adecuados, incidencias, repetición de pruebas afectadas y aceptación del responsable VM. Medir tiempo de tarea, errores, utilidad del entregable y costo de operación/integración; no atribuir mejora de ventas automáticamente.

## Evidencia que debe acompañar la aceptación

Por cada control: ID y versión de regla; commit probado; archivo y caso de prueba; tipo (unitaria/integración/navegador/operativa); insumos y expectativa; resultado y fecha; entorno; limitaciones; responsable y aprobación aplicable. Un comando con muchas pruebas aprobadas no sustituye el vínculo con el control concreto.

Pendientes de verificación documental: asociación exacta entre cada prueba y commit actual, inventario completo de mecanismos C12, revisión de VCR001 y `test_rcp001_tcp_sears_*` antes de decidir un nuevo modelo de mueble. No se ha confirmado aquí su contenido ni reutilización.

**Conclusión de alcance:** existe una base técnica reutilizable para guardar, atribuir y consultar reportes. No está demostrada todavía la operación completa de auditoría VM, aprobación/cierre, integración comercial ni resistencia frente a reescritura local contrastada externamente. Esta matriz no modifica el código, no autoriza reglas y no cambia por sí sola el porcentaje estimado del prototipo.
