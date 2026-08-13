# FS Request Tracker — User Guide

## What is this?

A private dashboard for Jenn and Jair to track the internal status of every DA Ops request. It pulls data directly from our SharePoint list and lets us mark progress on each step without going back to SharePoint for every update.

---

## How to Access

Open this URL in your browser:

**https://jairgarciaintel.github.io/ifs-request-tracker/**

The first time it opens, it will ask for your name (Jenn or Jair). Type it once and it remembers you.

---

## What You See

Each card is one request from SharePoint. It shows:

- **#ID** — the request number from SharePoint
- **Customer name** — who requested it
- **Colored badges** — the service types (Portal Creation, New DA, Codename, COD, etc.)
- **Status badge** — the current SharePoint status (Out for Signature, Complete, etc.)
- **Age badge** — how many days since it was created (green = fresh, amber = getting old, red = overdue)
- **Progress bar** — percentage of internal steps completed

---

## How to Use

### Opening a Request

Click on any card to expand it. Inside you will see:

1. **SharePoint Status dropdown** — change this to update the status in SharePoint directly (Info Requested, In Approval Loop, Out for Signature, WIP, Complete, etc.)

2. **Internal sub-steps** — the detailed steps we track internally:
   - Portal Creation: Create DA, Create Portal, Configure AGS, Configure JSM, Configure Security FT, Configure Access Mgmt, AGS Approved Role
   - New DA: Acknowledge, In Approval Loop, Add for Signature
   - COD/DA Edit: Info Request to BD, Route decision, then COD or DA Edit steps
   - Other types: single dropdown

3. **Notes** — free text field to write anything (IT ticket numbers, comments, etc.)

4. **View Change History** — click to see all changes made to this request with who and when

### Changing a Status

- Click the dropdown next to any step
- Select the new status
- It saves automatically (you will see your name appear next to it)
- The other person sees the change within 5 seconds

### SharePoint Sync

- When you change the **SharePoint Status** dropdown at the top of a card, it updates SharePoint directly
- You do NOT need to go to SharePoint to change the status anymore

---

## Filters

At the top you have:

- **Time filter**: All 2026 / This Month / Last Month / 2 Months Ago / 3 Months Ago
- **Type filter**: Filter by request type (Portal Creation, New DA, Codename, etc.)
- **Status filter**: All / Not Started / In Progress / Complete / Failed
- **Search**: Type a customer name or ID number

### Stat Pills (the colored buttons)

- Click **"69 WIP"** to show only Work in Progress requests
- Click **"224 done"** to show only completed
- Click **"39 new"** to show only new ones
- Click multiple to combine (e.g., WIP + New)
- Click **"332 total"** to show all

### Sort

- Newest First (ID) — default
- Oldest First (ID)
- Oldest Unresolved — prioritizes requests that have been waiting the longest

---

## Notifications

When the other person changes something, you see a banner at the top:

> **Jair** changed #2683 COD → Send for Signature: **Send for Signature**

It disappears after 8 seconds or click X to close it.

---

## Who is Working on What

When someone has a request open, the card gets an orange border and shows their name. This helps avoid working on the same request at the same time.

---

## Buttons

- **Sync** — refresh data from SharePoint right now (normally auto-refreshes every 10 min)
- **Excel** — download all data as an Excel file
- **JSON** — download all data as a JSON file
- **Expand All** — open all cards
- **Collapse All** — close all cards
- **Light/Dark** — toggle between dark and light mode

---

## Keyboard Shortcuts

- **Ctrl + E** — Expand all cards
- **Ctrl + W** — Collapse all cards
- **← →** — Navigate pages (when there are more than 50 requests)

---

## Data Flow (How It Works)

```
SharePoint List (New DA Request)
        ↕ (every 10 min via Power Automate)
FS Request Tracker (this page)
        ↕ (instant via Firebase)
Both Jenn and Jair see the same data
```

- New requests appear automatically (no manual export needed)
- Status changes you make here update SharePoint
- Internal step tracking is shared between both of us via Firebase
- Nothing you track internally overwrites anything in SharePoint unless you explicitly change the SharePoint Status dropdown

---

## Important Notes

- The internal sub-steps (Configure AGS, etc.) are ONLY visible here — they do not appear in SharePoint
- The SharePoint Status dropdown IS connected to SharePoint — changing it here changes it there
- If you both edit the same request at the same time, the last change wins
- Your progress is never lost — even if you refresh or close the browser

---

## FAQ

**Q: Do I need to install anything?**
A: No. Just open the URL in your browser.

**Q: Can other people see this?**
A: The URL is public but only people with the name prompt can edit. The data is only meaningful to DA Ops.

**Q: What if I make a mistake?**
A: Just change the dropdown back. All changes are logged in the history.

**Q: Does this replace SharePoint?**
A: No. SharePoint is still the official record. This is our internal tracking layer on top of it.

---

*Intel Foundry Services — DA Ops*
*Created: August 2026*
