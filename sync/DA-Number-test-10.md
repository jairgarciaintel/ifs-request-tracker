# Probar el backfill solo con los ULTIMOS 10 requests

En el PASO 2 (Send an HTTP request to SharePoint), cambiar la Uri por esta
(top 10 + ordenado por Id descendente = los 10 mas nuevos):

_api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items?$select=Id,DALink&$top=10&$orderby=Id desc

Guardar. Test -> Manually -> Run.

Revisar en SharePoint esos 10:
- Los que tienen DA Link con numero PURO (ej. 19381, 4566) -> DA Number = ese numero.
- Los que tienen https:// o texto en la Description -> DA Number en BLANCO.

Cuando quede bien, regresar la Uri para toda la lista:
_api/web/lists(guid'052c84aa-6a91-469d-9b44-35d068acc422')/items?$select=Id,DALink&$top=5000

(El $orderby se puede dejar o quitar para el corrido completo; no afecta.)
