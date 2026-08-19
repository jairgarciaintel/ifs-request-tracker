# FIX — orderby "mas nuevos primero" (Z a A por Id)

El problema del $orderby suele ser el ESPACIO en "Id desc". En la Uri hay que
codificar el espacio como %20.

## OPCION 1 — orderby por Id descendente (mas nuevo primero), top 10
_api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items?$select=Id,DALink&$top=10&$orderby=Id%20desc

## OPCION 2 (si orderby sigue fallando) — filtrar por Id mayor que X
Pon un numero ~10 por debajo de tu ID mas alto. Ej. si el mas nuevo es 2693, usa 2683:
_api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items?$select=Id,DALink&$filter=Id%20gt%202683&$top=100

  (Id%20gt%202683  =  "Id gt 2683"  =  Id mayor que 2683)

## Para toda la lista al final (sin filtro)
_api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items?$select=Id,DALink&$top=5000

NOTA: recordar que la Condition ya debe usar coalesce(...) (fix2) para no tronar con
DALink null.
