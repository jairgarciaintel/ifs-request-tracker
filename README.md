# IFS Request Tracker

Landing page privada para **Jenn y Jair** que trackea el estatus granular
de cada request de la SharePoint List de IFS IGO.

## Arquitectura

```
SharePoint List (New DA Request)
    ↓  sync_sharepoint.py (cada 10 min o manual)
data/requests.json ← la landing page lee esto
data/requests.xlsx ← para referencia/backup en Excel
data/tracking.json ← estatus que Jenn y Jair ponen (compartido)
    ↑
server.py (sirve la page + guarda tracking.json)
    ↑
index.html (browser — ambos ven los mismos datos)
```

## Quick Start

### 1. Levantar el servidor local

```bash
cd Request-Tracker
python server.py
```

Abre `http://localhost:8080` — verás los requests con demo data.

### 2. Sincronizar con SharePoint (primera vez)

```bash
pip install office365-rest-python-client openpyxl
python sync_sharepoint.py
```

Te pedirá tu email y password de Intel (se guarda en `.env`, no se commitea).

### 3. Usar

- Click en un request para expandir los sub-pasos
- Cambia los dropdowns — se guarda automáticamente en `data/tracking.json`
- Ambos (Jenn y tú) ven lo mismo si usan el mismo servidor
- **Export Excel** — descarga `.xlsx` con todos los requests y estatus
- **Export JSON** — descarga `.json` completo

## Estructura de Archivos

```
Request-Tracker/
├── index.html          # Landing page (abrir en browser via server.py)
├── Logo.png            # Intel Foundry logo
├── server.py           # Servidor local (Python) — sirve + guarda tracking
├── sync_sharepoint.py  # Script de sync con SharePoint → JSON + Excel
├── .env                # Credenciales (gitignored)
├── .gitignore
├── README.md
└── data/
    ├── requests.json   # Requests descargados de SharePoint
    ├── requests.xlsx   # Mismos datos en Excel
    └── tracking.json   # Estatus que ponen Jenn y Jair
```

## SharePoint Source

- **Site:** `https://intel.sharepoint.com/sites/ifs-igo-requests`
- **List:** `New DA Request`
- **View:** Customer View (`24767d4b-db10-43f1-83d2-4147c127b3f5`)

## Para el Data Server

Si quieres que corra 24/7 en tu servidor compartido:

```bash
# En el servidor (tmux o screen)
cd /path/to/Request-Tracker
python server.py &

# Cron para sync cada 10 minutos
crontab -e
*/10 * * * * cd /path/to/Request-Tracker && python sync_sharepoint.py >> sync.log 2>&1
```

Jenn accede a `http://<server-ip>:8080` y listo.

---

## Hosting Challenge — Prompt for Intel AI

We need IT guidance on how to host this page within the Intel ecosystem.
Use the following prompt with Intel's internal AI assistant:

```
I need to host a custom HTML/JavaScript dashboard page that my teammate (Jenn Glavan) and I (Jair Garcia) can both access via a URL from our Intel PCs. The page needs to:

1. Read data from an existing SharePoint Online list via REST API:
   - Site: https://intel.sharepoint.com/sites/ifs-igo-requests
   - List: "New DA Request"
   - We both have admin access to this site

2. Allow both of us to update status fields (dropdowns) and have those changes persist so the other person can see them in real time (shared state, not just local browser storage)

3. Run custom JavaScript (fetch calls to SharePoint REST API, DOM manipulation, no frameworks — just vanilla JS)

Our constraints:
- We do NOT have Script Editor or Content Editor web parts available in our SharePoint modern experience
- Custom Script feature is blocked at the tenant level (we get a correlation ID error when trying to activate it)
- We do NOT have access to a custom server to host the page
- We need this accessible via a simple URL that both of us can open from our Intel browsers (where we are already authenticated to SharePoint)

What are our options within the Intel environment to host this page? Specifically:

A) Is there a way to enable custom JavaScript execution on a SharePoint page in our site?
B) Can we request Custom Script to be enabled for our specific site collection?
C) Is there an internal Intel platform (like an internal app hosting service, Azure Web App, or internal portal) where we can host a static HTML page that can make authenticated calls to SharePoint?
D) Can we use Power Pages, Power Apps Portal, or any other Microsoft/Intel tool to achieve this?
E) Is there a way to use SharePoint Framework (SPFx) for this without needing a full development environment setup?

Our ideal solution is the simplest path to get a single HTML page running with JavaScript that reads/writes to our SharePoint list, accessible by both of us via URL.
```

---

## Status

- [x] Frontend built (index.html with grouped cards, SVG icons, dropdowns)
- [x] SharePoint REST API integration coded
- [x] Excel + JSON export working
- [x] Demo mode working
- [ ] **BLOCKED: Need hosting solution within Intel network** — awaiting IT guidance
- [ ] Connect to live SharePoint data
- [ ] Shared tracking persistence (both Jenn and Jair see same state)







reepsonse 

IFS Request Tracker - Hosting Options Analysis
Your Situation Summary
Constraint	Status
SharePoint Custom Script	❌ Blocked (tenant level)
Script Editor / Content Editor Web Part	❌ Not available (modern experience)
Custom server access	❌ Not available
SharePoint admin access (site collection)	✅ Yes
Intel browser auth to SharePoint	✅ Already authenticated
Both need read/write access	✅ Yes
Options Ranked by Simplicity
✅ Option A — SharePoint Custom Script Enable (Request It)
Can you request it? Yes — this is your cleanest path.
Even though it's blocked tenant-wide, SharePoint admins can enable it per site collection.
What to do:
Submit a request to your Intel IT / M365 tenant admin team
Ask them to run this PowerShell against your specific site:
POWERSHELL
# They would run this — not you
Set-SPOSite -Identity "https://intel.sharepoint.com/sites/ifs-iao-requests" `
            -DenyAddAndCustomizePages 0
Once enabled, you can use the Script Editor web part (classic) or embed via a SharePoint Framework workaround
Pros:
Cleanest solution
Stays within SharePoint
Auth is automatic (already logged in)
Cons:
Requires IT ticket/approval
May be denied due to security policy
Timeline unknown
Likelihood of approval: Medium — site-scoped requests are commonly granted for admin-owned sites
✅ Option B — SharePoint Framework (SPFx) Web Part (Recommended if IT is slow)
This does NOT require Custom Script to be enabled.
SPFx is the official Microsoft-supported way to run custom JavaScript on modern SharePoint pages. It deploys through the App Catalog and bypasses the Custom Script restriction entirely.
Minimal Setup Path (Less scary than it sounds):
Step 1 — One-time environment setup (your machine):
BASH
# Install Node.js LTS (v18) from Intel Software Center or nodejs.org
node --version  # confirm

# Install SPFx toolchain
npm install -g @microsoft/generator-sharepoint
npm install -g yo gulp-cli
Step 2 — Scaffold your web part:
BASH
mkdir ifs-tracker && cd ifs-tracker
yo @microsoft/sharepoint
# Answer the prompts: > Solution name: ifs-request-tracker > Target: SharePoint Online only > Type: WebPart > Framework: No JavaScript framework ← important for your vanilla JS goal > Web part name: IFSRequestTracker
Step 3 — Write your vanilla JS inside the generated web part:
TYPESCRIPT
// src/webparts/ifsRequestTracker/IfsRequestTrackerWebPart.ts
// You write plain JS/HTML here — TypeScript wrapper is minimal

public render(): void {
  this.domElement.innerHTML = `
    <div id="ifs-dashboard">
      <h2>IFS Request Tracker</h2>
      <div id="request-table-container">Loading...</div>
    </div>
  `;
  
  this._loadRequests();
}

private async _loadRequests(): Promise<void> {
  const siteUrl = this.context.pageContext.web.absoluteUrl;
  
  // SharePoint REST API call — auth is AUTOMATIC via SPFx context
  const response = await fetch(
    `${siteUrl}/_api/web/lists/getbytitle('New DA Request')/items?$top=500`,
    {
      headers: {
        'Accept': 'application/json;odata=verbose',
        // SPFx handles auth cookies automatically — no token needed
      }
    }
  );
  
  const data = await response.json();
  this._renderTable(data.d.results);
}

private _renderTable(items: any[]): void {
  const container = document.getElementById('request-table-container');
  
  let html = `
    <table border="1" style="width:100%; border-collapse:collapse;">
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Status</th>
          <th>Requestor</th>
          <th>Update Status</th>
        </tr>
      </thead>
      <tbody>
  `;
  
  items.forEach(item => {
    html += `
      <tr>
        <td>${item.Id}</td>
        <td>${item.Title || ''}</td>
        <td>${item.Status || 'Not Set'}</td>
        <td>${item.Requestor || ''}</td>
        <td>
          <select 
            data-item-id="${item.Id}" 
            onchange="window.ifsTracker.updateStatus(this)"
          >
            <option value="New" ${item.Status === 'New' ? 'selected' : ''}>New</option>
            <option value="In Progress" ${item.Status === 'In Progress' ? 'selected' : ''}>In Progress</option>
            <option value="Pending" ${item.Status === 'Pending' ? 'selected' : ''}>Pending</option>
            <option value="Complete" ${item.Status === 'Complete' ? 'selected' : ''}>Complete</option>
            <option value="Cancelled" ${item.Status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
          </select>
        </td>
      </tr>
    `;
  });
  
  html += `</tbody></table>`;
  container.innerHTML = html;
}
Step 4 — Handle status updates (writes back to SharePoint):
TYPESCRIPT
// Add this to your web part class
private async _updateStatus(selectElement: HTMLSelectElement): Promise<void> {
  const itemId = selectElement.getAttribute('data-item-id');
  const newStatus = selectElement.value;
  const siteUrl = this.context.pageContext.web.absoluteUrl;
  
  // Get Request Digest for write operations
  const digestResponse = await fetch(`${siteUrl}/_api/contextinfo`, {
    method: 'POST',
    headers: { 'Accept': 'application/json;odata=verbose' }
  });
  const digestData = await digestResponse.json();
  const requestDigest = digestData.d.GetContextWebInformation.FormDigestValue;
  
  // PATCH the list item
  const updateResponse = await fetch(
    `${siteUrl}/_api/web/lists/getbytitle('New DA Request')/items(${itemId})`,
    {
      method: 'POST',
      headers: {
        'Accept': 'application/json;odata=verbose',
        'Content-Type': 'application/json;odata=verbose',
        'X-RequestDigest': requestDigest,
        'X-HTTP-Method': 'MERGE',
        'IF-MATCH': '*'
      },
      body: JSON.stringify({
        '__metadata': { 'type': 'SP.Data.New_x0020_DA_x0020_RequestListItem' },
        'Status': newStatus
      })
    }
  );
  
  if (updateResponse.ok) {
    console.log(`✅ Item ${itemId} updated to: ${newStatus}`);
    // Show confirmation to user
    selectElement.style.backgroundColor = '#d4edda';
    setTimeout(() => selectElement.style.backgroundColor = '', 2000);
  } else {
    console.error('❌ Update failed:', await updateResponse.text());
    alert('Update failed — check console for details');
  }
}
Step 5 — Build and deploy:
BASH
# Build
gulp build
gulp bundle --ship
gulp package-solution --ship

# This creates: sharepoint/solution/ifs-request-tracker.sppkg
Step 6 — Deploy to App Catalog:
1. Go to: https://intel.sharepoint.com/sites/appcatalog (or ask IT for your tenant app catalog URL) 2. Upload the .sppkg file 3. Click "Deploy" when prompted 4. Go to your site → Site Contents → Add an App → IFS Request Tracker 5. Add the web part to any SharePoint page 6. Share that page URL with Jenn
Pros:
✅ No Custom Script needed
✅ Auth is completely automatic
✅ Real shared state (writes to SharePoint list — both see same data)
✅ Official Microsoft supported path
✅ Vanilla JS is totally fine inside SPFx
Cons:
Requires App Catalog access (you may need IT to deploy the .sppkg)
One-time setup of Node/toolchain (~30 min)
✅ Option C — SharePoint-Hosted Page via Site Assets (Quickest Hack)
No server needed. Uses SharePoint itself as the host.
This works because .aspx files in Site Assets can contain HTML/JS if you access them directly — but note this has limitations with auth for API calls.
Better version — use a .html file in Site Assets + iframe workaround:
1. Go to your site → Site Contents → Site Assets library 2. Upload your HTML file: ifs-dashboard.html 3. Direct URL becomes: https://intel.sharepoint.com/sites/ifs-iao-requests/SiteAssets/ifs-dashboard.html
Your HTML file:
HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>IFS Request Tracker</title>
  <style>
    body { font-family: Segoe UI, sans-serif; margin: 20px; background: #f3f2f1; }
    h1 { color: #0078d4; }
    table { width: 100%; border-collapse: collapse; background: white; }
    th { background: #0078d4; color: white; padding: 10px; text-align: left; }
    td { padding: 8px 10px; border-bottom: 1px solid #edebe9; }
    tr:hover { background: #f3f2f1; }
    select { padding: 4px 8px; border-radius: 4px; border: 1px solid #8a8886; }
    .status-badge { 
      padding: 3px 8px; border-radius: 12px; font-size: 12px; font-weight: 600;
    }
    .status-new { background: #ddf4ff; color: #0550ae; }
    .status-inprogress { background: #fff8c5; color: #9a6700; }
    .status-complete { background: #dafbe1; color: #116329; }
    .status-cancelled { background: #ffebe9; color: #cf222e; }
    #refresh-btn { 
      background: #0078d4; color: white; border: none; 
      padding: 8px 16px; border-radius: 4px; cursor: pointer; margin-bottom: 16px;
    }
    #last-updated { color: #605e5c; font-size: 12px; margin-left: 12px; }
    #status-msg { color: green; font-weight: bold; margin-left: 12px; }
  </style>
</head>
<body>

<h1>📋 IFS Request Tracker</h1>
<p>Site: <code>ifs-iao-requests</code> | List: <code>New DA Request</code></p>

<button id="refresh-btn" onclick="loadRequests()">🔄 Refresh</button>
<span id="last-updated"></span>
<span id="status-msg"></span>

<div id="container">Loading requests...</div>

<script>
  // ============================================================
  // CONFIGURATION
  // ============================================================
  const SITE_URL = 'https://intel.sharepoint.com/sites/ifs-iao-requests';
  const LIST_NAME = 'New DA Request';
  
  // Adjust these to match your actual column internal names
  // Go to List Settings → click column name → check URL for 'Field=' parameter
  const COLUMNS = {
    id: 'Id',
    title: 'Title',
    status: 'Status',           // ← update to your actual internal name
    requestor: 'Requestor',     // ← update to your actual internal name  
    priority: 'Priority',       // ← update to your actual internal name
    created: 'Created',
    modified: 'Modified'
  };
  
  const STATUS_OPTIONS = [
    'New',
    'In Progress', 
    'Pending Review',
    'Approved',
    'In Development',
    'Complete',
    'Cancelled',
    'On Hold'
  ];

  // ============================================================
  // LOAD REQUESTS FROM SHAREPOINT
  // ============================================================
  async function loadRequests() {
    document.getElementById('container').innerHTML = 'Loading...';
    document.getElementById('status-msg').textContent = '';
    
    const selectFields = Object.values(COLUMNS).join(',');
    const url = `${SITE_URL}/_api/web/lists/getbytitle('${encodeURIComponent(LIST_NAME)}')/items` +
                `?$select=${selectFields}&$orderby=Id desc&$top=500`;
    
    try {
      const response = await fetch(url, {
        credentials: 'include',  // ← uses your existing SharePoint session
        headers: {
          'Accept': 'application/json;odata=verbose'
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      renderTable(data.d.results);
      
      document.getElementById('last-updated').textContent = 
        `Last refreshed: ${new Date().toLocaleTimeString()}`;
        
    } catch (err) {
      document.getElementById('container').innerHTML = 
        `<p style="color:red;">❌ Error loading data: ${err.message}<br>
         Make sure you are logged into SharePoint in this browser.</p>`;
      console.error('Load error:', err);
    }
  }

  // ============================================================
  // RENDER TABLE
  // ============================================================
  function renderTable(items) {
    if (!items || items.length === 0) {
      document.getElementById('container').innerHTML = '<p>No items found.</p>';
      return;
    }
    
    let html = `
      <p style="color:#605e5c;">${items.length} requests found</p>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Current Status</th>
            <th>Requestor</th>
            <th>Priority</th>
            <th>Created</th>
            <th>Update Status</th>
          </tr>
        </thead>
        <tbody>
    `;
    
    items.forEach(item => {
      const statusClass = getStatusClass(item[COLUMNS.status]);
      const created = item[COLUMNS.created] 
        ? new Date(item[COLUMNS.created]).toLocaleDateString() 
        : '';
      
      html += `
        <tr id="row-${item.Id}">
          <td><strong>${item.Id}</strong></td>
          <td>${escapeHtml(item[COLUMNS.title] || '')}</td>
          <td>
            <span class="status-badge ${statusClass}">
              ${escapeHtml(item[COLUMNS.status] || 'Not Set')}
            </span>
          </td>
          <td>${escapeHtml(item[COLUMNS.requestor] || '')}</td>
          <td>${escapeHtml(item[COLUMNS.priority] || '')}</td>
          <td>${created}</td>
          <td>
            <select 
              id="select-${item.Id}"
              data-item-id="${item.Id}"
              data-list-item-type="SP.Data.New_x0020_DA_x0020_RequestListItem"
              onchange="updateStatus(this)"
            >
              ${STATUS_OPTIONS.map(opt => 
                `<option value="${opt}" ${item[COLUMNS.status] === opt ? 'selected' : ''}>${opt}</option>`
              ).join('')}
            </select>
            <span id="msg-${item.Id}" style="font-size:11px;"></span>
          </td>
        </tr>
      `;
    });
    
    html += `</tbody></table>`;
    document.getElementById('container').innerHTML = html;
  }

  // ============================================================
  // UPDATE STATUS — WRITES BACK TO SHAREPOINT
  // ============================================================
  async function updateStatus(selectEl) {
    const itemId = selectEl.getAttribute('data-item-id');
    const newStatus = selectEl.value;
    const msgEl = document.getElementById(`msg-${itemId}`);
    
    msgEl.textContent = '⏳ Saving...';
    msgEl.style.color = 'orange';
    selectEl.disabled = true;
    
    try {
      // Step 1: Get form digest (required for write operations)
      const digestResponse = await fetch(`${SITE_URL}/_api/contextinfo`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Accept': 'application/json;odata=verbose' }
      });
      
      if (!digestResponse.ok) {
        throw new Error(`Could not get form digest: ${digestResponse.status}`);
      }
      
      const digestData = await digestResponse.json();
      const requestDigest = digestData.d.GetContextWebInformation.FormDigestValue;
      
      // Step 2: PATCH the list item
      const updateResponse = await fetch(
        `${SITE_URL}/_api/web/lists/getbytitle('${encodeURIComponent(LIST_NAME)}')/items(${itemId})`,
        {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Accept': 'application/json;odata=verbose',
            'Content-Type': 'application/json;odata=verbose',
            'X-RequestDigest': requestDigest,
            'X-HTTP-Method': 'MERGE',
            'IF-MATCH': '*'
          },
          body: JSON.stringify({
            '__metadata': { 
              'type': 'SP.Data.New_x0020_DA_x0020_RequestListItem' 
            },
            [COLUMNS.status]: newStatus
          })
        }
      );
      
      if (updateResponse.ok || updateResponse.status === 204) {
        msgEl.textContent = '✅ Saved!';
        msgEl.style.color = 'green';
        
        // Update the status badge in the same row
        const badge = document.querySelector(`#row-${itemId} .status-badge`);
        if (badge) {
          badge.textContent = newStatus;
          badge.className = `status-badge ${getStatusClass(newStatus)}`;
        }
        
        setTimeout(() => { msgEl.textContent = ''; }, 3000);
      } else {
        const errText = await updateResponse.text();
        throw new Error(`Update failed (${updateResponse.status}): ${errText}`);
      }
      
    } catch (err) {
      msgEl.textContent = '❌ Failed';
      msgEl.style.color = 'red';
      console.error('Update error:', err);
      alert(`Failed to update item ${itemId}:\n${err.message}`);
    } finally {
      selectEl.disabled = false;
    }
  }

  // ============================================================
  // HELPERS
  // ============================================================
  function getStatusClass(status) {
    if (!status) return '';
    const s = status.toLowerCase().replace(/\s+/g, '');
    if (s === 'new') return 'status-new';
    if (s === 'inprogress' || s === 'indevelopment') return 'status-inprogress';
    if (s === 'complete' || s === 'approved') return 'status-complete';
    if (s === 'cancelled') return 'status-cancelled';
    return '';
  }
  
  function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  // ============================================================
  // AUTO-REFRESH every 60 seconds
  // ============================================================
  loadRequests();
  setInterval(loadRequests, 60000);
</script>

</body>
</html>
How to deploy:
1. Go to: https://intel.sharepoint.com/sites/ifs-iao-requests/SiteAssets/ 2. Upload ifs-dashboard.html 3. Share this URL with Jenn: https://intel.sharepoint.com/sites/ifs-iao-requests/SiteAssets/ifs-dashboard.html 4. Both of you open it while logged into SharePoint → it works
Why this works for auth:
credentials: 'include' ← this line sends your existing SharePoint session cookies with every fetch call No OAuth tokens needed No CORS issues (same domain)
Pros:
✅ Zero infrastructure needed
✅ No IT tickets required
✅ Works immediately if you have Site Assets access
✅ Shared state is REAL (SharePoint list = single source of truth)
✅ Both users see same data — no localStorage needed
Cons:
⚠️ SharePoint may block script execution when opening .html directly
⚠️ Browser may show security warning
⚠️ No guarantee Intel's SharePoint config allows this
Test this first — it's the fastest option. Upload and open the URL. If scripts run, you're done.
✅ Option D — Microsoft Lists + Power Automate (No-Code Alternative)
If all JS options are blocked, this gives you shared state with zero code:
Microsoft Lists (built on SharePoint) → Custom Views → Conditional formatting (JSON) → Shared via URL
For status updates specifically:
Both you and Jenn can edit list items directly in Microsoft Lists
Create a custom view filtered/sorted how you want
Share the view URL — it's live for both of you
Limitation: No custom JS, but covers the core use case of shared status tracking.
✅ Option E — Power Apps Canvas App
Power Apps → Canvas App → SharePoint connector (built-in, no auth config needed) → Publish → Share with Jenn → Accessible via URL or Teams tab
Quick setup:
1. Go to make.powerapps.com 2. New App → Canvas → Tablet layout 3. Add Data → SharePoint → your site → "New DA Request" list 4. Insert → Gallery → connect to list 5. Add dropdown for status → OnChange: Patch(list, item, {Status: dropdown.Selected.Value}) 6. Publish → Share with Jenn's email 7. URL: https://apps.powerapps.com/play/[app-id]
Pros: No IT approval, built-in SharePoint auth, shareable URL Cons: Not vanilla JS, Power Apps formula language (but very simple for this use case)
Decision Matrix
Option	IT Approval Needed	Setup Time	Custom JS	Real Shared State	Reliability
A — Request Custom Script	✅ Yes	Days/weeks	✅ Full	✅ Yes	⭐⭐⭐⭐⭐
B — SPFx Web Part	Maybe (App Catalog)	2-4 hours	✅ Full	✅ Yes	⭐⭐⭐⭐⭐
C — Site Assets HTML	❌ No	15 minutes	✅ Full	✅ Yes	⭐⭐⭐ (test first)
D — Microsoft Lists	❌ No	30 minutes	❌ No	✅ Yes	⭐⭐⭐⭐
E — Power Apps	❌ No	1-2 hours	❌ No	✅ Yes	⭐⭐⭐⭐
My Recommended Path for You
Step 1 (TODAY — 15 min): Try Option C — upload the HTML file to Site Assets Test if scripts execute when you open the URL If yes → you're done, share URL with Jenn Step 2 (If C is blocked — same day): Try Option B — SPFx setup The toolchain install is the hardest part Once deployed, it's the most robust solution Step 3 (In parallel): Submit IT ticket for Custom Script enable on your site Reference: Microsoft docs on DenyAddAndCustomizePages This unblocks future development too
Finding Your Actual Column Internal Names
Before deploying, verify your SharePoint column internal names:
JAVASCRIPT
// Run this in browser console while on your SharePoint site
// to get ALL column internal names for your list
fetch("https://intel.sharepoint.com/sites/ifs-iao-requests/_api/web/lists/getbytitle('New DA Request')/fields?$select=Title,InternalName,TypeAsString", {
  credentials: 'include',
  headers: { 'Accept': 'application/json;odata=verbose' }
})
.then(r => r.json())
.then(d => d.d.results.forEach(f => 
  console.log(`${f.InternalName.padEnd(40)} | ${f.TypeAsString.padEnd(15)} | ${f.Title}`)
));
This will print every column's internal name — update the COLUMNS config object in the HTML accordingly.
Let me know which option you want to pursue and I can help you troubleshoot the specific steps!