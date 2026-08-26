# Separar Codename en su propio request (boton "Separate request")

## Que hace el tracker (ya deployado)
- Cuando un request trae Codename JUNTO con New DA / Portal Creation, aparece un
  boton naranja: "Separate request - move Codename to its own request".
- Al darle clic (y confirmar), el tracker llama a un flow NUEVO (createRequestUrl)
  con este payload:
    {
      "sourceId": 27078,
      "customer": "Nombre empresa",
      "requestType": "Codename",
      "details": "…",
      "projectContactClaim": "i:0#.f|membership|correo",   (puede venir vacio)
      "fceLeadClaim": "i:0#.f|membership|correo",           (puede venir vacio)
      "remainingTypes": "New DA;#Portal Creation"
    }

## Falta: crear el flow "Create Request" en Power Automate
El flow updateFieldsUrl solo ACTUALIZA. Para crear un request nuevo hace falta un
flow con accion "Create item".

### Paso 1 - trigger HTTP
"When an HTTP request is received". JSON Schema:
    {
      "type":"object",
      "properties":{
        "sourceId":{"type":"integer"},
        "customer":{"type":"string"},
        "requestType":{"type":"string"},
        "details":{"type":"string"},
        "projectContactClaim":{"type":"string"},
        "fceLeadClaim":{"type":"string"},
        "remainingTypes":{"type":"string"}
      }
    }

### Paso 2 - Create item (el request NUEVO, solo Codename)
Accion SharePoint "Create item":
  - Site Address: https://intel.sharepoint.com/sites/ifs-igo-requests
  - List Name: New DA Request
  - Title: triggerBody()?['customer']
  - RequestType: Codename   (si es choice multiple, mandar solo Codename)
  - Details: triggerBody()?['details']
  - (opcional) Project Contact / FCE Lead: usar los claim si vienen.
  Guarda el ID nuevo que devuelve (lo usa el mensaje de vuelta, opcional).

### Paso 3 - Actualizar el request ORIGINAL (quitar Codename)
Accion "Update item" sobre sourceId:
  - RequestType = remainingTypes  (New DA / Portal Creation, sin Codename)
  Si RequestType es choice multiple, hay que mandar el array sin Codename. La
  forma robusta es "Send an HTTP request to SharePoint" validateUpdateListItem
  poniendo RequestType con los valores de remainingTypes (separados como pide el
  campo). Si se complica, primero probar Update item con el multi-choice.

### Paso 4 - Response 200 (opcional) y guardar. Copiar la URL del trigger.

## Conectar en el tracker
Pega la URL del trigger en index.html:
    CONFIG.createRequestUrl = 'https://...&sig=...'
(igual que hicimos con updateFieldsUrl). Avisar y la conecto + deploy.

## Probar
1. Un request con Codename + New DA/Portal -> abrelo -> boton "Separate request".
2. Confirmar. Debe crear un request nuevo (solo Codename) en SharePoint.
3. El original debe quedar sin Codename (solo New DA / Portal Creation).
4. En el siguiente Sync del tracker aparecen los dos por separado.

## Nota importante
Mientras CONFIG.createRequestUrl este vacio, el boton avisa que el flow no esta
configurado (no rompe nada). En cuanto pegues la URL, funciona.
