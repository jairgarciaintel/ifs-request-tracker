# FS Request Tracker - Estado del proyecto (contexto para futuros chats)

Ultima actualizacion: 2026-08-20
VERSION ACTUAL DEPLOYADA: v1.8.41  (commit 33a4000, repo jairgarciaintel/ifs-request-tracker)

## Como se trabaja (recordatorio operativo)
- El agente hace: editar index.html, subir version (APP_VERSION + array CHANGELOG
  del modal + CHANGELOG.md), verificar sintaxis (node --check sobre los <script>),
  git config core.hooksPath /dev/null + add + commit + push. En una sola tanda.
- Antes de push: git fetch/pull para alinear (las dos PCs suben commits).
- GitHub Pages tarda 1-2 min; si se ve version vieja es CACHE -> Cmd+Shift+R.
- Scripts/instrucciones largas para Power Automate: van en sync/*.md (viajan por git).
  NUNCA poner URLs firmadas (?sig=) en el repo publico salvo las ya presentes en CONFIG.

## URLs de Power Automate (en CONFIG dentro de index.html)
- sendEmailUrl     : workflow 205f9f20  (manda TODOS los correos)
- updateFieldsUrl  : workflow 7c9ac8ba  (actualiza campos: DA Link, DA Number, Portal Name, Assigned To)
- getRequestsUrl   : lee la lista SharePoint
- createRequestUrl : VACIO (falta crear flow para "Separate request" / Codename)
- Lista SharePoint GUID: 052c84aa-6a91-469d-9b44-35d068acc422

## Campos SharePoint confirmados (del debug de items reales)
- Title = customer / company
- RequestType = multichoice (array de objetos con Value)
- Status = objeto con Value
- Author = creador (Person, trae Email/Claims)
- TechNode = tecnologia (array de objetos con Value) -> filtro Tech Node
- iGOAdminOnly_x002d_AssignedTo = "Assigned To" (Person) -> EDITABLE desde el tracker (boton Assign)
- Project_x0020_Contact = "Assigned BD" (Person) -> solo lectura + destinatario Codename
- AssignedFCELead = "FCE Lead / Account Owner" (Person) -> solo lectura + destinatario Codename
- DALink = hyperlink (Url + Description). Description = numero DA (Alternative Text)
- DA_x0020_Number = columna texto para el numero DA (backfill hecho por flow)
- Project_x002f_PortalName = Portal Name

## Correos (todos por sendEmailUrl, con toggles)
- Toggle "Auto emails": OFF = no manda nada al cliente.
- Toggle "Test mode": ON = todo va solo a jair.garcia@intel.com sin CC.
- Correos por status: Acknowledged, Info Requested, Out for Signature, In Approval Loop.
- Complete: popup segun tipo (Portal/New DA vs IFS NDA vs MP-NDA vs COD). COD copia a
  birthe.dallmer@intel.com y james.c.matayabas.jr@intel.com, popup de doble confirmacion.
- Codename: popup pide el codename, correo va al Assigned BD (Project_x0020_Contact) +
  FCE Lead (AssignedFCELead). Debe ir CIFRADO (ver pendiente abajo).
- Todos mandan campo sensitivity: "" normal, etiqueta Intel solo en Codename.

## PENDIENTES ABIERTOS (importante)
1. CIFRADO CODENAME (no resuelto - depende del flow):
   - CONFIRMADO: el flow recibe Sensitivity = "Intel Confidential\Intel Employees (Encrypted - IC)"
     pero el correo llega SIN cifrar.
   - CAUSA: el conector Outlook NO aplica la etiqueta si viene como texto/expresion.
   - SOLUCION (el usuario debe hacerla en el flow): Condition + elegir la etiqueta
     del DROPDOWN en la rama Codename. Detalle en sync/DoNotForward-setup.md.

2. ASSIGNED TO -> SharePoint (Person) no persistia:
   - El tracker manda assignedToEmail + assignedToClaim (i:0#.f|membership|correo). HTTP 202.
   - El flow "Update item" no siempre resuelve Person. Metodo robusto:
     "Send an HTTP request to SharePoint" validateUpdateListItem. Detalle en
     sync/Assign-field-flow.md. Falta confirmar si el paso sale verde/rojo.

3. SEPARATE REQUEST (Codename): boton ya existe en el tracker. Falta crear el flow
   "Create Request" (createRequestUrl vacio). Detalle en sync/Separate-request-flow.md.

## FEATURES YA HECHAS (v1.8.x recientes)
- v1.8.41: filtro Tech Node en toolbar + Tech Node en tarjeta.
- v1.8.40: Assigned BD = Project_x0020_Contact; boton Separate request (Codename).
- v1.8.39: chip asignado morado y separado; correo Codename a BD+FCE Lead.
- v1.8.38: tarjeta muestra Assigned To / Assigned BD / FCE Lead por separado.
- v1.8.37: tracker manda assignedToClaim listo.
- v1.8.36: boton Assign en tarjeta + autofill Complete de cliente previo.
- v1.8.35: sensitivity explicito por correo.
- v1.8.30-34: Complete por tipo, COD doble confirmacion + CC, Codename popup + SVG llave,
  destinatarios reales, intentos de cifrado.
- v1.8.22-29: DA Number (columna + backfill), DA Link en tarjeta, search por DA number,
  Complete instantaneo (barra 100% sin reload).
- Antes: correos Acknowledged/Info/OutForSignature/InApprovalLoop, azul Intel #001E50,
  logos oficiales, filtros, pills, notas, historial, presencia, Firebase realtime.

## Equipo para asignar (TEAM_MEMBERS en index.html)
- Jair Garcia (jair.garcia@intel.com), Jenn Glavan (jenn.glavan@intel.com).
  Agregar mas ahi si hace falta.
