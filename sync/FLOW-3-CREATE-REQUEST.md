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





https://default46c98d88e3444ed484964ed7712e25.5d.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/589245b526e14f92944fdaf82ae775b6/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=rOYFDRH4nYMNN-VVgfXai9ik1lGhX8iVb1xGxvygC08




{
    "host": {
        "connectionReferenceName": "shared_sharepointonline",
        "operationId": "HttpRequest"
    },
    "parameters": {
        "dataset": "https://intel.sharepoint.com/sites/ifs-igo-requests",
        "parameters/method": "POST",
        "parameters/uri": "_api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items(0)/validateUpdateListItem",
        "parameters/headers": {
            "Accept": "application/json;odata=nometadata",
            "Content-Type": "application/json"
        },
        "parameters/body": "{\n    \"formValues\": [\n       { \"FieldName\": \"RequestType\", \"FieldValue\": \"New DA\" }\n     ]\n}"
    }
}{
    "statusCode": 400,
    "headers": {
        "Cache-Control": "no-store, no-cache",
        "Pragma": "no-cache",
        "Set-Cookie": "ARRAffinity=ef9bdbeebd9e8fd1c371cb72cf507422b060ba0c9a7456117efdf038b6c44eb6;Path=/;HttpOnly;Secure;Domain=sharepointonline-ncus.azconn-ncus-001.p.azurewebsites.net,ARRAffinitySameSite=ef9bdbeebd9e8fd1c371cb72cf507422b060ba0c9a7456117efdf038b6c44eb6;Path=/;HttpOnly;SameSite=None;Secure;Domain=sharepointonline-ncus.azconn-ncus-001.p.azurewebsites.net",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "x-ms-request-id": "294035a2-3058-f000-2b69-eed5fc2249c7",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "x-ms-environment-id": "default-46c98d88-e344-4ed4-8496-4ed7712e255d",
        "x-ms-tenant-id": "46c98d88-e344-4ed4-8496-4ed7712e255d",
        "x-ms-subscription-id": "197bf86c-a8ec-4d89-9f88-cfbf4cdaab01",
        "x-ms-dlp-re": "HttpRequest|False|2026-08-19T22:09:34.7182410+00:00",
        "x-ms-dlp-gu": "-|-",
        "x-ms-dlp-ef": "-|-/-|-|-|-|-",
        "x-ms-mip-sl": "-|-|-|-",
        "x-ms-au-creator-id": "2729280b-5169-4c3b-84ab-a3349cb8b8e2",
        "Timing-Allow-Origin": "*",
        "x-ms-apihub-cached-response": "true",
        "x-ms-apihub-obo": "false",
        "x-ms-plex-failed": "400",
        "Date": "Thu, 27 Aug 2026 06:08:41 GMT",
        "Content-Length": "510",
        "Content-Type": "application/json",
        "Expires": "-1"
    },
    "body": {
        "status": 400,
        "message": "{\"odata.error\":{\"code\":\"-2147024809, System.ArgumentException\",\"message\":{\"lang\":\"en-US\",\"value\":\"Item does not exist. It may have been deleted by another user.\"}}}\r\nclientRequestId: 19951a0e-1de9-4f60-b74e-8621a8e46e6c\r\nserviceRequestId: 294035a2-3058-f000-2b69-eed5fc2249c7",
        "source": "https://intel.sharepoint.com/sites/ifs-igo-requests/_api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items(0)/validateUpdateListItem",
        "errors": []
    }
}ss