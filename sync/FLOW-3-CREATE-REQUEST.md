# FLOW 3 - Create Request (Separate Codename) - pasos completos

Flow NUEVO: "FS Tracker Create Request". El boton "Separate request" del tracker
(en requests con Codename + New DA/Portal) lo llama. Hace 2 cosas:
  1. Crea un request NUEVO solo con Codename (copiando 3 campos de personas del original).
  2. Quita Codename del request original.

El tracker manda este payload (ya deployado v1.8.44):
{
  "sourceId": 2712,
  "customer": "Ahead Computing Inc.",
  "requestType": "Codename",
  "details": "...",
  "authorClaim": "i:0#.f|membership|<creador original>",       (Created By)
  "authorEmail": "<creador original>",
  "projectContactClaim": "i:0#.f|membership|<assigned BD>",     (Assigned BD)
  "projectContactEmail": "<assigned BD>",
  "fceLeadClaim": "i:0#.f|membership|<fce lead>",               (FCE Lead/Owner)
  "fceLeadEmail": "<fce lead>",
  "remainingTypes": "New DA;#Portal Creation"
}

============================================================
PASO 1 - Crear el flow  (YA HECHO)
============================================================
Instant cloud flow -> "When an HTTP request is received".

============================================================
PASO 2 - JSON Schema del trigger
============================================================
{
  "type": "object",
  "properties": {
    "sourceId": { "type": "integer" },
    "customer": { "type": "string" },
    "requestType": { "type": "string" },
    "details": { "type": "string" },
    "authorClaim": { "type": "string" },
    "authorEmail": { "type": "string" },
    "projectContactClaim": { "type": "string" },
    "projectContactEmail": { "type": "string" },
    "fceLeadClaim": { "type": "string" },
    "fceLeadEmail": { "type": "string" },
    "remainingTypes": { "type": "string" }
  }
}

============================================================
PASO 3 - Crear el request nuevo (solo Codename) + copiar los 3 campos de personas
============================================================
OJO con Created By (Author): el "Create item" normal NO deja poner el Author
(lo pone automatico = la cuenta del flow). Para copiar el Created By del original
hay que usar "Send an HTTP request to SharePoint" (validateUpdateListItem) despues
de crear, o crear y luego setear Author por HTTP. Se hace en 2 sub-pasos:

3a. Accion "Create item" (SharePoint):
    Site Address: https://intel.sharepoint.com/sites/ifs-igo-requests
    List Name: DA Ops Requests
    Title:        triggerBody()?['customer']
    RequestType:  Codename   (si es multichoice, solo el valor Codename)
    Details:      triggerBody()?['details']
    Project Contact (Assigned BD) Claims: triggerBody()?['projectContactClaim']
    AssignedFCELead Claims:               triggerBody()?['fceLeadClaim']
    -> guarda el ID que devuelve (lo usa 3b). Se llama outputs del Create item: ID.

3b. Copiar el Created By (Author) del original con HTTP:
    Accion "Send an HTTP request to SharePoint":
      Method: POST
      Uri:
        _api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items(@{outputs('Create_item')?['body/ID']})/validateUpdateListItem
      Headers:
        Accept: application/json;odata=nometadata
        Content-Type: application/json
      Body:
        {
          "formValues": [
            { "FieldName": "Author", "FieldValue": "[{'Key':'@{triggerBody()?['authorClaim']}'}]" }
          ]
        }
    NOTA: si "Author" no deja escribirse, algunas listas exponen el creador como
    "Created By" con otro internal name; si falla, dime el error y ajustamos.
    (Assigned BD y FCE Lead ya se pusieron en 3a; si prefieres, tambien se pueden
     setear aqui por HTTP con sus FieldName: Project_x0020_Contact y AssignedFCELead.)

============================================================
PASO 4 - Quitar Codename del request ORIGINAL
============================================================
Accion "Send an HTTP request to SharePoint":
    Method: POST
    Uri:
      _api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items(@{triggerBody()?['sourceId']})/validateUpdateListItem
    Headers: Accept application/json;odata=nometadata ; Content-Type application/json
    Body (RequestType sin Codename; remainingTypes viene "New DA;#Portal Creation"):
      {
        "formValues": [
          { "FieldName": "RequestType", "FieldValue": "@{triggerBody()?['remainingTypes']}" }
        ]
      }
    NOTA: si RequestType multichoice necesita otro formato para varios valores,
    probar primero con "Update item" y el campo multi-select; si falla, ajustamos.

============================================================
PASO 5 - Response 200 (opcional) + Guardar + copiar URL del trigger
============================================================
Copia la URL del trigger y pegala en index.html:  CONFIG.createRequestUrl = '...'
(o pasamela y la pongo + deploy).

============================================================
PROBAR
============================================================
- Request con Codename + New DA/Portal -> boton "Separate request" -> confirmar.
- Se crea un request nuevo (solo Codename) con el MISMO Created By, Assigned BD y
  FCE Lead que el original.
- El original queda sin Codename.
- En el siguiente Sync aparecen los dos por separado.
