# FS Request Tracker — Changelog

Control de versiones del tracker. La version actual se muestra en el header
de la pagina (esquina). Cuando GitHub Pages ya tiene la nueva version, el
numero cambia — asi sabes que el deploy ya subio.

Formato: vMAJOR.MINOR — fecha — cambios.

---

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
