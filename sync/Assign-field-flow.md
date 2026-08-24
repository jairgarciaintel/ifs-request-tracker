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
