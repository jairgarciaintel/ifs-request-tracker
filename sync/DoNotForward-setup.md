# Do Not Forward para el correo de Codename (SIN permisos de admin)

## Buena noticia
NO necesitas ser Exchange admin ni crear reglas de transporte. La accion
"Send an email (V2)" del conector Office 365 Outlook YA trae un parametro
**Sensitivity** con la opcion **Do not forward**. Se aplica directo en el flow.

El tracker ahora manda al flow un campo extra `sensitivity` con el valor
`do not forward` SOLO cuando es un correo de Codename. Los demas correos
(Acknowledged, Complete, etc.) siguen saliendo normales.

## Que hay que configurar en el flow de envio (una vez)
Es el flow que ya manda los correos del tracker (el de CONFIG.sendEmailUrl,
la accion "Send an email (V2)").

### 1. Agregar `sensitivity` al schema del trigger
En el trigger "When an HTTP request is received", en el JSON Schema agrega la
propiedad `sensitivity` junto a las que ya tienes (to, cc, subject, bodyHtml, etc.):

    "sensitivity": { "type": "string" }

(Si el schema es un objeto con "properties", metela ahi. No pasa nada si en la
mayoria de las llamadas no viene: queda vacia.)

### 2. Aplicar la Sensitivity en la accion "Send an email (V2)"
En la accion Send an email (V2):
  - Click en "Show advanced options" (o "Mostrar opciones avanzadas").
  - Busca el parametro **Sensitivity**.
  - El valor debe ser dinamico segun lo que mande el tracker. Como el conector
    espera uno de los valores fijos (Normal / Personal / Private / Confidential /
    Do not forward / Encrypt), lo mas simple y robusto es:

    OPCION SENCILLA (recomendada): pon una CONDICION antes del envio.
      - Agrega un "Condition":  sensitivity  is equal to  do not forward
      - Rama TRUE:  una accion "Send an email (V2)" con Sensitivity = "Do not forward"
      - Rama FALSE: la accion "Send an email (V2)" normal (sin sensitivity)
      Ambas ramas usan los mismos To/CC/Subject/Body (dynamic content del trigger).

    OPCION AVANZADA (una sola accion): en el campo Sensitivity usa una expresion
      que devuelva el valor cuando venga y vacio cuando no:
        if(equals(toLower(triggerBody()?['sensitivity']), 'do not forward'), 'Do not forward', '')
      OJO: el texto debe coincidir EXACTO con la etiqueta que el conector espera
      ("Do not forward"). Si el conector la rechaza, usa la Opcion sencilla.

### 3. Guardar. No cambia la URL del flow.

## Que hace el tracker (ya deployado)
- En el correo de Codename manda: to, cc, subject, name, id, customer, bodyHtml,
  y ademas  sensitivity: "do not forward".
- Los otros correos NO mandan sensitivity (o va vacia) -> salen normales.

## Probar
1. Test mode ON (llega solo a jair.garcia@intel.com).
2. Completa un request Codename, pon codename, envia.
3. El correo debe llegar con el candado / marca "Do Not Forward" y el boton de
   Reenviar deshabilitado.
4. Si llega normal: revisa que el flow tenga el paso de Sensitivity = Do not
   forward en la rama correcta, y que el schema tenga `sensitivity`.

## Destinatarios del correo de Codename (confirmado del item 2698)
Se leen de estos campos Person de SharePoint:
- `AssignedFCELead`      -> el BD / FCE Lead (ej. ravi.gutala@intel.com)
- `Project_x0020_Contact` -> contacto del proyecto
- `Author`               -> quien creo el request
CC: fs.da.ops@intel.com. En Test mode todo va solo a jair.garcia@intel.com.

NOTA: el campo `iGOAdminOnly_x002d_AssignedTo` NO existe en varios requests
(por eso "Assigned To" sale vacio). Para Codename usamos AssignedFCELead como BD.
