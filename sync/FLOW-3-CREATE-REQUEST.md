# FLOW 3 - Create Request (Separate) - ESTADO Y BLINDAJE

Flow "FS Tracker Create Request" (workflow 589245b5). Conectado en el tracker
(CONFIG.createRequestUrl, v1.8.45+). Se usa cuando das clic en "Separate request".

============================================================
## ESTADO: FUNCIONA
============================================================
- Crea un request NUEVO con el servicio separado (Codename o IFS NDA) con el
  RequestType CORRECTO.
- Copia Assigned BD (Project Contact) y FCE Lead del request original.
- Deja el request ORIGINAL con los tipos restantes, incluso varios juntos
  (ej. "New DA" + "Portal creation"). El multi-valor SI funciona.

CLAVE ya resuelta:
- RequestType usa expresion fx en "Value - 1":  triggerBody()?['requestType']
  (el dropdown/dynamic content NO lo aceptaban; la EXPRESION fx SI).
- Nombres EXACTOS de SharePoint (case/word sensitive):
    "New DA", "Portal creation" (c minuscula), "Code Name Request", "IFS NDA",
    "DA edit", "WebView AGS role", "MRUNDA", "MP-NDA".
  El tracker manda requestTypeRaw (nombre exacto). remainingTypes unidos por ;# .

============================================================
## BLINDAJE: request SIN Assigned BD (Project Contact vacio)
============================================================
### El problema
El tracker SIEMPRE manda los campos de persona, pero si el request no trae BD o
FCE Lead, manda el claim como "" (string vacio). Entonces el "Create item" arma:

    "item/Project_x0020_Contact": [ { "Claims": "" } ]

y SharePoint truena con:

    status 400 - "The specified user could not be found."

Esto pasa porque un ARRAY con un objeto de Claims vacio NO es lo mismo que "sin
persona": SharePoint intenta resolver el usuario "" y no existe.

### La regla de negocio (confirmada con el usuario)
- COMPANY (Title) es el UNICO campo 100% obligatorio.
- FCE Lead: es obligatorio en SharePoint (asterisco rojo), asi que casi siempre viene.
- Assigned BD (Project Contact): NO es obligatorio -> ESTE es el que puede venir vacio.
Por eso el blindaje importa sobre todo para Project Contact.

------------------------------------------------------------
### SOLUCION A (rapida, ya intentada con fx) - probar primero
------------------------------------------------------------
En el "Create item", en cada campo Person usar una expresion fx que mande null
cuando el claim viene vacio:

  Campo "Assigned FCE Lead or Account Owner - Claims":
    if(empty(triggerBody()?['fceLeadClaim']), null, triggerBody()?['fceLeadClaim'])

  Campo "Assigned BD / Project Contact - Claims":
    if(empty(triggerBody()?['projectContactClaim']), null, triggerBody()?['projectContactClaim'])

OJO: Project Contact es multi-value (array). Si al meter la expresion en "Claims"
el array sigue quedando como [ { "Claims": null } ], puede que SharePoint aun se
queje. Si eso pasa, usar la SOLUCION B (es la robusta).

------------------------------------------------------------
### SOLUCION B (robusta, recomendada) - Condition antes del Create
------------------------------------------------------------
Idea: hacer DOS ramas segun venga o no el BD, para que el array de Project Contact
exista SOLO cuando hay persona. Asi nunca mandas [{Claims:""}].

Pasos en el flow "FS Tracker Create Request":

1. Despues del trigger, agrega una accion "Condition".
   - Condicion:  triggerBody()?['projectContactClaim']  is not equal to  (dejar vacio)
     (en fx del lado izquierdo puedes poner: empty(triggerBody()?['projectContactClaim'])
      y comparar  is equal to  false)

2. Rama "If yes" (SI hay BD): pon un "Create item" que INCLUYA Project Contact:
       item/Project_x0020_Contact  ->  Claims:  triggerBody()?['projectContactClaim']

3. Rama "If no" (NO hay BD): pon otro "Create item" IGUAL pero SIN el campo
   Project Contact (borralo del formulario, deja el campo Person vacio, no lo mandes).

4. En AMBAS ramas, el FCE Lead usa la expresion fx de la Solucion A
   (por si tambien llegara vacio):
       if(empty(triggerBody()?['fceLeadClaim']), null, triggerBody()?['fceLeadClaim'])

Con esto: si el request no trae BD, se crea igual (sin BD) en vez de fallar.

------------------------------------------------------------
### SOLUCION C (alternativa avanzada) - "Send an HTTP request to SharePoint"
------------------------------------------------------------
Sacar Project Contact del Create item y, solo si hay BD, hacer despues un
"Send an HTTP request to SharePoint" (PATCH al item) para setear el campo.
Mas control, pero mas trabajo. Solo si A y B no te convencen.

============================================================
## PAYLOAD que manda el tracker (referencia)
============================================================
{
  "sourceId": <id original>,
  "customer": "<Company>",
  "requestType": "<tipo RAW, ej. IFS NDA>",
  "details": "<detalles>",
  "authorEmail": "<correo creador o ''>",
  "authorClaim": "i:0#.f|membership|<correo>  o  ''",
  "projectContactClaim": "i:0#.f|membership|<correo BD>  o  ''",   <- puede venir ''
  "projectContactEmail": "<correo BD o ''>",
  "fceLeadClaim": "i:0#.f|membership|<correo FCE>  o  ''",
  "fceLeadEmail": "<correo FCE o ''>",
  "remainingTypes": "New DA;#Portal creation"
}

Claim vacio = ""  ->  ese es el caso a blindar (empty() lo detecta).

============================================================
## INPUT DEL CREATE ITEM (como debe quedar) - Solucion A
============================================================
{
  "type": "OpenApiConnection",
  "inputs": {
    "parameters": {
      "dataset": "https://intel.sharepoint.com/sites/ifs-igo-requests",
      "table": "052c84aa-6a91-469d-9b44-35d068acc422",
      "item/Title": "@triggerBody()?['customer']",
      "item/Priority/Value": "Medium",
      "item/RequestType": [ { "Value": "@{triggerBody()?['requestType']}" } ],
      "item/Details": "@triggerBody()?['details']",
      "item/AssignedFCELead/Claims": "@if(empty(triggerBody()?['fceLeadClaim']), null, triggerBody()?['fceLeadClaim'])",
      "item/Project_x0020_Contact": "@if(empty(triggerBody()?['projectContactClaim']), null, json('[]'))"
    },
    "host": {
      "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
      "connection": "shared_sharepointonline",
      "operationId": "PostItem"
    }
  },
  "runAfter": {}
}

NOTA sobre Project Contact en la Solucion A:
- Si el Code view es solo lectura en tu flow (ya nos paso), NO podras pegar esto.
  En ese caso usa la Solucion B (Condition con dos Create item), que se hace
  todo con la UI sin Code view.

============================================================
## COMO PROBAR EL BLINDAJE
============================================================
Prueba 1 (sin BD): en el tracker separa un Codename de un request que NO tenga
  Assigned BD. Debe crear el request nuevo SIN error.
Prueba 2 (con BD): separa uno que SI tenga BD. Debe copiar el BD normal.
Prueba 3 (real): con un request real de produccion (casi siempre trae BD/FCE).

Ver resultado en Power Automate > el flow > Run history (verde = ok, rojo = revisar).

============================================================
## LIMPIEZA
============================================================
Borrar en SharePoint los requests de prueba: 2713-2719 (empiezan con "TEST").
