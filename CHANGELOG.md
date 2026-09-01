# FS Request Tracker — Changelog

Control de versiones del tracker. La version actual se muestra en el header
de la pagina (esquina). Cuando GitHub Pages ya tiene la nueva version, el
numero cambia — asi sabes que el deploy ya subio.

Formato: vMAJOR.MINOR — fecha — cambios.

---

## v1.8.58 — 2026-09-01
- Tab Indicators: nueva tira "Completed by Month" con los completados de cada mes del FY26 (no solo agosto).
- Filtro de mostrar/ocultar arriba del doughnut "Current Status Distribution": un checkbox por estado con su color y conteo. Complete y Canceled vienen destildados por defecto para que la grafica arranque en los estados activos; se redibuja al instante al tildar/destildar.
- Nueva grafica "Requests by Customer" (ancho completo, top 15 por volumen).

## v1.8.57 — 2026-09-01
- Arreglado el estiramiento infinito de las graficas de Indicators: cada grafica ahora vive en un contenedor de altura fija (300px), asi se ven bien con el zoom de la pagina y ya no hay scroll infinito hacia abajo.
- Se quitaron los emojis de los Automation Highlights y se reemplazaron por iconos SVG inline (dashboard, correo, workflow).

## v1.8.56 — 2026-09-01
- Nueva tab "Indicators" arriba (tabs estilo Excel), junto a "FS DA Requests": es el reporte mensual de DA Ops.
- Incluye: 3 Automation Highlights (en ingles), tarjetas KPI (Total Received, Completed, Open, Avg 1st Ack SLA, Avg Total SLA) y 4 graficas en vivo:
  - Received vs Completed por mes (con divisores de swimlane por trimestre Q1-Q4).
  - Current Status Distribution (dona).
  - SLA Performance por mes: 1st Ack SLA (Created -> Acknowledged) y Total SLA (Acknowledged -> siguiente stage: In Approval Loop / Out for Signature / IT Request Submitted / Complete).
  - Requests by Type (barra horizontal).
- Todo se calcula en vivo desde los datos de SharePoint + el historial de status en Firebase. Se agrego Chart.js 4.4.1.

## v1.8.55 — 2026-08-27
- Se quito el correo de status "Add for Signature" (ese status no existe en SharePoint). Los correos de status ahora cubren: Acknowledged, Info Requested, In Approval Loop, Out for Signature, IT Request Submitted, On Hold, Canceled y Complete.

## v1.8.54 — 2026-08-27
- El logo del footer ahora es una version recortada y con fondo TRANSPARENTE (sin cuadro blanco) del logo inline de Intel Foundry, mostrado mas grande (200px). Generado con make_logo_transparent.py.

## v1.8.53 — 2026-08-27
- El footer de los correos ahora usa el logo oficial "intel foundry" inline (negro) en vez del logo cuadrado chico, mas grande y limpio sobre el footer claro.

## v1.8.52 — 2026-08-27
- Mas cambios de status ahora mandan correo al cliente con el template estandar: Add for Signature, IT Request Submitted, On Hold y Canceled (ademas de los que ya existian: Acknowledged, Info Requested, In Approval Loop, Out for Signature, Complete).
- Todos requieren el toggle "Auto emails" en ON. Si un correo de status no llega, revisar la conexion de Outlook en Power Automate (Connections > Fix connection).

## v1.8.51 — 2026-08-27
- El popup de DA Link (al pasar a In Approval Loop) ahora SOLO aparece para Portal Creation y New DA — la etapa donde se crea el DA. Los demas tipos ya no lo muestran.
- Ahora el DA Link (URL) y el DA Number son AMBOS obligatorios en ese popup, para que siempre queden registrados en SharePoint.

## v1.8.50 — 2026-08-27
- Los correos de Complete ahora dicen QUE servicio se completo, justo despues del customer (ej. "REQ. 2683 - Customer - COD"). Aplica a COD y a todos los tipos. El servicio tambien se agrega al asunto del correo.
## v1.8.49 — 2026-08-27
- FAQ del chatbot ampliado: progress bar, age badges, notas, historial, export, dark mode, expand/collapse, paginacion, atajos, presencia/notificaciones, COD, DA Edit, MP-NDA/MRUNDA, sync, sort, version/changelog, report. En tracker y guia.
- Guia: nuevo slide "Help Chatbot" y lista completa de status validos de SharePoint (agregados IT Request Submitted, On Hold, Canceled).
- Blindaje del flow Separate documentado en sync/FLOW-3-CREATE-REQUEST.md (Soluciones A/B/C para requests sin Assigned BD; se limpiaron los marcadores de conflicto del archivo).
## v1.8.48 — 2026-08-27
- Chatbot de ayuda (boton flotante abajo-derecha) en el tracker y en la guia. Responde dudas comunes (FAQ por palabras clave, sin IA externa ni costo) y tiene boton "Report it" que envia bugs/feature requests a jair.garcia@intel.com por el flow de correo existente. El asunto "[FS Tracker FEEDBACK]" NO lleva REQ., asi que llega al inbox (no a la carpeta del tracker). Los reportes se anexan en sync/FEATURE-REQUESTS.md.
- Guia de usuario actualizada con todas las features nuevas (correos, Complete/COD/Codename, Assign, Separate, filtros multi-select/Tech Node, sonido). Imagenes img10-17 pendientes (se ocultan solas hasta que se agreguen).
## v1.8.47 — 2026-08-27
- Filtro de tipos ahora es MULTI-SELECT: el dropdown "All Types" se volvio un menu de checkboxes. Seleccionas varios tipos y muestra los requests que tengan CUALQUIERA de ellos; seleccionas uno y muestra solo ese; ninguno = todos. Incluye boton Clear.
## v1.8.46 — 2026-08-27
- Separate request ahora aplica a Codename Y a IFS NDA (cada uno debe ir en su propio request; New DA + Portal Creation se quedan juntos). El boton aparece cuando un standalone (Codename/IFS NDA) viene mezclado con otro servicio.
- El tracker ahora usa los nombres EXACTOS de SharePoint (requestTypeRaw) al reescribir RequestType, porque las opciones son sensibles a mayusculas/palabras ("Portal creation", "Code Name Request", "DA edit"). Antes mandaba los normalizados y por eso el multi-valor se perdia.
- PENDIENTE: escribir VARIOS tipos restantes (New DA + Portal) en el paso 4 del flow aun se pierde (solo guarda uno). Falta ver el output del paso 4 para el formato correcto del multi-choice.
## v1.8.45 — 2026-08-27
- Separate request (Codename) YA ESTA ACTIVO: se conecto el flow "Create Request" (CONFIG.createRequestUrl). Al dar clic en "Separate request" en un request con Codename + New DA/Portal, crea un request nuevo solo con Codename (copiando Assigned BD y demas personas) y le quita el Codename al original. Probado end-to-end (2713/2714).
## v1.8.44 — 2026-08-27
- Separate request (Codename): el tracker ahora tambien manda del request original el Created By (Author), el Assigned BD (Project Contact) y el FCE Lead / Account Owner, para que el request nuevo de Codename conserve esos tres campos de personas identicos al original. Requiere el flow "Create Request" (instrucciones en sync).
## v1.8.43 — 2026-08-20
- Sonido de nuevo ticket: la pagina suena una campanita cuando aparece un request nuevo (ID que no estaba) al refrescar. Toggle Sound/Muted (icono de campana SVG) en la barra para prender/apagar (se recuerda). El sonido se sintetiza en el navegador, no necesita archivo de audio. (El primer clic desbloquea el audio del navegador.)
- El sonido de Outlook (cuando llega un correo del tracker) se configura en la regla de Outlook con "play a sound"; instrucciones en sync/Sonidos-y-regla-outlook.md.
## v1.8.42 — 2026-08-20
- MRUNDA ahora es un servicio DISTINTO de MP-NDA (ya no se agrupan). Aparece como su propio tipo "MRUNDA" en las tarjetas, en el filtro de tipos y en los correos (Info Request y Complete).
## v1.8.41 — 2026-08-20
- Nuevo filtro "Tech Node" en la barra de arriba: selecciona Intel 18A, Intel N-x, etc. para filtrar por tecnologia (campo TechNode de SharePoint). El dropdown se llena solo con los tech nodes que existan en los datos. Tambien se muestra el Tech Node en cada tarjeta.
- Nota: requiere que el flow "Get all requests" devuelva la columna TechNode (en el debug del 2698 si venia, deberia funcionar directo).
## v1.8.40 — 2026-08-20
- "Assigned BD" ahora se lee de la columna correcta de SharePoint: Project_x0020_Contact.
- Nuevo boton "Separate request": cuando un request trae Codename junto con New DA / Portal Creation, un clic crea un request NUEVO en SharePoint solo con el Codename y deja el resto en el original. Requiere un flow "Create Request" (instrucciones en sync/Separate-request-flow.md). Mientras CONFIG.createRequestUrl este vacio, el boton avisa que falta configurar el flow y no rompe nada.
## v1.8.39 — 2026-08-20
- El chip de asignado en la cabecera ahora se separa visualmente (con un divisor) y usa color morado en vez del cyan que chocaba con la badge de Acknowledged en modo oscuro.
- El correo de Codename ahora va al Assigned BD y al FCE Lead / Account Owner (si ninguno tiene email, cae al project contact / author). CC: fs.da.ops.
- Se leen mas variantes del nombre interno de "Assigned BD". Si sigue sin aparecer, se necesita el nombre interno exacto (ver sync/Assign-field-flow.md).
- Escritura de "Assigned To" (Person) a SharePoint: se documenta el metodo robusto validateUpdateListItem en las notas del flow, porque el "Update item" normal no siempre resuelve campos Person.
- PENDIENTE (siguiente paso): separar el servicio Codename en su propio card cuando un request trae Codename + Portal Creation + New DA juntos. Requiere llaves compuestas (id-servicio) y se hara con cuidado para no romper el tracking.
## v1.8.38 — 2026-08-20
- La tarjeta muestra TRES campos de personas por separado: Assigned To (iGO Admin, editable), Assigned BD y FCE Lead / Account Owner (solo lectura).
- Nota: el flow "Get all requests" debe devolver esas columnas (iGOAdminOnly_x002d_AssignedTo, AssignedBD, AssignedFCELead) para que aparezcan tras Sync. Detalle en sync/Assign-field-flow.md.
## v1.8.37 — 2026-08-20
- Asignar a SharePoint mas simple: el tracker manda tambien el claim ya armado (assignedToClaim). En el flow solo pones ese token en el campo Assigned To Claims, sin concat ni if.
## v1.8.36 — 2026-08-20
- Asignar desde el frontend: cada tarjeta tiene un boton Assign/Change junto a "Assigned To". Se elige a un miembro del equipo (Jair, Jenn; se agregan mas en TEAM_MEMBERS) y escribe al campo Person "iGO Admin - Assigned To" de SharePoint.
- Popup de Complete con autollenado: si el mismo cliente ya tiene un request previo con Portal Name / DA number, el popup los prellena (editables antes de enviar) y avisa que vienen de un request anterior. Asi los clientes repetidos no se re-escriben. No inventa datos: solo reutiliza lo que ya existe en la lista.
## v1.8.35 — 2026-08-20
- Todos los correos mandan ahora el campo sensitivity explicito: vacio ("") en los normales y "Intel Confidential\Intel Employees (Encrypted - IC)" SOLO en Codename. Calza con la expresion del flow.
## v1.8.34 — 2026-08-20
- El dropdown Sensitivity trae etiquetas de Intel; la correcta para Codename es "Intel Confidential\Intel Employees (Encrypted - IC)". El tracker manda ese texto exacto solo en Codename.
## v1.8.33 — 2026-08-20
- Do Not Forward via Sensitivity del flow (sin admin). Asunto limpio.
## v1.8.32 — 2026-08-20
- Codename: el icono de llave ahora es SVG (sin emoji), en el popup y el correo.
- Destinatarios corregidos con los campos Person reales de SharePoint: BD = AssignedFCELead, mas Project Contact y Author (el campo iGO Admin Assigned To no existe en varios requests).
## v1.8.31 — 2026-08-20
- Codename: al completar un request de tipo Codename, sale un popup que pide el codename a asignar a la empresa (Company Name).
- Al confirmar, se envia el codename con el formato Intel al BD (iGO Admin Assigned To) y a todas las personas copiadas en el request.
- El correo lleva la etiqueta [Encrypt] en el asunto para que una regla de transporte de Exchange/Purview lo cifre. IMPORTANTE: el cifrado real depende de que TI tenga esa regla configurada; sin ella el correo sale sin cifrar.
- Se leen los emails del BD y de los copiados desde campos Person de SharePoint (varios nombres internos probables). Si algun destinatario no aparece, hay que confirmar el nombre interno del campo.
## v1.8.30 — 2026-08-20
- El correo de Complete ahora se adapta al tipo de request:
  - Portal Creation / New DA: muestra Portal Name + DA ID y el paso "go to AGS and apply to [Portal] WebView Only".
  - IFS NDA: el documento esta firmado, puedes iniciar la relacion de negocio con el cliente.
  - MP-NDA / Multi-Party: el documento esta firmado, puedes iniciar la relacion entre los dos clientes.
- COD al completar: popup de doble confirmacion (no pide portal name) y CC automatico a birthe.dallmer@intel.com y james.c.matayabas.jr@intel.com.
## v1.8.29 — 2026-08-19
- El buscador principal ahora tambien busca por DA number, DA link, nombre de portal y asignado (no solo customer/ID).
- Al completar un request, la barra de progreso llega a 100% y todos los sub-steps quedan completos al instante, sin recargar la pagina.

## v1.8.28 — 2026-08-19
- Todos los comunicados por correo usan ahora el azul Intel #001E50 de forma consistente: acentos de estado, numeros de SLA, cabeceras de tabla, botones de Info Request y el DA number del correo Complete quedan iguales al banner y al fondo.

## v1.8.27 — 2026-08-19
- La fecha de la tarjeta ahora es blanca en vez de gris tenue, para que se lea bien.

## v1.8.26 — 2026-08-19
- FIX: "Assigned To" ahora lee UNICAMENTE el campo iGO Admin (iGOAdminOnly_x002d_AssignedTo). Si nadie de iGO esta asignado, no muestra nada (el chip se oculta y la tarjeta dice "Unassigned"), en vez de caer al FCE Lead u otros campos.

## v1.8.25 — 2026-08-19
- Banners con el azul clasico de Intel #001E50: el header del portal y los comunicados por correo (Acknowledged, Info Request, Out for Signature, In Approval Loop, Complete). El fondo exterior de los correos tambien usa #001E50.

## v1.8.24 — 2026-08-19
- El asignado (Assigned To) ahora aparece como chip en la cabecera de la tarjeta, antes de la fecha, para ver de quien es cada request sin abrirlo.

## v1.8.23 — 2026-08-19
- Nuevo filtro "Assigned To" (campo iGO Admin Only - Assigned To) en la barra de filtros de arriba. Se llena solo con los asignados que existan; incluye opcion "Unassigned".
- Los requests con status Acknowledged ahora cuentan como WIP (In Progress), ya no como New.
- Nuevos stat pills: Acknowledged (ack) y Canceled. Canceled es su propia categoria (ya no se mezcla con Done). Al hacer clic filtran igual que los demas pills.

## v1.8.22 — 2026-08-19
- Nueva fila "DA Number" en la tarjeta, separada de DA Link. El numero que se captura en el popup de DA Link ahora se guarda en su propia columna de texto en SharePoint (DA_x0020_Number) y se lee de vuelta al hacer Sync.
- El boton de DA Link ahora siempre dice "Open DA Link" (el numero vive en su propia fila).
- PENDIENTE en Power Automate: en el flow Update Fields agregar el mapeo daNumber -> columna DA Number. Instrucciones en el l4ve.

## v1.8.21 — 2026-08-19
- FIX guardado DA Link: la columna DALink de SharePoint es tipo URL simple (String/uri), asi que el flow debe recibir SOLO la URL, no "url, texto". El numero de DA (Alternative Text) no cabe en esa columna; se queda en el tracker para autollenar el correo de Complete.
- Se borraron del repo los archivos Instructions_follow / Instructions_follow1 (traian la URL firmada del flow) y se agregaron al .gitignore.

## v1.8.20 — 2026-08-19
- Nuevo campo "DA Link" visible en la tarjeta, junto a Portal Name. Se guarda al instante desde el popup de DA Link (In Approval Loop), aunque SharePoint todavia no confirme la escritura, y tambien lo lee de vuelta de SharePoint cuando el flow de Get all requests lo trae.

## v1.8.19 — 2026-08-19
- FIX: la URL de `updateFieldsUrl` no tenia la firma de seguridad del flow (por eso daba 401 y cero corridas). Se cambio el trigger a "Anyone" en Power Automate y se conecto la URL completa con firma.
- Se elimino `Instructions_follow` del repo (contenia la URL firmada y ya no debe quedar publica).

## v1.8.18 — 2026-08-19
- Nuevo campo "Portal Name" visible en la tarjeta. Si el cliente lo puso en su request original, aparece con la etiqueta "Suggested by customer" hasta que nosotros lo confirmemos/corrijamos al poner el status Complete.
- Conectada la URL real del flow de Power Automate para `CONFIG.updateFieldsUrl` (escribe DA Link y Project Portal Name a SharePoint). URL: workflow 7c9ac8ba...
- OJO: la URL que se paso venia sin la firma `&sp=...&sv=1.0&sig=...` que traen los otros 3 flows. Si el guardado falla, re-copiar la URL completa desde Power Automate.

## v1.8.17 — 2026-08-19
- Logo del header mas grande: de 28px a 68px, en Dark y Light mode.
- Nuevo popup interno al pasar a In Approval Loop: pide DA Link (URL) y numero de DA (Alternative Text, opcional) y lo guarda directo en el campo "DA Link" de SharePoint. El cliente no se entera de esto.
- El popup de Complete ahora autorrellena el numero de DA si ya se capturo en el paso anterior. El Portal Name se escribe siempre en el campo "Project Portal Name" de SharePoint al completar.
- PENDIENTE: falta crear el flow de Power Automate que reciba estos campos y pegar su URL en `CONFIG.updateFieldsUrl` (index.html). Instrucciones en `.kiro/hooks/l4ve`.

## v1.8.16 — 2026-08-19
- Nuevo logo oficial de Intel Foundry en el header: version oscura (logo-dark.jpg) para Dark mode, version clara (logo-light.jpg) para Light mode. Cambia solo al usar el boton Light/Dark.

## v1.8.15 — 2026-08-19
- Nuevos correos automaticos: Out for Signature ("Depends on Customer, Avg 48-56 hrs") y In Approval Loop ("2-4 dias").
- Al poner el status en Complete se abre un popup pidiendo Portal Name y numero de DA. Al confirmar, se manda un correo de celebracion con chispas, "Congratulations! Your portal is already created.", el nombre del portal y el ID del DA.
- Los tres correos nuevos respetan los toggles existentes de Auto emails y Test mode.

## v1.8.14 — 2026-08-19
- Nuevo boton "Test mode" en el header, junto a Auto emails. Encendido (default): Acknowledged e Info Request van solo a Jair y CC vacio. Apagado: van al creador real del request con CC a `fs.da.ops@intel.com`.
- Se elimino la constante fija `TEST_MODE = true` de ambas funciones de envio; ahora usan el toggle persistido `testModeEnabled`.

## v1.8.13 — 2026-08-19
- Ajustado el numero de circulos por correo: Info Request ahora usa 34 circulos (17 por lado) y Acknowledged usa 46 circulos (23 por lado).

## v1.8.12 — 2026-08-19
- FIX Outlook: restaurados los circulos del correo Acknowledged eliminando `opacity` y `filter:alpha`, que Outlook podia interpretar como completamente transparentes.
- Los 40 circulos conservan la tabla Outlook-safe y ahora usan colores solidos premezclados para verse suaves sin desaparecer.
- TEST_MODE permanece activo: solo Jair y CC vacio.

## v1.8.11 — 2026-08-19
- Reactivado TEST_MODE para Acknowledged e Info Request.
- Ambos correos automaticos se envian unicamente a `jair.garcia@intel.com`.
- CC queda vacio; durante las pruebas no recibe correo el creador ni FS DA OPS.

## v1.8.10 — 2026-08-19
- Eliminado el simbolo `@` antes del nombre en Acknowledged, Info Request y los fallbacks mailto.
- El saludo conserva solamente el primer nombre: `Dear Nombre` o `Hi Nombre`.

## v1.8.9 — 2026-08-19
- PRODUCCION: Acknowledged e Info Request se envian al creador del request y siempre llevan CC a `fs.da.ops@intel.com`.
- El saludo usa solamente el primer nombre despues de `Dear @`; tambien interpreta correctamente nombres de SharePoint con formato `Apellido, Nombre`.
- `Acknowledged → Next step` permanece en una sola linea dentro de la tabla SLA.
- Los 40 circulos laterales conservan su posicion Outlook-safe y ahora son mas suaves/translucidos.

## v1.8.8 — 2026-08-19
- MPA-IC y MPA-NDA ahora se normalizan como MP-NDA/Multi-Party.
- Los correos automaticos de Info Request incluyen el template MP-RUNDA cuando SharePoint devuelve MP-NDA, MPA-NDA, MPA-IC, MRUNDA o Multi-Party.
- El correo manual que se abre al hacer clic en Created By usa el mismo template para cualquiera de esos nombres.

## v1.8.7 — 2026-08-19
- FIX Outlook: reemplazado el posicionamiento absoluto de los circulos por una tabla de presentacion de tres columnas.
- 40 circulos quedan en bandas laterales reales: 20 a la izquierda y 20 a la derecha; ya no pueden apilarse en el centro ni empujar el contenido.
- El mismo wrapper se aplica a Acknowledged e Info Request.
- Ambos correos permanecen en TEST: solo `jair.garcia@intel.com`, sin CC.

## v1.8.6 — 2026-08-19
- Se intentaron distribuir 40 circulos con coordenadas absolutas por ambos lados y a lo largo del correo.
- El deploy fue exitoso, pero Outlook ignoro las coordenadas y siguio mostrando los circulos apilados; queda documentado como intento fallido reemplazado en v1.8.7.

## v1.8.5 — 2026-08-19
- El modal Version History ahora incluye el historial completo de versiones, fixes, errores resueltos y problemas de deploy/git.

## v1.8.4 — 2026-08-19
- Badge de version clickeable: abre un modal "Version History" con todas las versiones y cambios.

## v1.8.3 — 2026-08-19
- Filtro "All Types" ahora incluye MP-NDA, Secure Chamber, DocuSign Request, Redbook Release.

## v1.8.2 — 2026-08-19
- Badge de version mas visible (fondo cyan solido) y hardcodeado en el HTML. Header con wrap.

## v1.8.1 — 2026-08-19
- Circulos del correo repartidos por los bordes (posiciones en %); tarjeta 600px.

## v1.8.0 — 2026-08-19
- Correo del nombre clickeable (mailto) ahora incluye el template MP-RUNDA para Multi-Party.
- Boton toggle estilo iPhone en el header: "Auto emails" ON/OFF (persistente en localStorage).
  Si esta OFF, no se mandan correos automaticos al cambiar el SP status.
- Fix Light Mode: textos que quedaban en blanco (customer, id, fecha, titulos, stats) y
  botones ahora se ven bien en modo claro.

## v1.7.2 — 2026-08-19
- Restaurados los circulos (divs position:absolute, el metodo que si renderizaba) en el
  fondo azul exterior de ambos correos (Acknowledged + Info Request).

## v1.7.1 — 2026-08-19
- Circulos del correo ahora son un PNG real (email-bg.png) hosteado en GitHub Pages.
  Outlook/Gmail NO renderizan SVG data-URI ni position:absolute; el PNG SI se ve.
- Script make_email_bg.py genera la imagen (navy + circulos).

## v1.7.0 — 2026-08-19
- Acknowledged y Info Request ahora comparten el MISMO diseno: banner azul Intel,
  circulos de fondo (SVG) y leyenda completa de Intel Confidential.
- Leyenda completa ("...may contain confidential information. If you are not the
  intended recipient, please notify the sender and delete this message.") en TODOS los correos.
- Badge de version movido al header, junto a los botones Sync/Excel/JSON.

## v1.6.0 — 2026-08-19
- Control de versiones + este CHANGELOG. Badge de version en el header de la pagina.

## v1.5.0 — 2026-08-19
- Correo automatico "Info Request" al cambiar SP Status a "Info Requested".
- Incluye TODOS los templates segun los tipos del request (New DA, DA Edit,
  Portal Creation, IFS NDA, Multi-Party RUNDA/MP-NDA, Codename como formulario).
- Diseno: banner azul Intel, circulos decorativos en el fondo exterior (SVG),
  botones azules clickeables por template, footer con logo + Intel Confidential.
- Links de templates confirmados; MP-RUNDA agregado.
- Acknowledged + Info Request en TEST_MODE (solo a Jair) mientras se prueba.

## v1.4.0 — 2026-08-19
- Correo automatico "Acknowledged": el tracker genera el HTML (buildAckEmailHtml)
  y lo manda al flow como bodyHtml. El flow ya no lleva HTML (se configura una vez).
- Diseno Foundry Services: header, tabla de SLAs, footer con logo, Intel Confidential.
- SLAs: Acknowledged->Next 24-48 hrs, In Approval Loop 2-4 days, Out for Signature
  "Depends on Customer, Avg 48-56 hrs".
- Saludo "Dear @Nombre Apellido", firma "FS DA OPS - Intel Foundry Services".
- CC fs.da.ops (en LIVE). Email del creador extraido de Author.Email / Claims.

## v1.3.0 — 2026-08-19
- Requests "Canceled": tarjeta en gris + overlay de diagonales + tag CANCELED.
- Notificacion de cambio de SP Status mas clara.

## v1.2.0 — 2026-08-19
- Orden de secciones: New DA primero, luego Portal Creation, luego el resto.
- Banner de SLA por tarjeta + badges de tiempo estimado por step.

## v1.1.0 — 2026-08-19
- Zoom global 140% para legibilidad.
- Nombre "Created By" clickeable -> abre correo (mailto) con template por tipo.

## v1.0.0 — 2026-08-19
- Campos nuevos en tarjeta expandida: Created By, Assigned BD, Details, Attachments.
- Attachments: link "View attachment(s)" abre el request en SharePoint.
- Assigned BD desde campo iGOAdminOnly_x002d_AssignedTo.

---

## Como actualizar la version (para Kiro en cada deploy)
1. Subir el numero en `CHANGELOG.md` (nueva entrada arriba con los cambios).
2. Actualizar la constante `APP_VERSION` en index.html (se muestra en el header).
3. Commit + push. GitHub Pages redepliega en 1-2 min.
