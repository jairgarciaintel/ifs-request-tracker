# Correo de Codename cifrado (Intel Confidential) - SIN permisos de admin

## Contexto
- El dropdown "Sensitivity" de la accion Send an email (V2) NO trae "Do not forward"
  generico. Trae las etiquetas de Intel. La correcta para Codename es:
      Intel Confidential\Intel Employees (Encrypted - IC)
  Esa etiqueta CIFRA el correo y lo restringe a empleados Intel (en la practica
  eso bloquea el reenvio a externos, que es lo que queriamos).
- El flow de envio es COMPARTIDO: manda TODOS los correos del tracker. Por eso NO
  se puede poner la etiqueta fija (cifraria tambien los correos a clientes).
- Solucion: el tracker manda el nombre EXACTO de la etiqueta en el campo
  `sensitivity` SOLO en el correo de Codename. En los demas correos ese campo va
  vacio -> salen normales.

## Lo que manda el tracker (ya deployado)
- Codename:  sensitivity = "Intel Confidential\Intel Employees (Encrypted - IC)"
- Todos los demas correos: NO mandan sensitivity (llega vacio).

## Configurar el flow (una vez) - la parte importante
El problema que viste ("Failed"): pusiste el token `sensitivity` directo en el
campo Sensitivity, pero cuando llega VACIO (los otros correos) el conector lo
rechaza porque "" no es una etiqueta valida. Hay que manejar el vacio.

### Paso 1 - schema del trigger
En "When an HTTP request is received", en el JSON Schema agrega:
    "sensitivity": { "type": "string" }

### Paso 2 - campo Sensitivity con expresion (una sola accion, recomendado)
En Send an email (V2) -> Show advanced options -> Sensitivity:
  - Quita el token `sensitivity` que tienes puesto ahora.
  - En su lugar pon esta EXPRESION (pestaña fx):

    if(empty(triggerBody()?['sensitivity']), null, triggerBody()?['sensitivity'])

  Asi: si viene la etiqueta (Codename) la aplica; si viene vacio manda `null`
  (sin sensitivity) y el correo sale normal.

  IMPORTANTE: el texto de la etiqueta debe coincidir EXACTO con la del dropdown:
      Intel Confidential\Intel Employees (Encrypted - IC)
  El tracker ya manda exactamente ese texto.

### Paso 2 (alternativa si la expresion da "Failed") - con Condition
Si el conector sigue marcando error con la expresion, usa dos ramas:
  - Condition:  sensitivity  is not equal to  (vacio)
  - Rama TRUE : Send an email (V2) con Sensitivity = elige del dropdown
                "Intel Confidential\Intel Employees (Encrypted - IC)"
                (fijo, elegido a mano, NO token)
  - Rama FALSE: Send an email (V2) SIN Sensitivity (normal)
  Ambas ramas con los mismos To/CC/Subject/Body (dynamic content del trigger).

  Esta alternativa es la mas confiable porque en la rama TRUE eliges la etiqueta
  del dropdown (valor 100% valido) y no dependes de que la expresion sea aceptada.

### Paso 3 - Guardar. No cambia la URL del flow.

## Probar
1. Test mode ON (llega solo a jair.garcia@intel.com).
2. Completa un request Codename -> el correo debe llegar CIFRADO
   (marca Intel Confidential / candado, restringido a Intel).
3. Completa/cambia otro request cualquiera (ej. Acknowledged) -> ese debe llegar
   NORMAL, sin cifrado. Asi confirmas que solo Codename va cifrado.

## Destinatarios del correo de Codename (confirmado del item 2698)
- AssignedFCELead       -> BD / FCE Lead (ej. ravi.gutala@intel.com)
- Project_x0020_Contact -> contacto del proyecto
- Author                -> quien creo el request
CC: fs.da.ops@intel.com. En Test mode todo va solo a jair.garcia@intel.com.
