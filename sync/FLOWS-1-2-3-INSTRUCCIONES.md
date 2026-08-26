# Instrucciones Power Automate - Pendientes 1, 2 y 3

Guia paso a paso. El codigo del tracker ya esta listo; falta configurar los flows.
Abrir https://make.powerautomate.com con tu cuenta.

Datos utiles:
- Site: https://intel.sharepoint.com/sites/ifs-igo-requests
- Lista: New DA Request
- Lista GUID: 052c84aa-6a91-469d-9b44-35d068acc422

=======================================================================
# PENDIENTE 1 - CIFRAR el correo de CODENAME
Flow a editar: el de envio de correos (workflow 205f9f20, el de sendEmailUrl).
=======================================================================

## Por que
El flow YA recibe Sensitivity = "Intel Confidential\Intel Employees (Encrypted - IC)"
pero Outlook NO cifra si la etiqueta llega como texto/token. Solo cifra si la
etiqueta se ELIGE del dropdown. Solucion: dos ramas.

## Pasos
1. Abre el flow -> Edit.
2. Asegura que el trigger (When an HTTP request is received) tenga en el JSON Schema:
       "sensitivity": { "type": "string" }
   (si ya lo tiene, dejalo).
3. Localiza la accion actual "Send an email (V2)". La vamos a poner dentro de una
   Condition. Lo mas facil:
   a. Agrega una accion nueva "Condition" ANTES del Send an email.
      - Lado izquierdo (fx):  triggerBody()?['sensitivity']
      - Operador: is not equal to
      - Lado derecho: dejar VACIO
   b. En la rama "If yes" (TRUE):
      - Agrega "Send an email (V2)".
      - To: en fx  triggerBody()?['to']
      - Subject: fx  triggerBody()?['subject']
      - Body: fx  triggerBody()?['bodyHtml']   (click en </> para HTML si aplica)
      - Show advanced options:
          CC: fx  triggerBody()?['cc']
          Sensitivity: ABRE EL DROPDOWN y SELECCIONA
             "Intel Confidential\Intel Employees (Encrypted - IC)"
             (seleccionar de la lista; NO escribir, NO poner token)
   c. En la rama "If no" (FALSE):
      - Agrega "Send an email (V2)" igual (To/Subject/Body/CC con los mismos fx)
      - Sensitivity: DEJAR VACIO.
   d. Si tenias un Send an email fuera de la Condition, BORRALO (ya quedan los dos
      de las ramas).
4. Guarda.

## Probar
- En el tracker: Test mode ON -> completa un Codename -> el correo debe llegar
  CIFRADO (Intel Confidential, sin poder reenviar).
- Cambia otro request a Acknowledged -> debe llegar NORMAL.

=======================================================================
# PENDIENTE 2 - ASSIGNED TO se guarde en SharePoint (campo Person)
Flow a editar: Update Fields (workflow 7c9ac8ba, el de updateFieldsUrl).
=======================================================================

## Por que
El tracker manda assignedToEmail (correo) y assignedToClaim (i:0#.f|membership|correo).
Los campos Person no siempre se llenan con "Update item". Metodo infalible:
"Send an HTTP request to SharePoint" con validateUpdateListItem.

## Pasos
1. Abre el flow -> Edit.
2. En el trigger, JSON Schema, agrega (si no estan):
       "assignedToEmail": { "type": "string" },
       "assignedToClaim": { "type": "string" }
3. Agrega una Condition (para asignar vs desasignar):
      Izquierda (fx): triggerBody()?['assignedToEmail']
      Operador: is not equal to
      Derecha: vacio
4. Rama "If yes" (asignar) -> accion "Send an HTTP request to SharePoint":
      Site Address: https://intel.sharepoint.com/sites/ifs-igo-requests
      Method: POST
      Uri (todo en una linea):
        _api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items(@{triggerBody()?['id']})/validateUpdateListItem
      Headers:
        Accept: application/json;odata=nometadata
        Content-Type: application/json
      Body:
        {
          "formValues": [
            {
              "FieldName": "iGOAdminOnly_x002d_AssignedTo",
              "FieldValue": "[{'Key':'@{triggerBody()?['assignedToClaim']}'}]"
            }
          ]
        }
5. Rama "If no" (desasignar) -> misma accion HTTP pero:
      Body:
        {
          "formValues": [
            { "FieldName": "iGOAdminOnly_x002d_AssignedTo", "FieldValue": "[]" }
          ]
        }
6. IMPORTANTE: si el flow tambien actualiza DA Link / DA Number / Portal Name en un
   "Update item", deja ESO como esta. Solo AGREGA lo de arriba para Assigned To.
   (El Assigned To por HTTP es aparte del Update item de los otros campos.)
7. Guarda.

## Probar
- En una tarjeta: boton Assign -> Jair -> Assign.
- Run history: la accion HTTP debe salir verde (200).
- En SharePoint el item debe quedar con iGO Admin - Assigned To = Jair.
- Assign -> Unassigned -> el campo se limpia.

=======================================================================
# PENDIENTE 3 - SEPARATE REQUEST (crear request nuevo solo Codename)
Flow a crear: NUEVO, "FS Tracker Create Request".
=======================================================================

## Por que
El boton "Separate request" (en tarjetas con Codename + New DA/Portal) manda datos
a un flow que debe: (a) crear un request nuevo solo Codename, y (b) quitar Codename
del original. El flow updateFieldsUrl solo actualiza, por eso hace falta uno nuevo.

## Pasos
1. Create -> Instant cloud flow -> trigger "When an HTTP request is received".
2. JSON Schema del trigger:
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
3. Accion "Create item" (SharePoint) - el request NUEVO solo Codename:
      Site Address: https://intel.sharepoint.com/sites/ifs-igo-requests
      List Name: New DA Request
      Title: fx  triggerBody()?['customer']
      RequestType: Codename
        (si RequestType es multichoice, mandar solo el valor Codename)
      Details: fx  triggerBody()?['details']
      (opcional) Project Contact / FCE Lead: usar los claim si vienen.
4. Actualizar el ORIGINAL para quitar Codename. Opcion robusta:
   "Send an HTTP request to SharePoint":
      Method: POST
      Uri:
        _api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items(@{triggerBody()?['sourceId']})/validateUpdateListItem
      Headers: Accept application/json;odata=nometadata ; Content-Type application/json
      Body (RequestType multichoice sin Codename; separar los valores como pide el
      campo choice, normalmente cada valor en el array):
        {
          "formValues": [
            { "FieldName": "RequestType", "FieldValue": "@{triggerBody()?['remainingTypes']}" }
          ]
        }
      NOTA: remainingTypes viene como "New DA;#Portal Creation". Si el campo choice
      espera otro separador, ajustar. Si se complica, primero probar con "Update item"
      y el campo RequestType multi-select.
5. (opcional) Response 200.
6. Guarda. Copia la URL del trigger (boton copiar del trigger).
7. Pasa esa URL al agente para ponerla en CONFIG.createRequestUrl del index.html
   + deploy. (O pegarla tu en index.html en la linea createRequestUrl: '...').

## Probar
- Request con Codename + New DA/Portal -> boton "Separate request" -> confirmar.
- Debe crearse un request nuevo (solo Codename) en SharePoint.
- El original queda sin Codename.
- En el siguiente Sync aparecen los dos por separado.

=======================================================================
# CAMBIO YA HECHO EN EL TRACKER (relacionado)
=======================================================================
- MRUNDA ahora es un servicio DISTINTO de MP-NDA (ya NO se agrupan). Aparece como
  su propio tipo "MRUNDA" en tarjetas, filtro de tipos y correos. (v1.8.42)
