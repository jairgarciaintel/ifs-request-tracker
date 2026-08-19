# FIX Condition del backfill — solo copiar si el Description es PURO numero

## Problema
Algunos Description del DA Link no son el numero: traen https://, texto, ":", "/", etc.
Solo queremos copiar a DA Number cuando el Description sea unicamente digitos
(cualquier largo: 4566, 19381, etc). Si tiene cualquier letra/simbolo, dejar vacio.

## Cambio en la Condition (Apply to each -> Condition)
Reemplazar la condicion por UNA sola fila:

- Lado izquierdo (pestaña fx / expresion) — quita todos los digitos al Description:

replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(item()?['DALink']?['Description'],'0',''),'1',''),'2',''),'3',''),'4',''),'5',''),'6',''),'7',''),'8',''),'9','')

- Operador: is equal to
- Lado derecho: VACIO

## Logica
La expresion le quita 0-9 al texto:
- "19381"       -> ""             (queda vacio -> ES numero -> TRUE -> copiar)
- "4566"        -> ""             (TRUE -> copiar)
- "https://1a1" -> "https://a"    (NO vacio -> NO es numero -> FALSE -> no copiar)
- "" o null     -> ""             (entraria a TRUE, pero copiar "" no hace dano;
                                    si molesta, ver nota abajo)

## (Opcional) evitar tambien el caso vacio/null
Si quieres que ademas NO toque los que vienen totalmente vacios, cambia "And" y
agrega una 2a fila:
  Fila 1 (la de arriba): expresion replace(...) is equal to (VACIO)
  Fila 2: item()?['DALink']?['Description']  is not equal to  (VACIO)
  Conector: And
Asi solo copia cuando: es puro numero Y no esta vacio.

## Update item (rama TRUE) — sin cambios
Id (fx): item()?['Id']
DA Number (DA_x0020_Number) (fx): item()?['DALink']?['Description']


Flow run failed. Action 'Condition' failed: Unable to process template language expressions for action 'Condition' at line '0' and column '0': 'The template language function 'replace' expects its first parameter 'string' to be a string. The provided value is of type 'Null'. Please see https://aka.ms/logicexpressions#replace for usage details.'.