# FLOW 2 — Modificar "FS Tracker Update Fields" (7c9ac8ba) para guardar DA Number

Este flow es el que usa el tracker cuando capturas datos en los popups (DA Link en
"In Approval Loop", y Portal Name en "Complete"). El tracker YA manda el campo
daNumber (desde v1.8.22). Falta que el flow lo guarde en la columna DA Number.

NO crear un flow nuevo. Editar el que ya existe (workflow 7c9ac8ba).
NO cambiar la URL del flow (sigue siendo la misma).

## PASO 1 — Trigger "When an HTTP request is received"
Reemplazar el JSON Schema del body por este (agrega daNumber):

{
  "type": "object",
  "properties": {
    "id": { "type": "integer" },
    "daLinkUrl": { "type": "string" },
    "daLinkText": { "type": "string" },
    "daNumber": { "type": "string" },
    "projectPortalName": { "type": "string" }
  }
}

## PASO 2 — Accion "Update item"
Mapear los campos asi (dynamic content del trigger):
- Campo "DA Number" (DA_x0020_Number)      = daNumber
- Campo "DA Link" (DALink)                 = daLinkUrl   (SOLO la URL, nunca "url, texto")
- Campo "Project Portal Name" (Project_x002f_PortalName) = projectPortalName

  (Si el editor no muestra daNumber en dynamic content tras editar el schema,
   guarda el flow y vuelve a abrir el paso; ya deberia aparecer. O usa la expresion:
   triggerBody()?['daNumber'] )

## PASO 3 — Guardar
No tocar la URL. Probar: en el tracker, cambia un request a "In Approval Loop",
escribe una URL y un DA number en el popup, guarda. Revisa en SharePoint que
DA Link tenga la URL y DA Number tenga el numero.

## NOTA sobre no borrar campos que vienen vacios
Como el tracker a veces manda solo unos campos (ej. solo daNumber+daLinkUrl en
In Approval Loop, o solo projectPortalName en Complete), si mapeas todos directo
podrias BORRAR los que vengan vacios. Para evitarlo, lo mas simple:
- Opcion facil: dejar que Update item reciba los vacios; SharePoint normalmente
  no borra si el valor llega null/omitido... pero NO siempre. Para estar seguros:
- Opcion segura: poner una expresion "solo si viene" por campo, por ejemplo en
  DA Number:
    if(empty(triggerBody()?['daNumber']), null, triggerBody()?['daNumber'])
  y de igual forma para DALink y Project Portal Name. Asi, si un campo no viene,
  manda null y no pisa lo que ya habia.
  (Si esto se complica, se puede partir en Condiciones/updates separados. Avisar.)
