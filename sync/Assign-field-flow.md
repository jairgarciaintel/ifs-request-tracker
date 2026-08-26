# Asignar request -> escribir "iGO Admin - Assigned To" (Person) en SharePoint

## El error "This expression has a problem"
Casi siempre es por las COMILLAS: al pegar, las comillas simples ' se vuelven
tipograficas ' ' y Power Automate no las reconoce. La doc de Microsoft dice:
borrar la expresion y ESCRIBIRLA A MANO para quitar caracteres ocultos.
(https://learn.microsoft.com/en-us/power-automate/error-reference)

Pero para evitarte pelear con la expresion, el tracker ahora manda el claim YA
ARMADO. Asi en el flow NO necesitas concat ni if: solo pones un token.

## Lo que manda el tracker ahora (ya deployado)
En la llamada de asignar manda:
- `assignedToEmail`  = "jair.garcia@intel.com"  (o "" si desasignas)
- `assignedToClaim`  = "i:0#.f|membership|jair.garcia@intel.com"  (o "" si desasignas)

## Configurar el flow (SIN expresiones) - Opcion facil
### 1. schema del trigger
En "When an HTTP request is received", agrega al JSON Schema:
    "assignedToEmail": { "type": "string" },
    "assignedToClaim": { "type": "string" }

### 2. En "Update item", campo Assigned To
El campo Person suele aparecer como "iGO Admin Only - Assigned To Claims".
  - Haz click en ese campo.
  - En el dynamic content elige el token  `assignedToClaim`  (el que manda el
    tracker). NADA de escribir expresiones. Solo el token.
  - Si tu conector muestra el campo pidiendo el email en vez del claim, entonces
    usa el token  `assignedToEmail`  en su lugar.

### 3. Guardar. No cambia la URL del flow.

Con esto, cuando asignas a Jair, el tracker manda el claim listo y el flow solo
lo coloca. Cuando desasignas, manda "" y el campo se limpia.

## Si de todas formas quieres usar la expresion (Opcion avanzada)
Escribela A MANO (no pegar) para evitar comillas curvas. Version sin `?`:

    if(empty(triggerBody()['assignedToEmail']),null,concat('i:0#.f|membership|',triggerBody()['assignedToEmail']))

Ojo: las comillas deben ser rectas '  no curvas ' '. Si al pegar falla, borra
y reescribe las comillas una por una, o mejor usa la Opcion facil de arriba.

## Probar
1. Tarjeta sin asignar -> boton Assign -> Jair -> Assign.
2. La tarjeta muestra "Jair Garcia" al instante.
3. En SharePoint el item queda con iGO Admin - Assigned To = Jair.
4. Assign -> Unassigned -> debe limpiarse en SharePoint.

## Nota: si al hacer Sync no se ve el asignado
El flow "Get all requests" quiza no incluye la columna iGOAdminOnly_x002d_AssignedTo
en su salida (en el debug del 2698 no venia). Si pasa eso, hay que agregar esa
columna al $select del flow de lectura. Avisar para verlo.


---

## ACTUALIZACION: campos que se MUESTRAN en la tarjeta (v1.8.38)
Aclaramos que hay 3 campos de personas distintos:
- iGO Admin Only - Assigned To  -> el que ASIGNAMOS/actualizamos desde el tracker
  (boton Assign). Es el que se muestra como "Assigned To".
- Assigned BD                    -> campo aparte, SOLO lectura, se muestra en la tarjeta.
- Assigned FCE Lead / Account Owner (AssignedFCELead) -> SOLO lectura, se muestra.

El tracker ahora muestra las 3 filas en la tarjeta. Assigned BD y FCE Lead son
informativos (no se editan aqui). Solo iGO Admin - Assigned To se edita/escribe.

## IMPORTANTE - para que se VEA el asignado tras Sync
El flow "Get all requests" (lectura) debe DEVOLVER estas columnas o no se veran
en la tarjeta aunque esten en SharePoint. En el debug del 2698 NO venia
iGOAdminOnly_x002d_AssignedTo. Revisar el flow de lectura y asegurar que el
$select / los campos incluyan:
  - iGOAdminOnly_x002d_AssignedTo   (Assigned To - el editable)
  - AssignedBD  (o el nombre interno real del campo "Assigned BD")
  - AssignedFCELead                 (FCE Lead / Account Owner)

Si "Assigned BD" no aparece, dime el nombre interno real (se ve en la URL al
editar esa columna en SharePoint, parametro Field=...) y lo ajusto en el tracker.
El tracker ya intenta varios nombres: AssignedBD, Assigned_x0020_BD, BD.


---

## v1.8.39 - dos problemas a resolver

### A) "Assigned To" no se guarda en SharePoint (campo Person)
El tracker manda bien el dato (se ve en consola: assignedToEmail y assignedToClaim
con formato i:0#.f|membership|...). El HTTP responde 202 (aceptado). El problema
esta en el paso "Update item" del flow: los campos Person a veces NO se llenan con
el claim en el token, o "aceptan" pero no resuelven al usuario.

PRIMERO revisa el Run history del flow -> la corrida -> paso "Update item":
  - Si esta ROJO: copia el error (Inputs/Outputs).
  - Si esta VERDE pero no llena: es el caso tipico de Person no resuelto.

Solucion recomendada (INFALIBLE) - usar "Send an HTTP request to SharePoint"
en vez de "Update item" para ese campo:

  1. Agrega accion "Send an HTTP request to SharePoint".
  2. Site Address: https://intel.sharepoint.com/sites/ifs-igo-requests
  3. Method: POST
  4. Uri:
     _api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items(@{triggerBody()?['id']})/validateUpdateListItem
  5. Headers:
     Accept: application/json;odata=nometadata
     Content-Type: application/json
  6. Body (resuelve el usuario por email con el formato Person):
     {
       "formValues": [
         {
           "FieldName": "iGOAdminOnly_x002d_AssignedTo",
           "FieldValue": "[{'Key':'i:0#.f|membership|@{triggerBody()?['assignedToEmail']}'}]"
         }
       ]
     }
  Nota: si assignedToEmail viene vacio (desasignar), manda FieldValue "[]".
  Se puede envolver en una Condition (si assignedToEmail vacio -> FieldValue "[]").

  Este metodo (validateUpdateListItem) es el que resuelve bien los campos Person.

Alternativa mas simple a probar primero en "Update item":
  - En el campo Person, en vez del claim, pon SOLO el email (token assignedToEmail).
  - Algunos conectores resuelven el usuario con solo el email.

### B) Campo "Assigned BD" no se trae
El FCE Lead (AssignedFCELead) SI se ve. El "Assigned BD" NO. Necesito el nombre
interno real de esa columna. Como verlo:
  - En SharePoint, ve a la lista -> List settings -> click en la columna "Assigned BD"
  - Mira la URL: al final dice  Field=XXXX   -> ese XXXX es el nombre interno.
  - Pasamelo y lo agrego. El tracker ya intenta: AssignedBD, Assigned_x0020_BD, BD,
    BusinessDevelopment, Assigned_BD. Si el real es otro, no lo agarra.
  - OJO: tambien el flow "Get all requests" debe DEVOLVER esa columna, o no llega
    al tracker aunque exista.

## Correo de Codename - destinatarios (v1.8.39)
Ahora el correo de Codename va al Assigned BD + FCE Lead / Account Owner (sus
emails). Si ninguno tiene email, cae al project contact / author. CC: fs.da.ops.
