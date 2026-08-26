# Codename cifrado - CAUSA CONFIRMADA y solucion

## Diagnostico (confirmado con el Run history)
En los Inputs del paso "Send an email (V2)", el campo Sensitivity SI llega con el
valor correcto:
    Intel Confidential\Intel Employees (Encrypted - IC)
...pero el correo llega SIN cifrar.

CONCLUSION: el conector Office 365 Outlook NO aplica la etiqueta cuando se la
pasas como TEXTO / expresion dinamica. Solo la aplica cuando la etiqueta esta
SELECCIONADA del dropdown (ahi el conector guarda el ID interno del label, no el
texto visible). Con texto libre la "acepta" pero no cifra.

## SOLUCION (hacer en el flow - Power Automate) : Condition + dropdown
Reemplazar el envio unico por DOS ramas. En la rama cifrada, la Sensitivity se
ELIGE DEL DROPDOWN (no token, no expresion).

1. Antes del "Send an email", agrega una accion "Condition":
     Izquierda:  triggerBody()?['sensitivity']
     Operador:   is not equal to
     Derecha:    (dejar vacio)

2. Rama "If yes" (TRUE = es Codename, viene con etiqueta):
     Accion "Send an email (V2)":
       - To:       triggerBody()?['to']       (o el token 'to')
       - Subject:  token 'subject'
       - Body:     token 'bodyHtml'
       - CC (advanced): token 'cc'
       - Sensitivity (advanced):  << ELIGE DEL DROPDOWN >>
             Intel Confidential\Intel Employees (Encrypted - IC)
         (seleccionarla de la lista desplegable; NO escribir texto ni poner token)

3. Rama "If no" (FALSE = correo normal):
     Accion "Send an email (V2)" IGUAL, pero Sensitivity VACIO (sin tocar).

4. Guardar. No cambia la URL del flow.

## Por que asi y no con expresion
- Con expresion / token en Sensitivity: el conector recibe el texto pero no lo
  resuelve a un label real -> correo sin cifrar (justo lo que paso).
- Eligiendo del dropdown: el conector usa el ID interno del label -> cifra.
- Por eso hay que duplicar el envio: una rama con el label del dropdown (Codename)
  y otra sin label (todos los demas correos).

## Probar
1. Test mode ON.
2. Completa un Codename -> el correo debe llegar CIFRADO (Intel Confidential).
3. Manda cualquier otro (Acknowledged) -> debe llegar NORMAL.

## Recordatorio
El tracker ya manda:
  - Codename:  sensitivity = "Intel Confidential\Intel Employees (Encrypted - IC)"
  - Resto:     sensitivity = ""
La condicion (sensitivity is not equal to vacio) separa bien ambos casos.
