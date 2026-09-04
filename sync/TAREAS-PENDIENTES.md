# FS Request Tracker - TAREAS PENDIENTES (2026-09-02)

Version actual deployada: v1.8.62

============================================================
## TAREA 0 - URGENTE (4 DIAS): reglas de Firebase (Test Mode expira)
============================================================
Firebase mando aviso: la Realtime DB esta en Test Mode y las reglas EXPIRAN en
~4 dias. Cuando expiren, TODAS las peticiones se deniegan -> el tracker deja de
guardar/leer tracking, notas, historial, presencia y notificaciones.

ACCION (el usuario, en Firebase Console):
  1. Realtime Database -> pestana "Rules".
  2. Pegar la OPCION E (recomendada) o la C. Publish.

OPCION E (acotada a las 5 rutas del tracker, NO caduca):
{
  "rules": {
    "tracking":   { ".read": true, ".write": true },
    "history":    { ".read": true, ".write": true },
    "lastChange": { ".read": true, ".write": true },
    "viewing":    { ".read": true, ".write": true },
    "presence":   { ".read": true, ".write": true },
    "$other":     { ".read": false, ".write": false }
  }
}

OPCION C (abierto total, NO caduca):
{ "rules": { ".read": true, ".write": true } }

Nota: ninguna pone auth real (herramienta interna 2 personas, datos no sensibles).
Auth fuerte = otro desarrollo (login Firebase). Reglas tambien en el l4ve.
ESTADO: PENDIENTE - solo el usuario puede cambiarlas en la consola de Firebase.

Resumen: el tracker como herramienta operativa esta COMPLETO. Los pendientes
que quedan son (A) la GUIA (le faltan imagenes + agregar la seccion de correos)
y (B) los INDICADORES (necesitan un flow que traiga el HISTORIAL de SharePoint
y una grafica nueva de total por ano). Detalle abajo.

============================================================
## TAREA 1 - GUIA: imagenes faltantes + seccion de Comunicaciones
============================================================
Archivo: guide/index.html  (se ve en /ifs-request-tracker/guide/)

### 1.1 Imagenes faltantes (PENDIENTE - el usuario las va a pasar)
- La guia ya tiene los slides, pero varios usan imagenes img10-img17 que aun
  NO existen (tienen onerror para ocultarse, por eso no se ven rotas).
- El slide nuevo del Chatbot espera img12.png.
- ACCION cuando el usuario las pase: guardarlas en guide/ con esos nombres
  exactos (img10.png ... img17.png) y hacer git add + push.
- >>> RECORDATORIO AL USUARIO: pasar las capturas de pantalla de la guia. <<<

### 1.2 Agregar seccion de COMUNICACIONES (correos) a la guia  (NUEVO)
Falta un/unos slide(s) que expliquen los correos automaticos que manda el
tracker, para que Jenn/Jair sepan como se ven y cuando se disparan. Incluir:
- Cuando se manda cada correo (por status): Acknowledged, Info Requested,
  In Approval Loop, Out for Signature, IT Request Submitted, On Hold, Canceled,
  Complete.
- Complete por tipo: Portal / New DA, IFS NDA, MP-NDA.
- COD: dice que se firmo y se envio el ticket para cerrar; incluye DA Number + DA Link;
  copia a Birthe y James; saludo "Dear Team".
- DA Edit (extension): dice que el DA se extendio y que se quito el tag de COD;
  incluye DA Number + DA Link; copia a Birthe y James; saludo "Dear Team".
- Codename: correo CIFRADO (Intel Confidential, solo empleados Intel).
- Los toggles "Auto emails" y "Test mode" (Test = solo llega a Jair).

>>> IMAGENES QUE NECESITO DEL USUARIO PARA ESTA SECCION (pasarmelas): <<<
  (a) Captura de un correo Acknowledged recibido.
  (b) Captura de un correo Complete de Portal (con Portal Details / DA ID).
  (c) Captura de un correo COD completado (con DA Number + DA Link + CC Birthe/James).
  (d) Captura de un correo DA Edit / extension.
  (e) Captura de un correo Codename cifrado (el aviso de "Encrypted / Intel only").
  (f) Captura del header del tracker mostrando los toggles Auto emails y Test mode.
  Nombres sugeridos al pasarlas: mail-ack.png, mail-complete-portal.png,
  mail-cod.png, mail-daedit.png, mail-codename.png, toggles.png
  (o me las pasas como sea y yo las renombro).

ESTADO: BLOQUEADA hasta que el usuario pase las imagenes.

============================================================
## TAREA 2 - INDICADORES: historial real de SharePoint (flow nuevo)
============================================================
### El problema (por que los datos por mes NO son correctos hoy)
El tracker solo conoce el ESTADO ACTUAL de cada request (su Status de hoy).
NO conoce el HISTORIAL: cuando paso a Acknowledged, cuando paso a Complete, etc.
Por eso:
- "Completed by Month" y las SLAs de meses pasados se ESTIMAN con la fecha del
  ticket / eventos de Firebase, no con la fecha real del cambio de status.
- Si un ticket se completo en mayo, hoy no hay forma 100% confiable de saber
  que fue en mayo (solo si Firebase registro ese evento, que empezo despues).

### La solucion (el flow que se pidio en el otro chat)
Crear un flow de Power Automate que LEA EL HISTORIAL/AUDITORIA de cada item de
SharePoint y lo devuelva al tracker, para poder ubicar cada cambio de status en
su fecha real.

Opciones tecnicas para el flow (elegir la que el tenant permita):
  A) "Get changes for an item or a file (properties only)" - devuelve cambios.
  B) "Send an HTTP request to SharePoint" al endpoint de versiones:
       _api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items(ID)/versions
     Devuelve TODAS las versiones del item con su Modified y el valor de Status
     en cada version -> con eso sabes en que fecha cambio a cada status.
  C) Habilitar el historial de versiones en la lista (si no esta) para que B
     tenga datos hacia atras.

Flujo propuesto (alto nivel):
  1. Trigger HTTP (When an HTTP request is received). Opcional: recibir un rango
     de fechas o "traer todo".
  2. Get items de la lista (todos, o los del ano). $top alto + paginacion.
  3. Para cada item: HTTP a .../items(ID)/versions  -> sacar por cada version
     el Status y la fecha Modified.
  4. Construir un JSON por request con su linea de tiempo:
       { id, created, history:[ {status:"Acknowledged", date:...},
                                 {status:"Complete", date:...}, ... ] }
  5. Response 200 con ese JSON.
  6. Copiar la URL del trigger -> pasarla al agente para ponerla en
     CONFIG.historyUrl + adaptar computeIndicatorMetrics() para usar fechas
     reales por status.

CUIDADO/known issue: en este tenant el conector HTTP de O365 ya fallo llamando
APIs EXTERNAS (Firebase, error 411). PERO "Send an HTTP request to SharePoint"
es INTERNO (al propio SharePoint), asi que deberia funcionar aunque el externo no.
Hay que probarlo primero con un item.

### Objetivo 2.1 - jalar requests desde ENERO (todo el ano)
Verificar que el flow de LECTURA/HISTORIAL traiga los requests desde enero 2026
(no solo los recientes). Revisar $top/paginacion y el filtro de fecha. Hoy el
dashboard "esta padre" (ve estados, completados por mes) pero los datos por mes
no son fieles por lo del historial.

ESTADO: BLOQUEADA - falta crear el flow de historial (el que se pidio en el
otro chat) y pasarme su URL. Cuando la tenga: conecto CONFIG.historyUrl y
recalculo los meses/SLAs con fechas reales.

============================================================
## TAREA 3 - INDICADORES: grafica "Total de requests por ANO"
============================================================
Agregar, HASTA ABAJO de la vista Indicators, una grafica que muestre el total
de requests por ANO, desde el primer ano que tengamos datos en SharePoint.

Requisito clave: hay que DESCARGAR de SharePoint los requests de todos los anos
(no solo 2026). Hoy el tracker filtra/trae principalmente el ano actual, asi que:
- El flow de lectura (Get all requests) debe poder traer TODO el historico, o
- Hacer una consulta especifica agrupada por ano (year de Created).

Plan:
  1. Asegurar que el flow de lectura pueda devolver requests de anos anteriores
     (revisar filtros de fecha / $top / paginacion).
  2. En el tracker, agrupar por year(Created) y contar.
  3. Dibujar una grafica de barras "Requests by Year" al final de #view-indicators.

ESTADO: BLOQUEADA - depende de traer el historico completo desde SharePoint.
Es la mas compleja (volumen de datos + paginacion). Se hace despues de la Tarea 2.

============================================================
## ORDEN SUGERIDO
============================================================
1. Guia: en cuanto el usuario pase imagenes (Tarea 1.1) y las de correos (1.2).
2. Indicadores historial (Tarea 2): crear flow de versions de SharePoint.
3. Grafica por ano (Tarea 3): despues del flow de historico.

## LO QUE NECESITO DEL USUARIO
- [ ] URGENTE (4 dias): cambiar las reglas de Firebase (Tarea 0) en la consola.
- [ ] Imagenes de la guia (img10-img17).
- [ ] Imagenes de los correos para la seccion de Comunicaciones (lista en 1.2).
- [ ] Crear el flow de HISTORIAL de SharePoint (Tarea 2) y pasarme su URL.
- [ ] Confirmar que el flow de lectura puede traer requests desde enero / anos previos.
