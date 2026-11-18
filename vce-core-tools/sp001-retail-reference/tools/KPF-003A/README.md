# KPF-003A.1 — Modelo mínimo de alcanzabilidad

## Alcance
Reproduce de forma abstracta el ataque KPF-002A.3: no se hereda FD, pero se abre el recurso por ruta y se escribe sin autorización. La variante confinada niega la apertura por ruta.

## Ejecución
Requiere Java y tla2tools.jar (TLC). Desde este directorio:

```sh
java -cp /ruta/a/tla2tools.jar tlc2.TLC -config vulnerable.cfg KPF003A.tla
java -cp /ruta/a/tla2tools.jar tlc2.TLC -config confined.cfg KPF003A.tla
```

Se espera violación de NoUnauthorizedEffect en vulnerable.cfg, y ausencia de violaciones en confined.cfg. Un fallo del primer caso es el resultado esperado; no indica un error del archivo.

## Límites
No modela aún mediador, IPC, procesos hijos, concurrencia, revocación, namespaces, permisos OS, canales laterales, ni correspondencia formal con código real. IsolationEnabled es un supuesto abstracto, NO una prueba de aislamiento del sistema operativo. NoUnauthorizedEffect solo aplica al recurso ficticio y a las transiciones representadas. No se han ejecutado TLC ni pruebas sobre el Mac del usuario para esta entrega.

## Próximo incremento
KPF-003A.2: modelar una relación de capacidades, delegación y solicitudes al mediador; añadir un contraejemplo de confused deputy.
