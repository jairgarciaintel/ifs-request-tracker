# FS Request Tracker - Project Brief (0 to 100) - for AI review

> PURPOSE: This document describes the whole project so an external AI (Gemini)
> can understand it end to end, assess its state, and suggest what to build next.
>
> SECURITY NOTE (read first): This file intentionally contains NO secrets.
> No API keys, no tokens, no PATs, no signed flow URLs. Flows are referenced by
> their workflow ID only. Never paste credentials into a document shared with an
> external AI. If the AI needs to "validate" something live, the human does it
> in a controlled way; secrets never leave Intel.

============================================================
## 1. WHAT IT IS (the elevator pitch)
============================================================
The FS Request Tracker is a single-page web app that helps the Intel Foundry
Services (IFS) DA Ops team (Jenn Glavan and Jair Garcia) track, in granular
detail, every request in the SharePoint list "New DA Request".

SharePoint is the official system of record. The tracker is an internal layer
ON TOP of SharePoint that:
- Pulls all requests live from SharePoint (every 10 min).
- Shows each request as a card with internal sub-steps only the team tracks.
- Writes some changes back to SharePoint (status, DA link/number, portal name,
  assigned owner).
- Sends branded customer emails automatically on status changes.
- Lets the two users collaborate in real time (shared tracking, notifications,
  presence, notes, history).

It is hosted as a static page on GitHub Pages. There is no backend server we own.
All "server" work is done by Power Automate flows and a Firebase Realtime DB.

============================================================
## 2. WHO USES IT
============================================================
- Jenn Glavan and Jair Garcia (IFS DA Ops). Only these two are authorized.
- Access control: user types their name on first load. Only "Jenn" or "Jair"
  are accepted (case-insensitive). 3 wrong attempts = blocked 24h on that browser.
  (This is light gating for a private internal tool, not hard security.)

============================================================
## 3. ARCHITECTURE (how the pieces fit)
============================================================
Frontend:
- One big index.html (HTML + CSS + vanilla JS, no framework, no build step).
- Hosted on GitHub Pages: https://jairgarciaintel.github.io/ifs-request-tracker/
- A separate guide/index.html is an animated slide-based user guide.

Data / integrations:
- SharePoint Online list "New DA Request" = source of truth.
- Power Automate flows (HTTP-triggered) are the bridge to SharePoint:
    * Get all requests            (workflow 88801fb7)
    * Update fields               (workflow 7c9ac8ba)  DA link/number, portal, assigned
    * Send emails                 (workflow 205f9f20)  all customer emails
    * Create request "Separate"   (workflow 589245b5)  splits Codename / IFS NDA
- Firebase Realtime DB = shared tracking state (sub-steps, notes, history,
  presence, notifications) synced between the two users in real time.
- GitHub API = used to persist a tracking.json fallback in the repo.
- Fallback data: data/requests.json (manual CSV/Excel export) if the live flow
  is down.

Data flow (read):  SharePoint -> Get-requests flow -> tracker renders cards.
Data flow (write): tracker -> Update/Send/Create flows -> SharePoint / email.
Collaboration:     tracker <-> Firebase (realtime, both users).

============================================================
## 4. KEY DOMAIN CONCEPTS
============================================================
Request types (SharePoint multi-choice). Each request can bundle several:
- Portal Creation (sub-steps: Create DA, Create Portal, Configure AGS, Configure
  JSM, Configure Security FT, Configure Access Mgmt, AGS Approved Role).
- New DA (Acknowledge, In Approval Loop, Add for Signature).
- COD (Send for Signature; shares Info Request + routing decision with DA Edit).
- DA Edit (In Approval Loop, Add for Signature; shares decision with COD).
- Single-step: Codename, WebView AGS Role, IFS NDA, MP-NDA, Portal Unencryption,
  Secure Chamber.
- Multi-Party equivalence: MPA-IC, MPA-NDA, MP-NDA, MRUNDA, Multi-Party are the
  SAME service; normalized to MP-NDA in emails.

Business rule (confirmed):
- Codename and IFS NDA must EACH live on their own request.
- New DA + Portal Creation stay together.
- The "Separate request" button creates a new request per standalone service and
  leaves the rest on the original.

SharePoint valid statuses: Info Requested, Acknowledged, In Approval Loop,
Out for Signature, WIP, IT Request Submitted, Complete, On Hold, Canceled.

People fields on each request:
- Assigned To (iGO Admin owner) - editable from the tracker.
- Assigned BD (Project Contact) - read-only; may be empty.
- FCE Lead / Account Owner - read-only; effectively required in SharePoint.

============================================================
## 5. FEATURES IMPLEMENTED (current: v1.8.49)
============================================================
- Grouped cards by request ID (one card, multiple service sections inside).
- Live pull from SharePoint every 10 min + manual Sync.
- SharePoint Status dropdown writes back to SharePoint.
- Automatic branded customer emails on status change (Acknowledged, Info
  Requested, Out for Signature, In Approval Loop, Complete). Per-service copy.
    * Two safety toggles: "Auto emails" (off = none) and "Test mode"
      (on = only Jair receives, no customer/CC).
    * Codename completion emails an encrypted (Intel-only) notice to BD + FCE Lead.
    * COD completion = double-confirmation, CCs specific people.
- Complete popup: asks Portal Name + DA Number (auto-fills from prior request of
  same customer).
- DA Link / DA Number capture popup on In Approval Loop.
- Assign popup: set owner (Jair/Jenn) -> writes to SharePoint; owner shown as chip.
- "Separate request" flow (Codename / IFS NDA) with correct RequestType.
- Filters: Time, Type (multi-select checkboxes), Assigned To, Tech Node, Status.
- Search: customer, ID, DA number, DA link, portal name, assignee.
- Clickable stat pills (WIP/Done/New/ack/canceled) multi-select.
- Sort: newest, oldest, oldest unresolved.
- Progress bar per card (50% in progress, 100% complete).
- Age badges (green <7d, amber 8-30d, red >30d).
- Notes/comments per request (shared).
- Change history viewer (who/what/when, last 20).
- Real-time notifications banner + presence indicator (who has a card open).
- Export Excel / JSON.
- Dark / Light mode.
- Expand/Collapse all + keyboard shortcuts (Ctrl+E, Ctrl+W, arrows for pages).
- Pagination (50 per page).
- New-ticket chime (Web Audio) toggle.
- Help chatbot (FAQ, keyword-based, no external AI) on tracker + guide, with a
  "Report it" button that emails bugs/features to Jair via the email flow.
- Animated background, versioned changelog, user guide (slides).

============================================================
## 6. KNOWN ISSUES / LIMITATIONS
============================================================
- Static public page: cannot hold secrets or run server code by itself.
- Power Automate HTTP (O365 connector) has failed calling EXTERNAL APIs in this
  tenant (got HTTP 411 with Firebase). This blocks some ideas (e.g. real AI via PA).
- No access to create a Google Cloud project (Intel org forces a parent org) or
  to register for external AI keys (Groq etc.). So a real-AI chatbot is on hold;
  current chatbot is a keyword FAQ.
- "Separate" flow: if a request has no Assigned BD (Project Contact empty), the
  Create item can fail (SharePoint "user could not be found") because the person
  array is [{Claims:""}]. Hardening documented (send null / conditional branch).
  Real requests almost always have BD, so it's an edge case.
- GitHub Pages caching: users sometimes need Cmd+Shift+R after a deploy.
- Access gating (name only) is light; fine for an internal 2-person tool.

============================================================
## 7. HOW IT IS DEPLOYED / MAINTAINED
============================================================
- Public repo (deploy): jairgarciaintel/ifs-request-tracker (this folder is the
  Request-Tracker/ subtree). GitHub Pages serves it.
- Private dev repo: jairgarciaintel/dashboards-strategy-2026 (workspace root).
- Deploy = edit index.html / guide -> version bump -> git commit + push to main.
  GitHub Pages updates in ~1-2 min.
- Versioning: APP_VERSION in index.html + CHANGELOG.md, bumped every deploy.
- Corporate laptop needs a git hooks workaround to push (Code Defender blocks it).
- Config (CONFIG object in index.html) holds the flow URLs and GitHub repo info.
  (URLs are omitted here on purpose - secrets stay out of this brief.)

============================================================
## 8. POSSIBLE NEXT DEVELOPMENTS (for the AI to weigh in on)
============================================================
Ideas already floated (not committed). Ask the AI to prioritize / critique /
propose better ones:
- Real-AI chatbot (blocked today by access + tenant 411; would need a serverless
  proxy like Cloudflare Workers/Vercel to hide a key, or a PA flow if the tenant
  allows external calls).
- Harden the "Separate" flow for requests without Assigned BD.
- Analytics/metrics view: aging, throughput, SLA compliance, per-owner load.
- Better SLA tracking and overdue alerts.
- Bulk actions (multi-select requests -> change status / assign).
- Audit/report export for management.
- Mobile layout polish.
- Replace name-only gating with real auth (e.g., Microsoft SSO) if it ever needs
  to open to more people.
- Reduce dependency on Power Automate reliability (connection drops, 411).

============================================================
## 9. WHAT WE WANT FROM THE AI REVIEW
============================================================
1. Rate the project 0-100 on: usefulness, architecture soundness, maintainability,
   reliability, security (for a 2-person internal tool). Explain each score.
2. Point out the biggest risks and quick wins.
3. Suggest the highest-value next features and a rough order to build them.
4. Flag anything fragile in the SharePoint / Power Automate / Firebase setup.
5. Keep advice practical for a no-backend, GitHub-Pages + Power Automate stack.

(Reminder: do not ask for or include any API keys, tokens, or signed URLs.)
