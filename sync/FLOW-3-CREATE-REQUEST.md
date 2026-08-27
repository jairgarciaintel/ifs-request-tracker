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



<<<<<<< HEAD

No dynamic content available
Empty dynamic content iconThere is no content available
Including dynamic content
If available, dynamic content is automatically generated from the connectors and actions you choose for your flow.

Dynamic content may also be added from other sources.
Learn more about dynamic content.
=======
============================================================
## BUG ENCONTRADO (2026-08-27): Create item crea siempre "Code Name Request"
============================================================
Sintoma: al separar un IFS NDA, el request nuevo salio como Codename, no IFS NDA.
Causa: en el flow, paso "Create item", el campo Request Type esta HARDCODEADO a
       "Code Name Request" (Value - 1 fijo), ignora el token del tracker.
El tracker SI manda el tipo correcto en el campo  requestType  (raw, ej. "IFS NDA").

ARREGLO (flow "FS Tracker Create Request" -> Create item):
1. Campo "Request Type" -> "Value - 1": borrar el texto fijo "Code Name Request".
2. Poner el DYNAMIC CONTENT del trigger:  requestType
   (asi usa lo que manda el tracker: IFS NDA, Codename, etc.)
3. Guardar.

Probar: separar un IFS NDA -> el request nuevo debe salir con RequestType = IFS NDA.
>>>>>>> 8e53e01adb7e5682bc835dff01203259fd05d53d


{
    "host": {
        "connectionReferenceName": "shared_sharepointonline",
        "operationId": "PostItem"
    },
    "parameters": {
        "dataset": "https://intel.sharepoint.com/sites/ifs-igo-requests",
        "table": "052c84aa-6a91-469d-9b44-35d068acc422",
        "item/Title": "TEST IFS NDA type",
        "item/Priority/Value": "Medium",
        "item/RequestType": [
            {
                "Value": "Code Name Request"
            }
        ],
        "item/Details": "verificar que crea IFS NDA",
        "item/AssignedFCELead/Claims": "i:0#.f|membership|puneet.sawhney@intel.com",
        "item/Project_x0020_Contact": [
            {
                "Claims": "i:0#.f|membership|jenn.glavan@intel.com"
            }
        ]
    }
}{
    "statusCode": 201,
    "headers": {
        "Cache-Control": "max-age=0, private",
        "Vary": "Origin",
        "X-FD-RouteKey": "intel",
        "X-NetworkStatistics": "3,523917,40,627,8423215,12736038,12736038,32812",
        "X-MSEdge-Ref": "MIRA: 8fa561b7-ce29-e838-530f-ea8115f991bb BY1P220CA0020 2026-08-27T07:32:25.695Z",
        "X-1DSCollectorUrl": "https://mobile.events.data.microsoft.com/OneCollector/1.0/",
        "IsOCDI": "0",
        "Request-Id": "8fa561b7-ce29-e838-530f-ea8115f991bb",
        "DATASERVICEVERSION": "3.0",
        "X-NanoProxy": "1",
        "SPRequestGuid": "982aa47e-56ef-4c17-9a49-f3b516e51a50",
        "X-FD-RouteKeyApplicationEndpointList": "206-IPV4V6.CLUMP.DPRODMGD105.AA-RT.SHAREPOINT.COM",
        "Content-Security-Policy": "frame-ancestors 'self' teams.microsoft.com *.teams.microsoft.com *.skype.com *.teams.microsoft.us local.teams.office.com teams.cloud.microsoft *.office365.com goals.cloud.microsoft *.powerapps.com *.powerbi.com *.yammer.com engage.cloud.microsoft word.cloud.microsoft excel.cloud.microsoft powerpoint.cloud.microsoft *.officeapps.live.com *.office.com *.microsoft365.com m365.cloud.microsoft *.cloud.microsoft *.stream.azure-test.net *.dynamics.com *.microsoft.com onedrive.live.com *.onedrive.live.com teams.microsoft.com *.teams.microsoft.com securebroker.sharepointonline.com;",
        "MicrosoftSharePointTeamServices": "16.0.0.27612",
        "MS-CV": "ojVE897QAPArae2TYMOzSQ.0",
        "X-FEServer": "BY1P220CA0020",
        "X-MS-SPConnector": "1",
        "SPClientServiceRequestDuration": "338",
        "SPLogId": "f34435a2-d0de-f000-2b69-ed9360c3b349",
        "X-AriaCollectorURL": "https://browser.pipe.aria.microsoft.com/Collector/3.0/",
        "X-SP-SERVERSTATE": "ReadOnly=0",
        "X-DataBoundary": "NONE",
        "X-BackEndHttpStatus": "201",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "SAMEORIGIN",
        "X-MS-InvokeApp": "1; RequireReadOnly",
        "X-Proxy-BackendServerStatus": "201",
        "X-Proxy-RoutingCorrectness": "1",
        "X-SharePointHealthScore": "3",
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
        "Date": "Thu, 27 Aug 2026 07:32:25 GMT",
        "Content-Length": "3903",
        "Content-Type": "application/json; charset=utf-8",
        "Expires": "Wed, 12 Aug 2026 07:32:25 GMT",
        "Last-Modified": "Thu, 27 Aug 2026 07:32:25 GMT"
    },
    "body": {
        "@odata.etag": "\"1\"",
        "ItemInternalId": "2718",
        "ID": 2718,
        "Title": "TEST IFS NDA type",
        "Created": "2026-08-27T07:32:26Z",
        "TechNode": [],
        "TechNode@odata.type": "#Collection(Microsoft.Azure.Connectors.SharePoint.SPListExpandedReference)",
        "TechNode#Id": [],
        "TechNode#Id@odata.type": "#Collection(Int64)",
        "Author": {
            "@odata.type": "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
            "Claims": "i:0#.f|membership|jair.garcia@intel.com",
            "DisplayName": "Garcia, Jair",
            "Email": "jair.garcia@intel.com",
            "Picture": "https://intel.sharepoint.com/sites/ifs-igo-requests/_layouts/15/UserPhoto.aspx?Size=L&AccountName=jair.garcia@intel.com",
            "Department": "INTEGRATED CUSTOMER SOLUTIONS",
            "JobTitle": "11571195"
        },
        "Author#Claims": "i:0#.f|membership|jair.garcia@intel.com",
        "Priority": {
            "@odata.type": "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedReference",
            "Id": 2,
            "Value": "Medium"
        },
        "Priority#Id": 2,
        "RequestType": [
            {
                "@odata.type": "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedReference",
                "Id": 1,
                "Value": "Code Name Request"
            }
        ],
        "RequestType@odata.type": "#Collection(Microsoft.Azure.Connectors.SharePoint.SPListExpandedReference)",
        "RequestType#Id": [
            1
        ],
        "RequestType#Id@odata.type": "#Collection(Int64)",
        "Details": "verificar que crea IFS NDA",
        "AssignedFCELead": {
            "@odata.type": "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
            "Claims": "i:0#.f|membership|puneet.sawhney@intel.com",
            "DisplayName": "Sawhney, Puneet",
            "Email": "puneet.sawhney@intel.com",
            "Picture": "https://intel.sharepoint.com/sites/ifs-igo-requests/_layouts/15/UserPhoto.aspx?Size=L&AccountName=puneet.sawhney@intel.com",
            "Department": "14A ETO TECH MKTG & PLATFORM",
            "JobTitle": "11954410"
        },
        "AssignedFCELead#Claims": "i:0#.f|membership|puneet.sawhney@intel.com",
        "Editor": {
            "@odata.type": "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
            "Claims": "i:0#.f|membership|jair.garcia@intel.com",
            "DisplayName": "Garcia, Jair",
            "Email": "jair.garcia@intel.com",
            "Picture": "https://intel.sharepoint.com/sites/ifs-igo-requests/_layouts/15/UserPhoto.aspx?Size=L&AccountName=jair.garcia@intel.com",
            "Department": "INTEGRATED CUSTOMER SOLUTIONS",
            "JobTitle": "11571195"
        },
        "Editor#Claims": "i:0#.f|membership|jair.garcia@intel.com",
        "Project_x0020_Contact": [
            {
                "@odata.type": "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
                "Claims": "i:0#.f|membership|jenn.glavan@intel.com",
                "DisplayName": "Glavan, Jenn",
                "Email": "jenn.glavan@intel.com",
                "Picture": "https://intel.sharepoint.com/sites/ifs-igo-requests/_layouts/15/UserPhoto.aspx?Size=L&AccountName=jenn.glavan@intel.com",
                "Department": "INTEGRATED CUSTOMER SOLUTIONS",
                "JobTitle": "10554118"
            }
        ],
        "Project_x0020_Contact@odata.type": "#Collection(Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser)",
        "Project_x0020_Contact#Claims": [
            "i:0#.f|membership|jenn.glavan@intel.com"
        ],
        "Project_x0020_Contact#Claims@odata.type": "#Collection(String)",
        "iGOAdminOnly_x002d_Contracttype": {
            "@odata.type": "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedReference",
            "Id": 3,
            "Value": "NTD"
        },
        "iGOAdminOnly_x002d_Contracttype#Id": 3,
        "Modified": "2026-08-27T07:32:26Z",
        "{Identifier}": "Lists%252fNew%2bDA%2bRequest%252f2718_.000",
        "{IsFolder}": false,
        "{Thumbnail}": {
            "Large": null,
            "Medium": null,
            "Small": null
        },
        "{Link}": "https://intel.sharepoint.com/sites/ifs-igo-requests/_layouts/15/listform.aspx?PageType=4&ListId=052c84aa%2D6a91%2D469d%2D9b44%2D35d068acc422&ID=2718&ContentTypeID=0x0100F37EA9E070FDB147A8961682D0C6335200CDB1CB2B0187494798E496B0B8DB2F35",
        "{Name}": "TEST IFS NDA type",
        "{FilenameWithExtension}": "TEST IFS NDA type",
        "{Path}": "Lists/New DA Request/",
        "{FullPath}": "Lists/New DA Request/2718_.000",
        "{ContentType}": {
            "@odata.type": "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedContentType",
            "Id": "0x0100F37EA9E070FDB147A8961682D0C6335200CDB1CB2B0187494798E496B0B8DB2F35",
            "Name": "Item"
        },
        "{ContentType}#Id": "0x0100F37EA9E070FDB147A8961682D0C6335200CDB1CB2B0187494798E496B0B8DB2F35",
        "{HasAttachments}": false,
        "{VersionNumber}": "1.0"
    }
}