# DA Number — Estrategia y flows de Power Automate (v2, fix GUID)

## Contexto
La columna "DA Link" es un Hyperlink de DOS partes:
- Url (arriba, azul): https://hsdes.intel.com/appstore/DMS/ticket/XXXXX
- Description / Alternative Text (abajo): el DA number, ej. 4566, 19381
El flow "Get all requests" (88801fb7...) aplana el hyperlink y solo trae la URL.

## Objetivo
1) BACKFILL (una vez): copiar Description (numero) de "DA Link" -> columna
   "DA Number" (DA_x0020_Number) para toda la lista, solo cuando exista Description.
2) De aqui en adelante: mapear daNumber -> DA_x0020_Number en el flow Update Fields.
REGLA: si no hay Description, dejar DA Number vacio.

## FLOW 1 — BACKFILL "FS Tracker Backfill DA Number" (correr UNA vez)

PASO 1 — Trigger: "Manually trigger a flow".

PASO 2 — "Send an HTTP request to SharePoint"
  Site Address: https://intel.sharepoint.com/sites/ifs-igo-requests
  Method: GET
  Uri (USAR GUID, el nombre por titulo FALLO con "List 'New DA Request' does not exist"):
    _api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items?$select=Id,DALink&$top=5000
  Headers: Accept = application/json;odata=nometadata
  (El GUID 052c84aa-6a91-469d-9b44-35d068acc422 salio del debug del item 2689.)

PASO 3 — "Parse JSON"
  Content: dynamic content -> Body (NO texto). Schema: value[] con Id y DALink{Description,Url}.

PASO 4 — "Apply to each" + Condition + Update item
  4a) Apply to each -> output (fx): body('Parse_JSON')?['value']
  4b) Condition (UNA fila; borrar la 2a):
      Izq (fx): item()?['DALink']?['Description']
      Op: is not equal to      Der: VACIO
  4c) Update item (rama TRUE):
      Site: https://intel.sharepoint.com/sites/ifs-igo-requests
      List Name: New DA Request (o del dropdown)
      Id (fx): item()?['Id']
      DA Number (DA_x0020_Number) (fx): item()?['DALink']?['Description']

PASO 5 — Guardar, Test -> Manually -> Run. Verificar 3-4 (2692 -> 19381).
  Prueba: cambiar &$top=5000 por &$top=3, correr, revisar, regresarlo.

## FLOW 2 — AJUSTE a "FS Tracker Update Fields" (7c9ac8ba...) — requests nuevos
1. Trigger JSON Schema: agregar "daNumber": { "type": "string" }
2. Update item: DA Number (DA_x0020_Number) = daNumber ; DA Link (DALink) = SOLO daLinkUrl.
3. Guardar. NO cambiar la URL.

NOTA: la Uri con getbytitle('New DA Request') FALLO. Usar el GUID de arriba.
