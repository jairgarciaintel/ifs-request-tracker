# Asignar request desde el frontend -> escribir "iGO Admin - Assigned To" en SharePoint

## Que hace el tracker (ya deployado)
- En cada tarjeta, junto a "Assigned To", hay un boton **Assign** (o **Change**).
- Abre un popup con un dropdown: Unassigned + los miembros del equipo
  (Jair Garcia, Jenn Glavan). Para agregar mas personas, editar la lista
  `TEAM_MEMBERS` en index.html.
- Al confirmar, el tracker:
  1. Actualiza la tarjeta al instante.
  2. Llama al flow updateFieldsUrl con:  { id, assignedToEmail: "<email>" }
     (assignedToEmail vacio "" = desasignar)

## Lo que falta en el flow (Update Fields - workflow 7c9ac8ba)
Hay que aceptar `assignedToEmail` y escribirlo al campo Person
`iGOAdminOnly_x002d_AssignedTo`.

### Paso 1 - schema del trigger
En "When an HTTP request is received", agrega al JSON Schema:
    "assignedToEmail": { "type": "string" }

### Paso 2 - escribir el campo Person en "Update item"
El campo Assigned To es tipo Person. En el conector SharePoint "Update item",
los campos Person suelen aparecer como "<Campo> Claims" (Assigned To Claims).

  - En el campo  "iGO Admin Only - Assigned To Claims"  pon una expresion que
    mande el claim del usuario cuando venga email, y vacio cuando no:

      if(empty(triggerBody()?['assignedToEmail']), null, concat('i:0#.f|membership|', triggerBody()?['assignedToEmail']))

    (El formato de claim de SharePoint es  i:0#.f|membership|correo@intel.com )

  - Si tu conector muestra el campo como "Assigned To" que pide directamente el
    email (algunas versiones aceptan solo el email), entonces usa:
      if(empty(triggerBody()?['assignedToEmail']), null, triggerBody()?['assignedToEmail'])

### Paso 3 - Guardar. No cambia la URL del flow.

## Nota sobre desasignar
Mandar assignedToEmail = "" debe LIMPIAR el campo. Con la expresion de arriba
manda null cuando viene vacio. Si el conector no limpia con null, quiza haya que
una Condition: si assignedToEmail vacio -> no tocar el campo (o setearlo a null
segun lo permita el conector).

## Probar
1. En una tarjeta sin asignar, boton **Assign** -> elige Jair -> Assign.
2. La tarjeta debe mostrar "Jair Garcia" al instante.
3. En SharePoint, el item debe quedar con iGO Admin - Assigned To = Jair.
4. Volver a abrir, elegir Unassigned -> debe limpiarse en SharePoint.
