---
name: workplace-productivity-documents-suite
description: >-
  Workplace SaaS & Document Engineering Suite: Google Workspace automation, Linear issue tracking, Notion databases, Nano-PDF processing, PowerPoint slides, and OCR document parsing.
version: 2.0.0
tags:
  - productivity
  - notion
  - linear
  - google-workspace
  - pdf
  - ocr
  - powerpoint
merged_member_skills:
  - google-workspace (01_Hermes_Skills_Core_Library\productivity\google-workspace\SKILL.md)
  - linear (01_Hermes_Skills_Core_Library\productivity\linear\SKILL.md)
  - nano-pdf (01_Hermes_Skills_Core_Library\productivity\nano-pdf\SKILL.md)
  - notion (01_Hermes_Skills_Core_Library\productivity\notion\SKILL.md)
  - ocr-and-documents (01_Hermes_Skills_Core_Library\productivity\ocr-and-documents\SKILL.md)
  - powerpoint (01_Hermes_Skills_Core_Library\productivity\powerpoint\SKILL.md)
---

# Workplace Productivity Documents Suite

> **Master Suite Consolidée :** Regroupe et unifie **6 compétences spécialisées** de l'écosystème Hermes en une référence modulaire et cohérente.


## 🎯 Quand Déclencher cette Master Suite (Triggers)
Cette suite doit être activée dès que l'utilisateur mentionne l'un des mots-clés, frameworks, outils ou objectifs liés aux modules inclus ci-dessous.
Chaque module peut être exécuté individuellement ou orchestré en séquence selon la tâche demandée.

---
## 📋 Vue d'Ensemble & Sommaire des Modules

1. **[google-workspace](#module-1-google-workspace)** : Gmail, Calendar, Drive, Contacts, Sheets, and Docs integration for Hermes. Uses Hermes-managed OAuth2 setup, prefers the Google Workspace CLI (`gws`) when available for broader API coverage, and falls back to the Python client libraries otherwise.
2. **[linear](#module-2-linear)** : Manage Linear issues, projects, and teams via the GraphQL API. Create, update, search, and organize issues. Uses API key auth (no OAuth needed). All operations via curl — no dependencies.
3. **[nano-pdf](#module-3-nano-pdf)** : Edit PDFs with natural-language instructions using the nano-pdf CLI. Modify text, fix typos, update titles, and make content changes to specific pages without manual editing.
4. **[notion](#module-4-notion)** : Notion API for creating and managing pages, databases, and blocks via curl. Search, create, update, and query Notion workspaces directly from the terminal.
5. **[ocr-and-documents](#module-5-ocr-and-documents)** : Extract text from PDFs and scanned documents. Use web_extract for remote URLs, pymupdf for local text-based PDFs, marker-pdf for OCR/scanned docs. For DOCX use python-docx, for PPTX see the powerpoint skill.
6. **[powerpoint](#module-6-powerpoint)** : Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.

---

## Module 1: `google-workspace`

- **Origine :** `01_Hermes_Skills_Core_Library\productivity\google-workspace\SKILL.md`
- **Rôle / Objectif :** Gmail, Calendar, Drive, Contacts, Sheets, and Docs integration for Hermes. Uses Hermes-managed OAuth2 setup, prefers the Google Workspace CLI (`gws`) when available for broader API coverage, and falls back to the Python client libraries otherwise.

## Google Workspace

Gmail, Calendar, Drive, Contacts, Sheets, and Docs — through Hermes-managed OAuth and a thin CLI wrapper. When `gws` is installed, the skill uses it as the execution backend for broader Google Workspace coverage; otherwise it falls back to the bundled Python client implementation.

### References

- `references/google-workspace_gmail-search-syntax.md` — Gmail search operators (is:unread, from:, newer_than:, etc.)

### Scripts

- `scripts/google-workspace_setup.py` — OAuth2 setup (run once to authorize)
- `scripts/google-workspace_google_api.py` — compatibility wrapper CLI. It prefers `gws` for operations when available, while preserving Hermes' existing JSON output contract.

### First-Time Setup

The setup is fully non-interactive — you drive it step by step so it works
on CLI, Telegram, Discord, or any platform.

Define a shorthand first:

```bash
GSETUP="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google-workspace_setup.py"
```

#### Step 0: Check if already set up

```bash
$GSETUP --check
```

If it prints `AUTHENTICATED`, skip to Usage — setup is already done.

#### Step 1: Triage — ask the user what they need

Before starting OAuth setup, ask the user TWO questions:

**Question 1: "What Google services do you need? Just email, or also
Calendar/Drive/Sheets/Docs?"**

- **Email only** → They don't need this skill at all. Use the `himalaya` skill
  instead — it works with a Gmail App Password (Settings → Security → App
  Passwords) and takes 2 minutes to set up. No Google Cloud project needed.
  Load the himalaya skill and follow its setup instructions.

- **Email + Calendar** → Continue with this skill, but use
  `--services email,calendar` during auth so the consent screen only asks for
  the scopes they actually need.

- **Calendar/Drive/Sheets/Docs only** → Continue with this skill and use a
  narrower `--services` set like `calendar,drive,sheets,docs`.

- **Full Workspace access** → Continue with this skill and use the default
  `all` service set.

**Question 2: "Does your Google account use Advanced Protection (hardware
security keys required to sign in)? If you're not sure, you probably don't
— it's something you would have explicitly enrolled in."**

- **No / Not sure** → Normal setup. Continue below.
- **Yes** → Their Workspace admin must add the OAuth client ID to the org's
  allowed apps list before Step 4 will work. Let them know upfront.

#### Step 2: Create OAuth credentials (one-time, ~5 minutes)

Tell the user:

> You need a Google Cloud OAuth client. This is a one-time setup:
>
> 1. Create or select a project:
>    https://console.cloud.google.com/projectselector2/home/dashboard
> 2. Enable the required APIs from the API Library:
>    https://console.cloud.google.com/apis/library
>    Enable: Gmail API, Google Calendar API, Google Drive API,
>    Google Sheets API, Google Docs API, People API
> 3. Create the OAuth client here:
>    https://console.cloud.google.com/apis/credentials
>    Credentials → Create Credentials → OAuth 2.0 Client ID
> 4. Application type: "Desktop app" → Create
> 5. If the app is still in Testing, add the user's Google account as a test user here:
>    https://console.cloud.google.com/auth/audience
>    Audience → Test users → Add users
> 6. Download the JSON file and tell me the file path
>
> Important Hermes CLI note: if the file path starts with `/`, do NOT send only the bare path as its own message in the CLI, because it can be mistaken for a slash command. Send it in a sentence instead, like:
> `The JSON file path is: /home/user/Downloads/client_secret_....json`

Once they provide the path:

```bash
$GSETUP --client-secret /path/to/client_secret.json
```

If they paste the raw client ID / client secret values instead of a file path,
write a valid Desktop OAuth JSON file for them yourself, save it somewhere
explicit (for example `~/Downloads/hermes-google-client-secret.json`), then run
`--client-secret` against that file.

#### Step 3: Get authorization URL

Use the service set chosen in Step 1. Examples:

```bash
$GSETUP --auth-url --services email,calendar --format json
$GSETUP --auth-url --services calendar,drive,sheets,docs --format json
$GSETUP --auth-url --services all --format json
```

This returns JSON with an `auth_url` field and also saves the exact URL to
`~/.hermes/google_oauth_last_url.txt`.

Agent rules for this step:
- Extract the `auth_url` field and send that exact URL to the user as a single line.
- Tell the user that the browser will likely fail on `http://localhost:1` after approval, and that this is expected.
- Tell them to copy the ENTIRE redirected URL from the browser address bar.
- If the user gets `Error 403: access_denied`, send them directly to `https://console.cloud.google.com/auth/audience` to add themselves as a test user.

#### Step 4: Exchange the code

The user will paste back either a URL like `http://localhost:1/?code=4/0A...&scope=...`
or just the code string. Either works. The `--auth-url` step stores a temporary
pending OAuth session locally so `--auth-code` can complete the PKCE exchange
later, even on headless systems:

```bash
$GSETUP --auth-code "THE_URL_OR_CODE_THE_USER_PASTED" --format json
```

If `--auth-code` fails because the code expired, was already used, or came from
an older browser tab, it now returns a fresh `fresh_auth_url`. In that case,
immediately send the new URL to the user and have them retry with the newest
browser redirect only.

#### Step 5: Verify

```bash
$GSETUP --check
```

Should print `AUTHENTICATED`. Setup is complete — token refreshes automatically from now on.

#### Notes

- Token is stored at `~/.hermes/google_token.json` and auto-refreshes.
- Pending OAuth session state/verifier are stored temporarily at `~/.hermes/google_oauth_pending.json` until exchange completes.
- If `gws` is installed, `google_api.py` points it at the same `~/.hermes/google_token.json` credentials file. Users do not need to run a separate `gws auth login` flow.
- To revoke: `$GSETUP --revoke`

### Usage

All commands go through the API script. Set `GAPI` as a shorthand:

```bash
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google-workspace_google_api.py"
```

#### Gmail

```bash
## Search (returns JSON array with id, from, subject, date, snippet)
$GAPI gmail search "is:unread" --max 10
$GAPI gmail search "from:boss@company.com newer_than:1d"
$GAPI gmail search "has:attachment filename:pdf newer_than:7d"

## Read full message (returns JSON with body text)
$GAPI gmail get MESSAGE_ID

## Send
$GAPI gmail send --to user@example.com --subject "Hello" --body "Message text"
$GAPI gmail send --to user@example.com --subject "Report" --body "<h1>Q4</h1><p>Details...</p>" --html
$GAPI gmail send --to user@example.com --subject "Hello" --from '"Research Agent" <user@example.com>' --body "Message text"

## Reply (automatically threads and sets In-Reply-To)
$GAPI gmail reply MESSAGE_ID --body "Thanks, that works for me."
$GAPI gmail reply MESSAGE_ID --from '"Support Bot" <user@example.com>' --body "Thanks"

## Labels
$GAPI gmail labels
$GAPI gmail modify MESSAGE_ID --add-labels LABEL_ID
$GAPI gmail modify MESSAGE_ID --remove-labels UNREAD
```

#### Calendar

```bash
## List events (defaults to next 7 days)
$GAPI calendar list
$GAPI calendar list --start 2026-03-01T00:00:00Z --end 2026-03-07T23:59:59Z

## Create event (ISO 8601 with timezone required)
$GAPI calendar create --summary "Team Standup" --start 2026-03-01T10:00:00-06:00 --end 2026-03-01T10:30:00-06:00
$GAPI calendar create --summary "Lunch" --start 2026-03-01T12:00:00Z --end 2026-03-01T13:00:00Z --location "Cafe"
$GAPI calendar create --summary "Review" --start 2026-03-01T14:00:00Z --end 2026-03-01T15:00:00Z --attendees "alice@co.com,bob@co.com"

## Delete event
$GAPI calendar delete EVENT_ID
```

#### Drive

```bash
$GAPI drive search "quarterly report" --max 10
$GAPI drive search "mimeType='application/pdf'" --raw-query --max 5
```

#### Contacts

```bash
$GAPI contacts list --max 20
```

#### Sheets

```bash
## Read
$GAPI sheets get SHEET_ID "Sheet1!A1:D10"

## Write
$GAPI sheets update SHEET_ID "Sheet1!A1:B2" --values '[["Name","Score"],["Alice","95"]]'

## Append rows
$GAPI sheets append SHEET_ID "Sheet1!A:C" --values '[["new","row","data"]]'
```

#### Docs

```bash
$GAPI docs get DOC_ID
```

### Output Format

All commands return JSON. Parse with `jq` or read directly. Key fields:

- **Gmail search**: `[{id, threadId, from, to, subject, date, snippet, labels}]`
- **Gmail get**: `{id, threadId, from, to, subject, date, labels, body}`
- **Gmail send/reply**: `{status: "sent", id, threadId}`
- **Calendar list**: `[{id, summary, start, end, location, description, htmlLink}]`
- **Calendar create**: `{status: "created", id, summary, htmlLink}`
- **Drive search**: `[{id, name, mimeType, modifiedTime, webViewLink}]`
- **Contacts list**: `[{name, emails: [...], phones: [...]}]`
- **Sheets get**: `[[cell, cell, ...], ...]`

### Rules

1. **Never send email or create/delete events without confirming with the user first.** Show the draft content and ask for approval.
2. **Check auth before first use** — run `setup.py --check`. If it fails, guide the user through setup.
3. **Use the Gmail search syntax reference** for complex queries — load it with `skill_view("google-workspace", file_path="references/google-workspace_gmail-search-syntax.md")`.
4. **Calendar times must include timezone** — always use ISO 8601 with offset (e.g., `2026-03-01T10:00:00-06:00`) or UTC (`Z`).
5. **Respect rate limits** — avoid rapid-fire sequential API calls. Batch reads when possible.

### Troubleshooting

| Problem | Fix |
|---------|-----|
| `NOT_AUTHENTICATED` | Run setup Steps 2-5 above |
| `REFRESH_FAILED` | Token revoked or expired — redo Steps 3-5 |
| `HttpError 403: Insufficient Permission` | Missing API scope — `$GSETUP --revoke` then redo Steps 3-5 |
| `HttpError 403: Access Not Configured` | API not enabled — user needs to enable it in Google Cloud Console |
| `ModuleNotFoundError` | Run `$GSETUP --install-deps` |
| Advanced Protection blocks auth | Workspace admin must allowlist the OAuth client ID |

### Revoking Access

```bash
$GSETUP --revoke
```


---

## Module 2: `linear`

- **Origine :** `01_Hermes_Skills_Core_Library\productivity\linear\SKILL.md`
- **Rôle / Objectif :** Manage Linear issues, projects, and teams via the GraphQL API. Create, update, search, and organize issues. Uses API key auth (no OAuth needed). All operations via curl — no dependencies.

## Linear — Issue & Project Management

Manage Linear issues, projects, and teams directly via the GraphQL API using `curl`. No MCP server, no OAuth flow, no extra dependencies.

### Setup

1. Get a personal API key from **Linear Settings > API > Personal API keys**
2. Set `LINEAR_API_KEY` in your environment (via `hermes setup` or your env config)

### API Basics

- **Endpoint:** `https://api.linear.app/graphql` (POST)
- **Auth header:** `Authorization: $LINEAR_API_KEY` (no "Bearer" prefix for API keys)
- **All requests are POST** with `Content-Type: application/json`
- **Both UUIDs and short identifiers** (e.g., `ENG-123`) work for `issue(id:)`

Base curl pattern:
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { id name } }"}' | python3 -m json.tool
```

### Workflow States

Linear uses `WorkflowState` objects with a `type` field. **6 state types:**

| Type | Description |
|------|-------------|
| `triage` | Incoming issues needing review |
| `backlog` | Acknowledged but not yet planned |
| `unstarted` | Planned/ready but not started |
| `started` | Actively being worked on |
| `completed` | Done |
| `canceled` | Won't do |

Each team has its own named states (e.g., "In Progress" is type `started`). To change an issue's status, you need the `stateId` (UUID) of the target state — query workflow states first.

**Priority values:** 0 = None, 1 = Urgent, 2 = High, 3 = Medium, 4 = Low

### Common Queries

#### Get current user
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { id name email } }"}' | python3 -m json.tool
```

#### List teams
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ teams { nodes { id name key } } }"}' | python3 -m json.tool
```

#### List workflow states for a team
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ workflowStates(filter: { team: { key: { eq: \"ENG\" } } }) { nodes { id name type } } }"}' | python3 -m json.tool
```

#### List issues (first 20)
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issues(first: 20) { nodes { identifier title priority state { name type } assignee { name } team { key } url } pageInfo { hasNextPage endCursor } } }"}' | python3 -m json.tool
```

#### List my assigned issues
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { assignedIssues(first: 25) { nodes { identifier title state { name type } priority url } } } }"}' | python3 -m json.tool
```

#### Get a single issue (by identifier like ENG-123)
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issue(id: \"ENG-123\") { id identifier title description priority state { id name type } assignee { id name } team { key } project { name } labels { nodes { name } } comments { nodes { body user { name } createdAt } } url } }"}' | python3 -m json.tool
```

#### Search issues by text
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issueSearch(query: \"bug login\", first: 10) { nodes { identifier title state { name } assignee { name } url } } }"}' | python3 -m json.tool
```

#### Filter issues by state type
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issues(filter: { state: { type: { in: [\"started\"] } } }, first: 20) { nodes { identifier title state { name } assignee { name } } } }"}' | python3 -m json.tool
```

#### Filter by team and assignee
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issues(filter: { team: { key: { eq: \"ENG\" } }, assignee: { email: { eq: \"user@example.com\" } } }, first: 20) { nodes { identifier title state { name } priority } } }"}' | python3 -m json.tool
```

#### List projects
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ projects(first: 20) { nodes { id name description progress lead { name } teams { nodes { key } } url } } }"}' | python3 -m json.tool
```

#### List team members
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { nodes { id name email active } } }"}' | python3 -m json.tool
```

#### List labels
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issueLabels { nodes { id name color } } }"}' | python3 -m json.tool
```

### Common Mutations

#### Create an issue
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { id identifier title url } } }",
    "variables": {
      "input": {
        "teamId": "TEAM_UUID",
        "title": "Fix login bug",
        "description": "Users cannot login with SSO",
        "priority": 2
      }
    }
  }' | python3 -m json.tool
```

#### Update issue status
First get the target state UUID from the workflow states query above, then:
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { stateId: \"STATE_UUID\" }) { success issue { identifier state { name type } } } }"}' | python3 -m json.tool
```

#### Assign an issue
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { assigneeId: \"USER_UUID\" }) { success issue { identifier assignee { name } } } }"}' | python3 -m json.tool
```

#### Set priority
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { priority: 1 }) { success issue { identifier priority } } }"}' | python3 -m json.tool
```

#### Add a comment
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { commentCreate(input: { issueId: \"ISSUE_UUID\", body: \"Investigated. Root cause is X.\" }) { success comment { id body } } }"}' | python3 -m json.tool
```

#### Set due date
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { dueDate: \"2026-04-01\" }) { success issue { identifier dueDate } } }"}' | python3 -m json.tool
```

#### Add labels to an issue
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { labelIds: [\"LABEL_UUID_1\", \"LABEL_UUID_2\"] }) { success issue { identifier labels { nodes { name } } } } }"}' | python3 -m json.tool
```

#### Add issue to a project
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { projectId: \"PROJECT_UUID\" }) { success issue { identifier project { name } } } }"}' | python3 -m json.tool
```

#### Create a project
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation($input: ProjectCreateInput!) { projectCreate(input: $input) { success project { id name url } } }",
    "variables": {
      "input": {
        "name": "Q2 Auth Overhaul",
        "description": "Replace legacy auth with OAuth2 and PKCE",
        "teamIds": ["TEAM_UUID"]
      }
    }
  }' | python3 -m json.tool
```

### Pagination

Linear uses Relay-style cursor pagination:

```bash
## First page
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issues(first: 20) { nodes { identifier title } pageInfo { hasNextPage endCursor } } }"}' | python3 -m json.tool

## Next page — use endCursor from previous response
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issues(first: 20, after: \"CURSOR_FROM_PREVIOUS\") { nodes { identifier title } pageInfo { hasNextPage endCursor } } }"}' | python3 -m json.tool
```

Default page size: 50. Max: 250. Always use `first: N` to limit results.

### Filtering Reference

Comparators: `eq`, `neq`, `in`, `nin`, `lt`, `lte`, `gt`, `gte`, `contains`, `startsWith`, `containsIgnoreCase`

Combine filters with `or: [...]` for OR logic (default is AND within a filter object).

### Typical Workflow

1. **Query teams** to get team IDs and keys
2. **Query workflow states** for target team to get state UUIDs
3. **List or search issues** to find what needs work
4. **Create issues** with team ID, title, description, priority
5. **Update status** by setting `stateId` to the target workflow state
6. **Add comments** to track progress
7. **Mark complete** by setting `stateId` to the team's "completed" type state

### Rate Limits

- 5,000 requests/hour per API key
- 3,000,000 complexity points/hour
- Use `first: N` to limit results and reduce complexity cost
- Monitor `X-RateLimit-Requests-Remaining` response header

### Important Notes

- Always use `terminal` tool with `curl` for API calls — do NOT use `web_extract` or `browser`
- Always check the `errors` array in GraphQL responses — HTTP 200 can still contain errors
- If `stateId` is omitted when creating issues, Linear defaults to the first backlog state
- The `description` field supports Markdown
- Use `python3 -m json.tool` or `jq` to format JSON responses for readability


---

## Module 3: `nano-pdf`

- **Origine :** `01_Hermes_Skills_Core_Library\productivity\nano-pdf\SKILL.md`
- **Rôle / Objectif :** Edit PDFs with natural-language instructions using the nano-pdf CLI. Modify text, fix typos, update titles, and make content changes to specific pages without manual editing.

## nano-pdf

Edit PDFs using natural-language instructions. Point it at a page and describe what to change.

### Prerequisites

```bash
## Install with uv (recommended — already available in Hermes)
uv pip install nano-pdf

## Or with pip
pip install nano-pdf
```

### Usage

```bash
nano-pdf edit <file.pdf> <page_number> "<instruction>"
```

### Examples

```bash
## Change a title on page 1
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"

## Update a date on a specific page
nano-pdf edit report.pdf 3 "Update the date from January to February 2026"

## Fix content
nano-pdf edit contract.pdf 2 "Change the client name from 'Acme Corp' to 'Acme Industries'"
```

### Notes

- Page numbers may be 0-based or 1-based depending on version — if the edit hits the wrong page, retry with ±1
- Always verify the output PDF after editing (use `read_file` to check file size, or open it)
- The tool uses an LLM under the hood — requires an API key (check `nano-pdf --help` for config)
- Works well for text changes; complex layout modifications may need a different approach


---

## Module 4: `notion`

- **Origine :** `01_Hermes_Skills_Core_Library\productivity\notion\SKILL.md`
- **Rôle / Objectif :** Notion API for creating and managing pages, databases, and blocks via curl. Search, create, update, and query Notion workspaces directly from the terminal.

## Notion API

Use the Notion API via curl to create, read, update pages, databases (data sources), and blocks. No extra tools needed — just curl and a Notion API key.

### Prerequisites

1. Create an integration at https://notion.so/my-integrations
2. Copy the API key (starts with `ntn_` or `secret_`)
3. Store it in `~/.hermes/.env`:
   ```
   NOTION_API_KEY=ntn_your_key_here
   ```
4. **Important:** Share target pages/databases with your integration in Notion (click "..." → "Connect to" → your integration name)

### API Basics

All requests use this pattern:

```bash
curl -s -X GET "https://api.notion.com/v1/..." \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json"
```

The `Notion-Version` header is required. This skill uses `2025-09-03` (latest). In this version, databases are called "data sources" in the API.

### Common Operations

#### Search

```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "page title"}'
```

#### Get Page

```bash
curl -s "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

#### Get Page Content (blocks)

```bash
curl -s "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

#### Create Page in a Database

```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "xxx"},
    "properties": {
      "Name": {"title": [{"text": {"content": "New Item"}}]},
      "Status": {"select": {"name": "Todo"}}
    }
  }'
```

#### Query a Database

```bash
curl -s -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "select": {"equals": "Active"}},
    "sorts": [{"property": "Date", "direction": "descending"}]
  }'
```

#### Create a Database

```bash
curl -s -X POST "https://api.notion.com/v1/data_sources" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "xxx"},
    "title": [{"text": {"content": "My Database"}}],
    "properties": {
      "Name": {"title": {}},
      "Status": {"select": {"options": [{"name": "Todo"}, {"name": "Done"}]}},
      "Date": {"date": {}}
    }
  }'
```

#### Update Page Properties

```bash
curl -s -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Status": {"select": {"name": "Done"}}}}'
```

#### Add Content to a Page

```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Hello from Hermes!"}}]}}
    ]
  }'
```

### Property Types

Common property formats for database items:

- **Title:** `{"title": [{"text": {"content": "..."}}]}`
- **Rich text:** `{"rich_text": [{"text": {"content": "..."}}]}`
- **Select:** `{"select": {"name": "Option"}}`
- **Multi-select:** `{"multi_select": [{"name": "A"}, {"name": "B"}]}`
- **Date:** `{"date": {"start": "2026-01-15", "end": "2026-01-16"}}`
- **Checkbox:** `{"checkbox": true}`
- **Number:** `{"number": 42}`
- **URL:** `{"url": "https://..."}`
- **Email:** `{"email": "user@example.com"}`
- **Relation:** `{"relation": [{"id": "page_id"}]}`

### Key Differences in API Version 2025-09-03

- **Databases → Data Sources:** Use `/data_sources/` endpoints for queries and retrieval
- **Two IDs:** Each database has both a `database_id` and a `data_source_id`
  - Use `database_id` when creating pages (`parent: {"database_id": "..."}`)
  - Use `data_source_id` when querying (`POST /v1/data_sources/{id}/query`)
- **Search results:** Databases return as `"object": "data_source"` with their `data_source_id`

### Notes

- Page/database IDs are UUIDs (with or without dashes)
- Rate limit: ~3 requests/second average
- The API cannot set database view filters — that's UI-only
- Use `is_inline: true` when creating data sources to embed them in pages
- Add `-s` flag to curl to suppress progress bars (cleaner output for Hermes)
- Pipe output through `jq` for readable JSON: `... | jq '.results[0].properties'`


---

## Module 5: `ocr-and-documents`

- **Origine :** `01_Hermes_Skills_Core_Library\productivity\ocr-and-documents\SKILL.md`
- **Rôle / Objectif :** Extract text from PDFs and scanned documents. Use web_extract for remote URLs, pymupdf for local text-based PDFs, marker-pdf for OCR/scanned docs. For DOCX use python-docx, for PPTX see the powerpoint skill.

## PDF & Document Extraction

For DOCX: use `python-docx` (parses actual document structure, far better than OCR).
For PPTX: see the `powerpoint` skill (uses `python-pptx` with full slide/notes support).
This skill covers **PDFs and scanned documents**.

### Step 1: Remote URL Available?

If the document has a URL, **always try `web_extract` first**:

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.

Only use local extraction when: the file is local, web_extract fails, or you need batch processing.

### Step 2: Choose Local Extractor

| Feature | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|-----------------|---------------------|
| **Text-based PDF** | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ✅ (90+ languages) |
| **Tables** | ✅ (basic) | ✅ (high accuracy) |
| **Equations / LaTeX** | ❌ | ✅ |
| **Code blocks** | ❌ | ✅ |
| **Forms** | ❌ | ✅ |
| **Headers/footers removal** | ❌ | ✅ |
| **Reading order detection** | ❌ | ✅ |
| **Images extraction** | ✅ (embedded) | ✅ (with context) |
| **Images → text (OCR)** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown output** | ✅ (via pymupdf4llm) | ✅ (native, higher quality) |
| **Install size** | ~25MB | ~3-5GB (PyTorch + models) |
| **Speed** | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) |

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout analysis.

If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for PyTorch and models. Your system has [X]GB free. Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf which works for text-based PDFs but not scanned documents or equations."

---

### pymupdf (lightweight)

```bash
pip install pymupdf pymupdf4llm
```

**Via helper script**:
```bash
python scripts/ocr-and-documents_extract_pymupdf.py document.pdf              # Plain text
python scripts/ocr-and-documents_extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/ocr-and-documents_extract_pymupdf.py document.pdf --tables      # Tables
python scripts/ocr-and-documents_extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/ocr-and-documents_extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/ocr-and-documents_extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline**:
```bash
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

---

### marker-pdf (high-quality OCR)

```bash
## Check disk space first
python scripts/ocr-and-documents_extract_marker.py --check

pip install marker-pdf
```

**Via helper script**:
```bash
python scripts/ocr-and-documents_extract_marker.py document.pdf                # Markdown
python scripts/ocr-and-documents_extract_marker.py document.pdf --json         # JSON with metadata
python scripts/ocr-and-documents_extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/ocr-and-documents_extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/ocr-and-documents_extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI** (installed with marker-pdf):
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

---

### Arxiv Papers

```
## Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

## Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

## Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

### Split, Merge & Search

pymupdf handles these natively — use `execute_code` or inline Python:

```python
## Split: extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
## Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
## Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.

---

### Notes

- `web_extract` is always first choice for URLs
- pymupdf is the safe default — instant, no models, works everywhere
- marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when needed
- Both helper scripts accept `--help` for full usage
- marker-pdf downloads ~2.5GB of models to `~/.cache/huggingface/` on first use
- For Word docs: `pip install python-docx` (better than OCR — parses actual structure)
- For PowerPoint: see the `powerpoint` skill (uses python-pptx)


---

## Module 6: `powerpoint`

- **Origine :** `01_Hermes_Skills_Core_Library\productivity\powerpoint\SKILL.md`
- **Rôle / Objectif :** Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.

## Powerpoint Skill

### Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | Read [editing.md](editing.md) |
| Create from scratch | Read [pptxgenjs.md](pptxgenjs.md) |

---

### Reading Content

```bash
## Text extraction
python -m markitdown presentation.pptx

## Visual overview
python scripts/thumbnail.py presentation.pptx

## Raw XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

### Editing Workflow

**Read [editing.md](editing.md) for full details.**

1. Analyze template with `thumbnail.py`
2. Unpack → manipulate slides → edit content → clean → pack

---

### Creating from Scratch

**Read [pptxgenjs.md](pptxgenjs.md) for full details.**

Use when no template or reference presentation is available.

---

### Design Ideas

**Don't create boring slides.** Plain bullets on a white background won't impress anyone. Consider ideas from this list for each slide.

#### Before Starting

- **Pick a bold, content-informed color palette**: The palette should feel designed for THIS topic. If swapping your colors into a completely different presentation would still "work," you haven't made specific enough choices.
- **Dominance over equality**: One color should dominate (60-70% visual weight), with 1-2 supporting tones and one sharp accent. Never give all colors equal weight.
- **Dark/light contrast**: Dark backgrounds for title + conclusion slides, light for content ("sandwich" structure). Or commit to dark throughout for a premium feel.
- **Commit to a visual motif**: Pick ONE distinctive element and repeat it — rounded image frames, icons in colored circles, thick single-side borders. Carry it across every slide.

#### Color Palettes

Choose colors that match your topic — don't default to generic blue. Use these palettes as inspiration:

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| **Midnight Executive** | `1E2761` (navy) | `CADCFC` (ice blue) | `FFFFFF` (white) |
| **Forest & Moss** | `2C5F2D` (forest) | `97BC62` (moss) | `F5F5F5` (cream) |
| **Coral Energy** | `F96167` (coral) | `F9E795` (gold) | `2F3C7E` (navy) |
| **Warm Terracotta** | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) |
| **Ocean Gradient** | `065A82` (deep blue) | `1C7293` (teal) | `21295C` (midnight) |
| **Charcoal Minimal** | `36454F` (charcoal) | `F2F2F2` (off-white) | `212121` (black) |
| **Teal Trust** | `028090` (teal) | `00A896` (seafoam) | `02C39A` (mint) |
| **Berry & Cream** | `6D2E46` (berry) | `A26769` (dusty rose) | `ECE2D0` (cream) |
| **Sage Calm** | `84B59F` (sage) | `69A297` (eucalyptus) | `50808E` (slate) |
| **Cherry Bold** | `990011` (cherry) | `FCF6F5` (off-white) | `2F3C7E` (navy) |

#### For Each Slide

**Every slide needs a visual element** — image, chart, icon, or shape. Text-only slides are forgettable.

**Layout options:**
- Two-column (text left, illustration on right)
- Icon + text rows (icon in colored circle, bold header, description below)
- 2x2 or 2x3 grid (image on one side, grid of content blocks on other)
- Half-bleed image (full left or right side) with content overlay

**Data display:**
- Large stat callouts (big numbers 60-72pt with small labels below)
- Comparison columns (before/after, pros/cons, side-by-side options)
- Timeline or process flow (numbered steps, arrows)

**Visual polish:**
- Icons in small colored circles next to section headers
- Italic accent text for key stats or taglines

#### Typography

**Choose an interesting font pairing** — don't default to Arial. Pick a header font with personality and pair it with a clean body font.

| Header Font | Body Font |
|-------------|-----------|
| Georgia | Calibri |
| Arial Black | Arial |
| Calibri | Calibri Light |
| Cambria | Calibri |
| Trebuchet MS | Calibri |
| Impact | Arial |
| Palatino | Garamond |
| Consolas | Calibri |

| Element | Size |
|---------|------|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body text | 14-16pt |
| Captions | 10-12pt muted |

#### Spacing

- 0.5" minimum margins
- 0.3-0.5" between content blocks
- Leave breathing room—don't fill every inch

#### Avoid (Common Mistakes)

- **Don't repeat the same layout** — vary columns, cards, and callouts across slides
- **Don't center body text** — left-align paragraphs and lists; center only titles
- **Don't skimp on size contrast** — titles need 36pt+ to stand out from 14-16pt body
- **Don't default to blue** — pick colors that reflect the specific topic
- **Don't mix spacing randomly** — choose 0.3" or 0.5" gaps and use consistently
- **Don't style one slide and leave the rest plain** — commit fully or keep it simple throughout
- **Don't create text-only slides** — add images, icons, charts, or visual elements; avoid plain title + bullets
- **Don't forget text box padding** — when aligning lines or shapes with text edges, set `margin: 0` on the text box or offset the shape to account for padding
- **Don't use low-contrast elements** — icons AND text need strong contrast against the background; avoid light text on light backgrounds or dark text on dark backgrounds
- **NEVER use accent lines under titles** — these are a hallmark of AI-generated slides; use whitespace or background color instead

---

### QA (Required)

**Assume there are problems. Your job is to find them.**

Your first render is almost never correct. Approach QA as a bug hunt, not a confirmation step. If you found zero issues on first inspection, you weren't looking hard enough.

#### Content QA

```bash
python -m markitdown output.pptx
```

Check for missing content, typos, wrong order.

**When using templates, check for leftover placeholder text:**

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

If grep returns results, fix them before declaring success.

#### Visual QA

**⚠️ USE SUBAGENTS** — even for 2-3 slides. You've been staring at the code and will see what you expect, not what's there. Subagents have fresh eyes.

Convert slides to images (see [Converting to Images](#converting-to-images)), then use this prompt:

```
Visually inspect these slides. Assume there are issues — find them.

Look for:
- Overlapping elements (text through shapes, lines through words, stacked elements)
- Text overflow or cut off at edges/box boundaries
- Decorative lines positioned for single-line text but title wrapped to two lines
- Source citations or footers colliding with content above
- Elements too close (< 0.3" gaps) or cards/sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (e.g., light gray text on cream-colored background)
- Low-contrast icons (e.g., dark icons on dark backgrounds without a contrasting circle)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

For each slide, list issues or areas of concern, even if minor.

Read and analyze these images:
1. /path/to/slide-01.jpg (Expected: [brief description])
2. /path/to/slide-02.jpg (Expected: [brief description])

Report ALL issues found, including minor ones.
```

#### Verification Loop

1. Generate slides → Convert to images → Inspect
2. **List issues found** (if none found, look again more critically)
3. Fix issues
4. **Re-verify affected slides** — one fix often creates another problem
5. Repeat until a full pass reveals no new issues

**Do not declare success until you've completed at least one fix-and-verify cycle.**

---

### Converting to Images

Convert presentations to individual slide images for visual inspection:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

This creates `slide-01.jpg`, `slide-02.jpg`, etc.

To re-render specific slides after fixes:

```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

---

### Dependencies

- `pip install "markitdown[pptx]"` - text extraction
- `pip install Pillow` - thumbnail grids
- `npm install -g pptxgenjs` - creating from scratch
- LibreOffice (`soffice`) - PDF conversion (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- Poppler (`pdftoppm`) - PDF to images


---
