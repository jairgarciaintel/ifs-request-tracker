# Codename cifrado (Intel Confidential) - DEBUG por que no encripta

## Confirmado
- El metodo (Sensitivity label en "Send an email V2") SI funciona bien cuando el
  campo esta bien configurado (doc de Microsoft lo confirma).
- El tracker manda bien:  sensitivity = "Intel Confidential\Intel Employees (Encrypted - IC)"
  SOLO en Codename, y "" en los demas. El HTTP responde 202.
- Entonces el problema esta en COMO quedo el campo Sensitivity del flow.

## PASO 1 - ver el Run history (LA PISTA CLAVE)
Flow de envio (workflow 205f9f20) -> Run history -> abre la corrida del correo
Codename -> paso "Send an email (V2)" -> Inputs -> campo "Sensitivity". Que dice?

  a) Dice "Intel Confidential\Intel Employees (Encrypted - IC)"
     -> el valor llega, pero el conector no lo aplica con texto libre.
     SOLUCION: usar la Condition de abajo (elegir la etiqueta del DROPDOWN a mano).

  b) Esta VACIO / null
     -> el flow no esta tomando el sensitivity del trigger (mapeo mal).
     SOLUCION: revisar la expresion/token del campo (ver abajo).

  c) El paso esta en ROJO
     -> copiar el error y mandarlo.

## SOLUCION ROBUSTA (recomendada) - Condition + etiqueta del dropdown
En vez de meter el label como texto (que el conector puede no reconocer), duplica
el envio en dos ramas y en la rama cifrada ELIGE la etiqueta del dropdown:

1. Agrega una Condition antes del envio:
     triggerBody()?['sensitivity']   is not equal to   (vacio)
2. Rama TRUE (es Codename):
     "Send an email (V2)" con:
       To/CC/Subject/Body = tokens del trigger (to, cc, subject, bodyHtml)
       Advanced options -> Sensitivity = ELEGIR DEL DROPDOWN:
         "Intel Confidential\Intel Employees (Encrypted - IC)"
       (NO escribir texto ni token; seleccionarla de la lista, valor 100% valido)
3. Rama FALSE (correo normal):
     "Send an email (V2)" con los mismos tokens y Sensitivity VACIO.

Esto garantiza que el label sea uno valido (elegido del dropdown), no texto libre.

## Si prefieres una sola accion (mas fragil)
En el campo Sensitivity pon la expresion (escrita a MANO, comillas rectas):
    if(empty(triggerBody()?['sensitivity']),null,triggerBody()?['sensitivity'])
Pero si el conector no reconoce el texto, NO cifra. Por eso se prefiere la Condition.

## PASO 2 - requisitos del tenant (si el paso sale verde pero no cifra)
- La etiqueta "Intel Confidential\Intel Employees (Encrypted - IC)" debe existir en
  Purview y APLICAR cifrado (no solo clasificar). Es de Intel, deberia estar ok.
- Rights Management debe estar activo en el tenant (lo esta en Intel).
- La conexion Office 365 Outlook del flow debe ser de una cuenta con esa etiqueta
  disponible (jair.garcia@intel.com). Confirmar que la conexion no este caida.

## Prueba controlada (ya la mande yo)
Se mandaron 2 correos de prueba a jair.garcia@intel.com:
  - "TEST Sensitivity - Codename 2665"  -> deberia llegar CIFRADO
  - "TEST Sensitivity - VACIO (control)" -> deberia llegar NORMAL
Si el de Codename llega normal, el flow no aplica la etiqueta -> usar la Condition.
