# DA Number — Estrategia y flows de Power Automate

## Contexto (confirmado con debugReq(2689) + fotos de SharePoint)
La columna "DA Link" de la lista New DA Request es un Hyperlink de DOS partes:
- Url (arriba, azul): https://hsdes.intel.com/appstore/DMS/ticket/XXXXX
- Description / Alternative Text (abajo): el DA number, ej. 4566, 19381

El flow "Get all requests" (workflow 88801fb7...) APLANA el hyperlink y solo devuelve
la URL como string (DALink: "https://..."), por eso el numero (Description) nunca llega
al tracker. En la vista de lista, los requests sin URL muestran solo el numero como
texto del link.

## Objetivo
1) BACKFILL (una sola vez): copiar el Description (numero) de "DA Link" a la nueva
   columna "DA Number" (internal name DA_x0020_Number) para TODA la lista existente,
   solo cuando exista Description.
2) DE AQUI EN ADELANTE: el popup del tracker ya manda daNumber (v1.8.22). Falta mapear
   daNumber -> DA_x0020_Number en el flow "FS Tracker Update Fields" (7c9ac8ba...).

REGLA: si un request no tiene Description (solo URL o nada), dejar DA Number vacio.

## FLOW 1 — BACKFILL "FS Tracker Backfill DA Number" (correr UNA vez)
El conector "Get items" tambien aplana el hyperlink. Para leer Url + Description hay
que usar "Send an HTTP request to SharePoint" (SharePoint REST), que devuelve el campo
completo.

1. Trigger: "Manually trigger a flow" (Instant cloud flow).

2. Accion "Send an HTTP request to SharePoint":
   - Site Address: https://intel.sharepoint.com/sites/ifs-igo-requests
   - Method: GET
   - Uri:
     _api/web/lists/getbytitle('New DA Request')/items?$select=Id,DALink&$top=5000
   - Headers:
     Accept = application/json;odata=nometadata
   NOTA: si hay mas de 5000 items, hay que paginar con $skiptoken. Avisar y se ajusta.

3. Accion "Parse JSON":
   - Content: body de la accion anterior
   - Schema:
   {
     "type": "object",
     "properties": {
       "value": {
         "type": "array",
         "items": {
           "type": "object",
           "properties": {
             "Id": { "type": "integer" },
             "DALink": {
               "type": ["object", "null"],
               "properties": {
                 "Description": { "type": ["string", "null"] },
                 "Url": { "type": ["string", "null"] }
               }
             }
           }
         }
       }
     }
   }

4. "Apply to each" sobre  body('Parse_JSON')?['value']:
   - Condicion: item()?['DALink']?['Description']  is not equal to  (vacio)
     (y que no sea null). Solo backfillear cuando hay numero.
   - Si TRUE -> "Update item" (SharePoint):
       Site Address: https://intel.sharepoint.com/sites/ifs-igo-requests
       List Name: New DA Request
       Id: item()?['Id']
       Campo "DA Number" (DA_x0020_Number): item()?['DALink']?['Description']

5. Guardar. Correr UNA vez.
   - Verificar 3-4 items: el 2692 debe quedar con 19381, el de 4566, etc.
   - Si algo sale raro, NO re-correr; avisar.

## FLOW 2 — AJUSTE a "FS Tracker Update Fields" (7c9ac8ba...) para requests nuevos
1. Trigger (When an HTTP request is received): agregar daNumber al JSON Schema:
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
2. En "Update item":
   - Campo "DA Number" (DA_x0020_Number) = dynamic content  daNumber
   - Campo "DA Link" (DALink) = SOLO  daLinkUrl  (URL sola; nunca "url, texto",
     por eso daba el error String/uri).
3. Guardar. NO cambiar la URL del flow (sigue siendo workflow 7c9ac8ba...).

## PENDIENTE / verificacion
- Confirmar que el internal name de la columna nueva es exactamente DA_x0020_Number.
  Si "Update item" no encuentra el campo, revisar en List settings > columna DA Number
  > la URL trae Field=... con el internal name real.


========================================================================
PASO 2 — Send an HTTP request to SharePoint (copiar/pegar exacto)
========================================================================

Site Address:
https://intel.sharepoint.com/sites/ifs-igo-requests

Method:
GET

Uri:
_api/web/lists/getbytitle('New DA Request')/items?$select=Id,DALink&$top=5000

Headers (key / value):
Accept    application/json;odata=nometadata
