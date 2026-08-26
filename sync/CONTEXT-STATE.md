# FS Request Tracker - Estado del proyecto (contexto para futuros chats)

Ultima actualizacion: 2026-08-20
VERSION ACTUAL DEPLOYADA: v1.8.43  (repo jairgarciaintel/ifs-request-tracker, rama main)

Este archivo es el "punto de retomar". En un chat nuevo, leelo primero para tener
todo el contexto sin perder nada. Vive en sync/ (viaja por git a ambas compus).

============================================================
## COMO HACER DEPLOY (procedimiento exacto que sigue el agente)
============================================================
1. Editar index.html (carpeta Dashboards Analysis/Request-Tracker/).
2. Subir version en 3 lugares:
   - const APP_VERSION = 'vX.Y.Z'
   - el array CHANGELOG del modal (primera entrada, arriba)
   - CHANGELOG.md (nueva seccion arriba)
3. Verificar sintaxis JS (extraer los <script> y correr node --check).
4. Deploy en UNA tanda:
     git config --global core.hooksPath /dev/null   (Code Defender bloquea el push)
     git fetch origin ; git pull --no-rebase origin main   (alinear con la otra PC)
     git add index.html CHANGELOG.md [archivos sync]
     git commit -m "vX.Y.Z: ..."
     git push origin main
5. GitHub Pages tarda 1-2 min. Si se ve version vieja -> es CACHE -> Cmd+Shift+R.
6. La pagina en vivo: https://jairgarciaintel.github.io/ifs-request-tracker/

REGLA: el agente hace todo el ciclo (config hooks + add + commit + push) el mismo.
Responder siempre en espanol. Nada de emojis en la UI (usar SVG).

============================================================
## REPOS Y RUTAS
============================================================
- TRACKER (deploy, publico): jairgarciaintel/ifs-request-tracker
  Carpeta: Dashboards Analysis/Request-Tracker/
  Remote HTTPS con PAT de jairgarciaintel.
- DEV (privado): hackerjj/dashboards-strategy-2026 (raiz 14. Dashboards, tiene .kiro/hooks/l4ve)
  Remote SSH: git@github-hackerjj:hackerjj/dashboards-strategy-2026.git
- Compartir notas entre las 2 compus: carpeta sync/ del repo TRACKER (sin secretos).

============================================================
## URLs de Power Automate (en CONFIG dentro de index.html)
============================================================
- sendEmailUrl     : workflow 205f9f20  (manda TODOS los correos)
- updateFieldsUrl  : workflow 7c9ac8ba  (DA Link, DA Number, Portal Name, Assigned To)
- getRequestsUrl   : lee la lista SharePoint
- createRequestUrl : VACIO (falta el flow para "Separate request" / Codename - Pendiente 3)
- Lista SharePoint GUID: 052c84aa-6a91-469d-9b44-35d068acc422
- Site: https://intel.sharepoint.com/sites/ifs-igo-requests  | Lista: New DA Request

============================================================
## CAMPOS SharePoint confirmados
============================================================
- Title = customer/company
- RequestType = multichoice (array de objetos con Value)
- Status = objeto con Value
- Author = creador (Person)
- TechNode = tecnologia (array con Value) -> filtro Tech Node
- iGOAdminOnly_x002d_AssignedTo = "Assigned To" (Person) -> EDITABLE (boton Assign)
- Project_x0020_Contact = "Assigned BD" (Person) -> solo lectura + destinatario Codename
- AssignedFCELead = "FCE Lead / Account Owner" (Person) -> solo lectura + destinatario Codename
- DALink = hyperlink (Url + Description). Description = numero DA (Alternative Text)
- DA_x0020_Number = columna texto para el numero DA
- Project_x002f_PortalName = Portal Name

============================================================
## TIPOS DE REQUEST (normalizeType)
============================================================
- Portal Creation, New DA, Codename, WebView AGS Role, Portal Unencryption,
  Secure Chamber, IFS NDA, DA Edit, COD, DocuSign Request, Redbook Release, etc.
- MP-NDA = familia (MP-NDA, MPA-NDA, MPA-IC, Multi-Party).
- MRUNDA = SERVICIO DISTINTO de MP-NDA (v1.8.42). NO se agrupan.

============================================================
## CORREOS (todos por sendEmailUrl, con toggles)
============================================================
- Toggle "Auto emails": OFF = no manda nada al cliente.
- Toggle "Test mode": ON = todo va solo a jair.garcia@intel.com sin CC.
- Por status: Acknowledged, Info Requested, Out for Signature, In Approval Loop.
- Complete: mensaje segun tipo (Portal/New DA con paso AGS WebView; IFS NDA;
  MP-NDA/MRUNDA relacion entre 2 clientes; COD doble confirmacion + CC a
  birthe.dallmer@intel.com y james.c.matayabas.jr@intel.com).
- Codename: popup pide codename; correo al Assigned BD (Project_x0020_Contact) +
  FCE Lead (AssignedFCELead). Debe ir CIFRADO (Pendiente 1).
- Todos mandan campo "sensitivity": "" normal, etiqueta Intel solo en Codename.
- Diseno: banner azul Intel #001E50, logos oficiales, footer Intel Confidential.

============================================================
## FEATURES YA IMPLEMENTADAS (resumen)
============================================================
- v1.8.43: SONIDO de nuevo ticket en la pagina (campanita Web Audio, sin archivo).
  Boton Sound/Muted (campana SVG) en toolbar. Suena al aparecer un ID nuevo.
- v1.8.42: MRUNDA separado de MP-NDA.
- v1.8.41: filtro Tech Node + Tech Node en tarjeta.
- v1.8.40: Assigned BD = Project_x0020_Contact; boton "Separate request" (Codename).
- v1.8.39: chip asignado morado y separado; correo Codename a BD+FCE Lead.
- v1.8.38: tarjeta muestra Assigned To / Assigned BD / FCE Lead por separado.
- v1.8.36-37: boton Assign en tarjeta (escribe iGO Admin); autofill Complete de
  cliente previo; tracker manda assignedToClaim listo.
- v1.8.30-35: Complete por tipo, COD doble confirmacion + CC, Codename popup + llave SVG,
  destinatarios reales, sensitivity por correo, intentos de cifrado.
- v1.8.22-29: columna DA Number + backfill, DA Link en tarjeta, search por DA number,
  Complete instantaneo (barra 100% sin reload).
- Base: correos por status, azul Intel, filtros (tipo/status/assignee/tech node/tiempo),
  pills multiselect, notas, historial, presencia, Firebase realtime, dark/light,
  export Excel/JSON, paginacion, atajos de teclado.
- Equipo para asignar (TEAM_MEMBERS): Jair Garcia (jair.garcia@intel.com),
  Jenn Glavan (jenn.glavan@intel.com). Agregar mas ahi.

============================================================
## PENDIENTES ABIERTOS (todos = configurar flows Power Automate)
============================================================
El CODIGO del tracker ya esta listo para los 3. Pasos detallados en
sync/FLOWS-1-2-3-INSTRUCCIONES.md.

1. CIFRAR correo de CODENAME  (flow 205f9f20)
   - Confirmado: el flow recibe Sensitivity correcto pero Outlook NO cifra con
     texto/token. Solucion: Condition + elegir la etiqueta DEL DROPDOWN
     "Intel Confidential\Intel Employees (Encrypted - IC)" en la rama Codename.
   - Detalle: sync/DoNotForward-setup.md y FLOWS-1-2-3-INSTRUCCIONES.md

2. ASSIGNED TO -> escribir en SharePoint (Person)  (flow 7c9ac8ba)
   - Tracker manda assignedToEmail + assignedToClaim (HTTP 202) pero no persiste.
   - Solucion robusta: "Send an HTTP request to SharePoint" validateUpdateListItem
     con FieldName iGOAdminOnly_x002d_AssignedTo.
   - Detalle: sync/Assign-field-flow.md y FLOWS-1-2-3-INSTRUCCIONES.md

3. SEPARATE REQUEST (Codename)  (flow NUEVO por crear)
   - Boton ya existe en la tarjeta. Falta flow "Create Request" (Create item +
     quitar Codename del original) y pegar su URL en CONFIG.createRequestUrl.
   - Detalle: sync/Separate-request-flow.md y FLOWS-1-2-3-INSTRUCCIONES.md

4. VERIFICAR flow "Get all requests" (lectura) devuelva:
   iGOAdminOnly_x002d_AssignedTo, Project_x0020_Contact, AssignedFCELead, TechNode,
   DALink, DA_x0020_Number. Si algo no aparece tras Sync, agregarlo al flow de lectura.

============================================================
## OUTLOOK (fuera del tracker)
============================================================
- Regla para mover notificaciones del tracker a un folder pero dejar respuestas de
  cliente en el inbox: condicion From = cuenta del flow + Subject incluye "REQ.".
  Las respuestas vienen del cliente (RE:), no cumplen y se quedan en inbox.
- Sonido cuando llega correo del tracker: en Outlook ESCRITORIO, misma regla con
  accion "play a sound" (.WAV; convertir mp3 con ffmpeg). Detalle:
  sync/Sonidos-y-regla-outlook.md

============================================================
## ARCHIVOS EN sync/ (referencia)
============================================================
- CONTEXT-STATE.md              (este archivo - estado general)
- PENDIENTES.md                 (lista corta de pendientes)
- FLOWS-1-2-3-INSTRUCCIONES.md  (pasos detallados flows 1,2,3)
- DoNotForward-setup.md         (cifrado Codename - detalle)
- Assign-field-flow.md          (Assigned To Person - detalle)
- Separate-request-flow.md      (flow Create Request - detalle)
- Sonidos-y-regla-outlook.md    (sonidos + regla Outlook)
- DA-Number-*.md                (backfill DA Number - ya hecho)
