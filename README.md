# Trexovia Assistant

> A private, proactive AI chief of staff that turns conversations, documents, email, and calendar context into dependable next actions.

Trexovia Assistant helps you stay ahead of the work that matters: it remembers
what you have decided, grounds answers in your documents, prepares you for
meetings, and surfaces opportunities before they become missed follow-ups. It
can read connected services to build context, but it never performs an external
write without showing you exactly what will happen and receiving your approval.

## What it does

- **Talk naturally.** Have a continuous conversation with an LLM that retains
  useful short-term context.
- **Remember deliberately.** Store durable preferences, commitments, people,
  and project context with controls to review, edit, pin, or forget it.
- **Answer from your knowledge.** Upload documents and receive grounded answers
  with source citations instead of unsupported claims.
- **Work across your day.** Search Gmail, inspect Calendar availability, triage
  inboxes, draft replies, and prepare meeting briefs.
- **Act safely.** Every side-effecting action—sending email, creating an event,
  or changing access—pauses for an approval that names the target, effect, and
  parameters.
- **Bring in specialists.** Route work to focused research, communication,
  planning, and operations agents while retaining a single, clear audit trail.
- **Be helpfully proactive.** Detect stale conversations, upcoming meetings,
  open commitments, and timely follow-ups without turning notifications into
  noise.

## Product tour

| Ask Trexovia | What happens |
| --- | --- |
| “What did we decide about the Atlas launch?” | Retrieves relevant long-term memories and connected documents, then cites the supporting sources. |
| “Prepare me for my 2 PM with Maya.” | Builds a concise brief from the calendar event, recent email, previous notes, and open commitments. |
| “Triage today’s urgent email.” | Classifies messages, identifies decisions and follow-ups, and proposes drafts or tasks. |
| “Find a 30-minute slot with the design team.” | Reads availability and presents options; creating an event requires approval. |
| “Send the summary to Maya.” | Creates an immutable approval preview. Nothing is sent until you approve it. |

## How it works

```mermaid
flowchart LR
    U[You] --> C[Conversation & specialist agents]
    C --> M[Short-term + long-term memory]
    C --> R[Document RAG]
    C --> T[Gmail & Calendar tools]
    M --> C
    R --> C
    T --> P{External action?}
    P -->|Read| C
    P -->|Write| A[Approval preview]
    A -->|Approved| X[Execute + verify]
    A -->|Rejected / expired| C
    X --> L[Audit log, metrics & evaluation data]
```

Trexovia keeps orchestration, policy enforcement, tool access, and user data
boundaries outside the model. The model can propose a plan; deterministic
services validate permissions, require approval where needed, execute the
action idempotently, and verify the outcome before reporting success.

## Core capabilities

### Memory that stays useful

Trexovia maintains two complementary layers of context:

- **Conversation memory** keeps the active discussion coherent without flooding
  the model with old turns.
- **Long-term memory** stores explicit facts, preferences, decisions,
  commitments, and project context. Each recalled item includes why it was used,
  and you can correct or remove it at any time.

### Grounded document intelligence

Documents are chunked, indexed, and retrieved within the current workspace.
Retrieved material is treated as untrusted reference content—not as
instructions—and answers retain document and page-level provenance.

### Gmail and Google Calendar

With a connected Google account, Trexovia can:

- find and summarize relevant threads;
- triage messages into urgency and follow-up categories;
- draft, but never silently send, replies;
- inspect events and availability; and
- assemble meeting preparation briefs with linked evidence.

OAuth tokens are scoped to the minimum permissions required, encrypted at rest,
and never exposed to the model prompt or browser client.

### Agents and workflows

Specialist agents handle focused tasks such as research, inbox triage, meeting
prep, and communications. A workflow records its plan, status, tools,
approvals, outputs, and verification receipt so you can resume work or inspect
what happened later.

## Safety and privacy

Trexovia is designed to make assistant automation inspectable and reversible.

- Read-only tools and write tools have separate permissions.
- Write actions require an approval bound to the exact actor, target,
  parameters, risk, and expiry. Material changes invalidate the approval.
- Executions use idempotency keys and verify the provider’s authoritative state
  before reporting completion.
- Every user, workspace, memory, document, tool invocation, and audit event is
  isolated by tenant identity.
- Sensitive credentials remain server-side; secrets are never placed in model
  context, client bundles, logs, or source control.
- Retrieval is provenance-aware and resistant to instruction injection from
  uploaded or connected content.

Report suspected vulnerabilities privately to the project maintainers; never
include credentials, private documents, or user data in a public issue.

## Quick start

### Prerequisites

- Python 3.11+
- An OpenAI API key (or a compatible model-provider endpoint)
- Docker and Docker Compose for the full local stack

### Run locally

```bash
git clone https://github.com/brainox/trexovia-assistant.git
cd trexovia-assistant

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

touch .env
# Add OPENAI_API_KEY and select OPENAI_MODEL in .env
python app.py
```

The assistant stores local development data in `data/`. Add `data/` and
`.env` to your personal ignore rules and never commit either file.

### Run the full stack

```bash
docker compose up --build
```

Open `http://localhost:3000` for the web app. The API is available at
`http://localhost:8000`; its health endpoint reports database, queue, and
model-provider readiness.

## Configuration

Create `.env` (or copy `.env.example` when included in a release) and set the
values appropriate to your environment. At minimum, configure:

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-5
DATABASE_URL=postgresql://trexovia:trexovia@localhost:5432/trexovia
REDIS_URL=redis://localhost:6379/0
APP_ENCRYPTION_KEY=replace_with_a_32_byte_secret
```

For Gmail and Calendar, create Google OAuth credentials and add the redirect
URL shown by the Integrations screen. Keep OAuth client secrets and encryption
keys in your deployment’s secret manager—not in `.env` files shared with a
team.

## Testing and quality

```bash
pytest
ruff check .
ruff format --check .
```

The CI pipeline runs unit and integration tests, type and lint checks,
dependency/security scanning, and evaluation suites for retrieval quality,
approval enforcement, tool reliability, and regression-prone user journeys.

## Deployment

Trexovia is containerized for cloud deployment. A production environment needs:

- managed PostgreSQL with vector search and backups;
- Redis-backed worker queues for durable workflows;
- object storage for document originals;
- a secrets manager for model and OAuth credentials;
- a public HTTPS callback URL for Google OAuth; and
- centralized logs, metrics, traces, alerts, and evaluation reporting.

Run database migrations before deploying a new version. Workers use leases and
idempotency keys so retries do not duplicate an approved external action.

## Repository guide

```text
app/             API, orchestration, tools, agents, and policy services
web/             Web application
workers/         Durable workflow and ingestion workers
tests/           Unit, integration, and end-to-end tests
infra/           Containers, deployment, and infrastructure configuration
docs/            Architecture, connector, and operational documentation
```

## Status

Trexovia Assistant is production-ready for personal and workspace use. The
project continues to evolve daily; the public API, connector scopes, and agent
skills follow semantic versioning and are documented with migration notes.

## Contributing

Contributions are welcome. Please open an issue before undertaking a large
change, keep pull requests focused, add tests for behavior changes, and avoid
including real user data, credentials, or provider responses in commits.

## License

Add the project license here (for example, MIT or Apache-2.0) before accepting
external contributions.
