# FS Request Tracker - PENDIENTES por resolver

Ultima actualizacion: 2026-08-20
Version actual deployada: v1.8.41

Todos estos pendientes dependen de configurar FLOWS de Power Automate (el codigo
del tracker ya esta listo). Aqui esta cada uno con su estado y que falta hacer.

>>> INSTRUCCIONES PASO A PASO DE LOS FLOWS 1, 2 y 3:
>>> sync/FLOWS-1-2-3-INSTRUCCIONES.md

============================================================
## 1) CIFRADO del correo de CODENAME  (Do Not Forward / Intel Confidential)
============================================================
ESTADO: el correo llega SIN cifrar.
CAUSA CONFIRMADA: en el Run history, el flow SI recibe
    Sensitivity = "Intel Confidential\Intel Employees (Encrypted - IC)"
pero el conector Outlook NO cifra cuando la etiqueta viene como TEXTO/expresion.
Solo cifra si la etiqueta se ELIGE del dropdown.

QUE FALTA (hacer en el flow de envio, workflow 205f9f20):
  1. Agregar una Condition antes de "Send an email (V2)":
       triggerBody()?['sensitivity']  is not equal to  (vacio)
  2. Rama TRUE (Codename): "Send an email (V2)" con To/CC/Subject/Body tokens y
     Sensitivity = ELEGIR DEL DROPDOWN "Intel Confidential\Intel Employees (Encrypted - IC)"
     (seleccionar de la lista, NO escribir texto ni token).
  3. Rama FALSE (normal): "Send an email (V2)" igual pero Sensitivity vacio.
  4. Guardar.
Detalle completo: sync/DoNotForward-setup.md
PROBAR: Test mode ON -> completar Codename -> debe llegar CIFRADO.

============================================================
## 2) ASSIGNED TO -> escribir en SharePoint (campo Person iGO Admin)
============================================================
ESTADO: al asignar desde el tracker, la tarjeta cambia al instante, pero NO
persiste en SharePoint (el campo Person no se llena).
DATO: el tracker manda bien assignedToEmail y assignedToClaim
      (i:0#.f|membership|correo). El HTTP responde 202.

QUE FALTA (en el flow Update Fields, workflow 7c9ac8ba):
  a) Confirmar en Run history si el paso "Update item" sale VERDE o ROJO.
  b) Metodo robusto (recomendado): usar "Send an HTTP request to SharePoint"
     validateUpdateListItem para el campo iGOAdminOnly_x002d_AssignedTo:
       Uri: _api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items(@{triggerBody()?['id']})/validateUpdateListItem
       Body: formValues con FieldName iGOAdminOnly_x002d_AssignedTo y
             FieldValue "[{'Key':'i:0#.f|membership|@{triggerBody()?['assignedToEmail']}'}]"
       (vacio "[]" para desasignar)
Detalle completo: sync/Assign-field-flow.md

============================================================
## 3) SEPARATE REQUEST (Codename) -> crear request nuevo en SharePoint
============================================================
ESTADO: el boton "Separate request" ya existe en la tarjeta (aparece cuando hay
Codename + New DA / Portal Creation). Al usarlo avisa que falta el flow.
FALTA: crear un flow "Create Request" y pegar su URL en CONFIG.createRequestUrl.

QUE FALTA (flow nuevo):
  - Trigger HTTP con schema: sourceId, customer, requestType, details,
    projectContactClaim, fceLeadClaim, remainingTypes.
  - Accion "Create item": crea el request nuevo SOLO con Codename (Title=customer,
    RequestType=Codename, Details).
  - Accion "Update item"/HTTP: quita Codename del request original (deja remainingTypes).
  - Copiar la URL del trigger y pasarla al agente para ponerla en
    CONFIG.createRequestUrl + deploy.
Detalle completo: sync/Separate-request-flow.md

============================================================
## 4) VERIFICAR que el flow "Get all requests" DEVUELVA estas columnas
============================================================
Para que se vean/filtren bien en el tracker, el flow de lectura debe incluir:
  - iGOAdminOnly_x002d_AssignedTo   (Assigned To - el editable)
  - Project_x0020_Contact           (Assigned BD)
  - AssignedFCELead                 (FCE Lead / Account Owner)
  - TechNode                        (para el filtro Tech Node)
  - DALink y DA_x0020_Number        (DA Link / DA Number en tarjeta)
Si alguno no aparece tras Sync, agregarlo al $select / campos del flow de lectura.

============================================================
## NOTAS
============================================================
- Todo el codigo del tracker para estos 4 puntos YA esta hecho y deployado (v1.8.41).
- Lo unico que falta es la configuracion de los flows de Power Automate (puntos 1-3)
  y verificar el flow de lectura (punto 4).
- Recordatorio: si la pagina se ve en version vieja, es cache -> Cmd+Shift+R.
