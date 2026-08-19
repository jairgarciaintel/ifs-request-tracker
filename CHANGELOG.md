# FS Request Tracker — Changelog

Control de versiones del tracker. La version actual se muestra en el header
de la pagina (esquina). Cuando GitHub Pages ya tiene la nueva version, el
numero cambia — asi sabes que el deploy ya subio.

Formato: vMAJOR.MINOR — fecha — cambios.

---

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
