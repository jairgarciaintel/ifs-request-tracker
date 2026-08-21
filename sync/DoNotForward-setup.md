# Do Not Forward (encriptar + bloquear reenvio) para el correo de Codename

## Que hace el tracker
Cuando completas un request de tipo **Codename**, el tracker manda el correo con
el asunto:

    [DoNotForward] REQ. <id> - <empresa> - Codename Assigned

El tag `[DoNotForward]` en el asunto es la senal. El tracker NO puede aplicar el
cifrado / "Do Not Forward" por si solo: eso lo controla Exchange Online / Microsoft
Purview del lado de Intel. Hay que configurar UNA regla (una sola vez) para que
cualquier correo con ese tag salga protegido como "Do Not Forward"
(equivalente a Outlook > Options > Encrypt > Do Not Forward).

## Opcion A (recomendada) — Regla de transporte en Exchange Admin Center
Necesita permisos de Exchange admin (probablemente TI, no nosotros).

1. Entra a https://admin.exchange.microsoft.com  ->  Mail flow  ->  Rules
2. Add a rule  ->  "Apply Office 365 Message Encryption and rights protection..."
3. Nombre: `FS Tracker - Codename Do Not Forward`
4. Apply this rule if:
   - The subject includes any of these words  ->  `[DoNotForward]`
   - (opcional y mas seguro) AND The sender is  ->  la cuenta/servicio que usa el
     flow de Power Automate para mandar (la que aparece como From en el correo)
5. Do the following:
   - "Apply Office 365 Message Encryption and rights protection"  ->  elige la
     plantilla **Do Not Forward** (RMS template "Do Not Forward").
6. Guardar y activar.

Con esto, todo correo con `[DoNotForward]` en el asunto sale cifrado y sin poder
reenviarse, aunque lo mande Power Automate.

## Opcion B — Etiqueta de sensibilidad (Purview) auto-aplicada
Si Intel usa etiquetas de sensibilidad, TI puede crear una auto-label / regla que
aplique la etiqueta con proteccion "Do Not Forward" cuando el asunto trae el tag.
Mismo efecto, distinto lugar (Purview compliance portal).

## Que NO funciona (por que no lo hago en el flow/JS)
- El conector "Send an email (V2)" de Power Automate NO tiene un switch de
  "Do Not Forward". No existe parametro para eso.
- Desde JavaScript del tracker no se puede forzar cifrado de un correo saliente.
- Por eso la unica via real es la regla de Exchange/Purview de arriba, que ademas
  es lo estandar en Intel.

## Para probar despues de que TI configure la regla
1. Con Test mode ON (el correo llega solo a jair.garcia@intel.com).
2. Completa un request Codename, pon un codename, envia.
3. Abre el correo que llega: debe verse el candado / aviso de "Do Not Forward"
   y el boton de reenviar deshabilitado.
4. Si llega normal (sin proteccion), la regla aun no esta activa o el tag del
   asunto no coincide -> confirmar con TI que la condicion sea exactamente
   `[DoNotForward]`.

## Destinatarios del correo de Codename (confirmado del item 2698)
El tracker manda el codename a los correos de estos campos Person de SharePoint:
- `AssignedFCELead`  (el BD / FCE Lead, ej. ravi.gutala@intel.com)
- `Project_x0020_Contact`  (contacto del proyecto)
- `Author`  (quien creo el request)
CC: fs.da.ops@intel.com
En Test mode todo va solo a jair.garcia@intel.com sin CC.

NOTA: el campo `iGOAdminOnly_x002d_AssignedTo` NO existe en varios requests
(por eso "Assigned To" sale vacio). Para el correo de Codename usamos AssignedFCELead
como BD, que si viene en los items.
