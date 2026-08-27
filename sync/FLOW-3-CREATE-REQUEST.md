# FLOW 3 - Create Request (Separate) - ESTADO

Flow "FS Tracker Create Request" (workflow 589245b5). Conectado en el tracker
(CONFIG.createRequestUrl, v1.8.45+).

============================================================
## FUNCIONA (probado 2026-08-27)
============================================================
- Crea un request NUEVO con el servicio separado (Codename o IFS NDA).
- Deja el request ORIGINAL con los tipos restantes, INCLUSO VARIOS
  (ej. "New DA" + "Portal creation" juntos). El multi-valor SI funciona.
- CLAVE: hay que usar los NOMBRES EXACTOS de SharePoint (case/word sensitive):
    "New DA", "Portal creation" (c minuscula), "Code Name Request", "IFS NDA",
    "DA edit", "WebView AGS role", "MRUNDA", "MP-NDA", etc.
  El tracker ya manda requestTypeRaw (el nombre exacto), unidos por ;# .
  Ejemplo remainingTypes que SI guardo los dos: "New DA;#Portal creation".

============================================================
## PENDIENTE / BLINDAR (importante)
============================================================
Si un request NO tiene BD (Project Contact) o FCE Lead, el claim llega VACIO ("")
y el "Create item" TRUENA con:
    status 400 - "The specified user could not be found."
(visto cuando projectContactClaim / fceLeadClaim = "").

ARREGLO en el flow, paso "Create item", en los campos Person usar expresion que
mande null si viene vacio:

  Campo "Assigned FCE Lead or Account Owner Claims":
    if(empty(triggerBody()?['fceLeadClaim']), null, triggerBody()?['fceLeadClaim'])

  Campo "Assigned BD - Claims" (Project Contact):
    if(empty(triggerBody()?['projectContactClaim']), null, triggerBody()?['projectContactClaim'])

  (Opcional, si el Author tambien puede venir vacio, igual con authorClaim.)

Con eso, si falta BD o FCE Lead, crea el request sin esa persona en vez de fallar.

============================================================
## REGLA DE NEGOCIO (confirmada)
============================================================
- Codename  -> SIEMPRE en su propio request (se separa).
- IFS NDA   -> SIEMPRE en su propio request (se separa).
- New DA + Portal Creation -> se quedan JUNTOS (no se separan).
- El boton "Separate request" aparece cuando hay Codename o IFS NDA mezclado con
  otro servicio. Al darle: crea 1 request nuevo por cada standalone y deja el resto
  (New DA + Portal, etc.) en el original.

============================================================
## LIMPIEZA
============================================================
Requests de prueba creados hoy (borrar en SharePoint cuando quieras):
2713, 2714, 2715, 2716 (TEST ...).



{
    "host": {
        "connectionReferenceName": "shared_sharepointonline",
        "operationId": "PostItem"
    },
    "parameters": {
        "dataset": "https://intel.sharepoint.com/sites/ifs-igo-requests",
        "table": "052c84aa-6a91-469d-9b44-35d068acc422",
        "item/Title": "TEST blindaje sin BD",
        "item/Priority/Value": "Medium",
        "item/RequestType": [
            {
                "Value": "Code Name Request"
            }
        ],
        "item/Details": "prueba sin BD ni FCE",
        "item/AssignedFCELead/Claims": null,
        "item/Project_x0020_Contact": [
            {
                "Claims": ""
            }
        ]
    }
}

{
    "statusCode": 400,
    "headers": {
        "Cache-Control": "max-age=0, private",
        "Vary": "Origin",
        "X-FD-RouteKey": "intel",
        "X-NetworkStatistics": "0,1048279,43,130,754777,2096896,2096896,28756",
        "X-MSEdge-Ref": "MIRA: 2fe39426-6902-332e-95b1-b6fcfb165c1a SJ2PR07CA0016 2026-08-27T07:02:30.539Z",
        "X-1DSCollectorUrl": "https://mobile.events.data.microsoft.com/OneCollector/1.0/",
        "IsOCDI": "0",
        "Request-Id": "2fe39426-6902-332e-95b1-b6fcfb165c1a",
        "DATASERVICEVERSION": "3.0",
        "X-NanoProxy": "1",
        "SPRequestGuid": "80a3a91e-311c-42c2-91f3-57749cb1b32c",
        "X-FD-RouteKeyApplicationEndpointList": "206-IPV4V6.CLUMP.DPRODMGD105.AA-RT.SHAREPOINT.COM",
        "Content-Security-Policy": "frame-ancestors 'self' teams.microsoft.com *.teams.microsoft.com *.skype.com *.teams.microsoft.us local.teams.office.com teams.cloud.microsoft *.office365.com goals.cloud.microsoft *.powerapps.com *.powerbi.com *.yammer.com engage.cloud.microsoft word.cloud.microsoft excel.cloud.microsoft powerpoint.cloud.microsoft *.officeapps.live.com *.office.com *.microsoft365.com m365.cloud.microsoft *.cloud.microsoft *.stream.azure-test.net *.dynamics.com *.microsoft.com onedrive.live.com *.onedrive.live.com teams.microsoft.com *.teams.microsoft.com securebroker.sharepointonline.com;",
        "MicrosoftSharePointTeamServices": "16.0.0.27612",
        "MS-CV": "ojVDPZnAAPArae9tV9BhoQ.0",
        "X-FEServer": "SJ2PR07CA0016",
        "X-MS-SPConnector": "1",
        "SPClientServiceRequestDuration": "50",
        "SPLogId": "3d4335a2-c099-f000-2b69-ef6d57d061a1",
        "X-AriaCollectorURL": "https://browser.pipe.aria.microsoft.com/Collector/3.0/",
        "X-SP-SERVERSTATE": "ReadOnly=0",
        "X-DataBoundary": "NONE",
        "X-BackEndHttpStatus": "400",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "SAMEORIGIN",
        "X-MS-InvokeApp": "1; RequireReadOnly",
        "X-Proxy-BackendServerStatus": "400",
        "X-Proxy-RoutingCorrectness": "1",
        "X-SharePointHealthScore": "1",
        "X-FirstHopCafeEFZ": "SJC",
        "Alt-Svc": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "P3P": "CP=\"ALL IND DSP COR ADM CONo CUR CUSo IVAo IVDo PSA PSD TAI TELo OUR SAMo CNT COM INT NAV ONL PHY PRE PUR UNI\"",
        "X-AspNet-Version": "4.0.30319",
        "x-ms-environment-id": "default-46c98d88-e344-4ed4-8496-4ed7712e255d",
        "x-ms-tenant-id": "46c98d88-e344-4ed4-8496-4ed7712e255d",
        "x-ms-subscription-id": "197bf86c-a8ec-4d89-9f88-cfbf4cdaab01",
        "x-ms-dlp-re": "postitem|False|2026-08-19T22:09:34.7182410+00:00",
        "x-ms-dlp-gu": "-|-",
        "x-ms-dlp-ef": "-|-/-|-|-|-|-",
        "x-ms-mip-sl": "-|-|-|-",
        "x-ms-au-creator-id": "2729280b-5169-4c3b-84ab-a3349cb8b8e2",
        "Timing-Allow-Origin": "*",
        "x-ms-apihub-cached-response": "false",
        "x-ms-apihub-obo": "false",
        "Date": "Thu, 27 Aug 2026 07:02:30 GMT",
        "Content-Length": "193",
        "Content-Type": "application/json",
        "Expires": "Wed, 12 Aug 2026 07:02:30 GMT",
        "Last-Modified": "Thu, 27 Aug 2026 07:02:30 GMT"
    },
    "body": {
        "status": 400,
        "message": "The specified user  could not be found.\r\nclientRequestId: 80a3a91e-311c-42c2-91f3-57749cb1b32c\r\nserviceRequestId: 3d4335a2-c099-f000-2b69-ef6d57d061a1"
    }
}

