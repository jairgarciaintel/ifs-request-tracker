# FLOW 1 - Cifrar correo Codename (pasos completos)

Flow: el de correos (workflow 205f9f20). Manda TODOS los correos, por eso se
necesita una Condition: solo el Codename se cifra, el resto sale normal.

El tracker ya manda el campo "sensitivity":
  - Codename:  "Intel Confidential\Intel Employees (Encrypted - IC)"
  - Resto:     "" (vacio)

============================================================
PASO 1 - Condition  (YA HECHO)
============================================================
Agregada una accion "Condition" entre el trigger y el "Send an email (V2)".

============================================================
PASO 2 - Llenar la Condition
============================================================
En la Condition, primera fila:
  - Lado IZQUIERDO: clic en el campo -> pestaña fx (Expression) -> escribe:
        triggerBody()?['sensitivity']
    (o del dynamic content, elige el token "sensitivity")
  - Operador (en medio):  is not equal to
  - Lado DERECHO: dejarlo VACIO (no escribir nada)
Debe quedar UNA sola fila. Si hay una segunda fila con "And", borrarla.

Logica: si sensitivity NO esta vacio -> es Codename -> rama TRUE (cifrar).
        si esta vacio -> correo normal -> rama FALSE (sin cifrar).

============================================================
PASO 3 - Rama "If yes" (TRUE = Codename, CIFRAR)
============================================================
1. Dentro de la rama "If yes", clic en "Add an action".
2. Busca y agrega "Send an email (V2)" (Office 365 Outlook).
3. Llena los campos con los tokens del trigger (dynamic content):
     To:       token  to
     Subject:  token  subject
     Body:     token  bodyHtml   (si hay boton </> de codigo, activarlo para HTML)
4. Clic en "Show advanced options":
     CC:          token  cc
     Importance:  Normal (o deja el default)
     Sensitivity: << ABRE EL DROPDOWN Y SELECCIONA DE LA LISTA >>
          "Intel Confidential\Intel Employees (Encrypted - IC)"
          IMPORTANTE: seleccionarla de la lista desplegable.
          NO escribir texto, NO poner token/variable. (Con texto NO cifra.)

============================================================
PASO 4 - Rama "If no" (FALSE = correo normal, SIN cifrar)
============================================================
Aqui va tu "Send an email (V2)" ORIGINAL (el que ya tenias).
Opcion A (facil): arrastra el "Send an email V2" original que quedo ABAJO de la
   Condition hacia DENTRO de la rama "If no".
Opcion B: si no te deja arrastrar, crea uno nuevo dentro de "If no" con:
     To: token to | Subject: token subject | Body: token bodyHtml
     Advanced -> CC: token cc
     Sensitivity: DEJAR VACIO (sin etiqueta, sin token).
   Y borra el "Send an email V2" viejo que quedo suelto abajo.

REGLA: al final solo deben existir DOS "Send an email": uno en If yes (con etiqueta
del dropdown) y otro en If no (sin etiqueta). NO debe quedar ninguno suelto fuera
de la Condition.

============================================================
PASO 5 - Guardar y probar
============================================================
1. Save.
2. En el tracker: Test mode ON.
3. Completa un request CODENAME -> el correo debe llegar CIFRADO (Intel Confidential).
4. Cambia otro request a Acknowledged -> debe llegar NORMAL (sin cifrar).
Si el Codename llega normal: revisar que en la rama If yes la Sensitivity este
ELEGIDA DEL DROPDOWN (no como texto), y que la Condition sea "sensitivity is not
equal to (vacio)".
