# FIX 2 — el replace tronaba con DALink null

## Error
Action 'Condition' failed: 'replace' expects its first parameter to be a string.
The provided value is of type 'Null'.
Causa: hay requests con DALink = null (sin liga). replace() no acepta null.

## Solucion: envolver con coalesce(..., '') para convertir null en cadena vacia.

### OPCION A (simple) — una sola fila en la Condition
Lado izquierdo (fx) — pegar EXACTO:

replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(coalesce(item()?['DALink']?['Description'],''),'0',''),'1',''),'2',''),'3',''),'4',''),'5',''),'6',''),'7',''),'8',''),'9','')

Operador: is equal to
Derecha: VACIO

Con esto: puro numero -> TRUE -> copia. https/texto -> FALSE. 
null/vacio -> queda '' -> TRUE -> copiaria '' (no hace dano, deja DA Number vacio).

### OPCION B (recomendada) — evita tocar los vacios. DOS filas, conector And
Fila 1 (fx):
replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(coalesce(item()?['DALink']?['Description'],''),'0',''),'1',''),'2',''),'3',''),'4',''),'5',''),'6',''),'7',''),'8',''),'9','')
  Operador: is equal to     Derecha: VACIO

Fila 2 (fx):
coalesce(item()?['DALink']?['Description'],'')
  Operador: is not equal to     Derecha: VACIO

Conector (arriba izquierda): And
=> Solo copia cuando: es puro numero Y no esta vacio.

## Update item (rama TRUE) — sin cambios
Id (fx): item()?['Id']
DA Number (DA_x0020_Number) (fx): item()?['DALink']?['Description']
