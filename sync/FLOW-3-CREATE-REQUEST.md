# FLOW 3 - Create Request (Separate) - ESTADO

Flow "FS Tracker Create Request" (workflow 589245b5). Conectado en el tracker
(CONFIG.createRequestUrl, v1.8.45+).

============================================================
## FUNCIONA (probado 2026-08-27)
============================================================
- Crea un request NUEVO con el servicio separado (Codename o IFS NDA).
- Deja el request ORIGINAL con los tipos restantes, INCLUSO VARIOS
  (ej. "New DA" + "Portal creation" juntos). El multi-valor SI funciona.
- CLAVE: hay que usar los NOMBRES EXACTOS de SharePoint (case/word sensitive):
    "New DA", "Portal creation" (c minuscula), "Code Name Request", "IFS NDA",
    "DA edit", "WebView AGS role", "MRUNDA", "MP-NDA", etc.
  El tracker ya manda requestTypeRaw (el nombre exacto), unidos por ;# .
  Ejemplo remainingTypes que SI guardo los dos: "New DA;#Portal creation".

============================================================
## PENDIENTE / BLINDAR (importante)
============================================================
Si un request NO tiene BD (Project Contact) o FCE Lead, el claim llega VACIO ("")
y el "Create item" TRUENA con:
    status 400 - "The specified user could not be found."
(visto cuando projectContactClaim / fceLeadClaim = "").

ARREGLO en el flow, paso "Create item", en los campos Person usar expresion que
mande null si viene vacio:

  Campo "Assigned FCE Lead or Account Owner Claims":
    if(empty(triggerBody()?['fceLeadClaim']), null, triggerBody()?['fceLeadClaim'])

  Campo "Assigned BD - Claims" (Project Contact):
    if(empty(triggerBody()?['projectContactClaim']), null, triggerBody()?['projectContactClaim'])

  (Opcional, si el Author tambien puede venir vacio, igual con authorClaim.)

Con eso, si falta BD o FCE Lead, crea el request sin esa persona en vez de fallar.

============================================================
## REGLA DE NEGOCIO (confirmada)
============================================================
- Codename  -> SIEMPRE en su propio request (se separa).
- IFS NDA   -> SIEMPRE en su propio request (se separa).
- New DA + Portal Creation -> se quedan JUNTOS (no se separan).
- El boton "Separate request" aparece cuando hay Codename o IFS NDA mezclado con
  otro servicio. Al darle: crea 1 request nuevo por cada standalone y deja el resto
  (New DA + Portal, etc.) en el original.

============================================================
## LIMPIEZA
============================================================
Requests de prueba creados hoy (borrar en SharePoint cuando quieras):
2713, 2714, 2715, 2716 (TEST ...).
