# FS Request Tracker - Bugs & Feature Requests

Lista de reportes que llegan por el chatbot (correo con asunto [FS Tracker FEEDBACK]
a jair.garcia@intel.com, NO lleva "REQ." para que caiga en el inbox, no en la
carpeta de notificaciones del tracker).

Cuando llegue un reporte por correo, se anexa aqui para tenerlo en la cola de
proximos desarrollos.

Formato: fecha | quien | tipo (bug/feature) | descripcion | estado (nuevo/en progreso/hecho)

============================================================
## Cola de reportes
============================================================
(vacio por ahora - los reportes del chatbot se van anexando aqui)

============================================================
## Como funciona el chatbot (recordatorio)
============================================================
- Widget de ayuda (boton flotante abajo-derecha) en el TRACKER y en la GUIA.
- Responde dudas comunes (FAQ por palabras clave; sin IA externa, sin API key,
  sin costo, seguro para pagina publica).
- Boton "Report it": manda el bug/feature por el flow de correo existente
  (sendEmailUrl / workflow 205f9f20) a jair.garcia@intel.com.
- El asunto es "[FS Tracker FEEDBACK] ..." (sin REQ.) -> llega al inbox.
- Para agregar mas respuestas al FAQ: editar el arreglo HB_FAQ en index.html
  (y en guide/index.html si quieres que tambien responda alli).
