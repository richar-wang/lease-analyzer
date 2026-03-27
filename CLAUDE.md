# Ontario Tenant Lease Analyzer

## What It Does

A web app that analyzes Ontario residential lease PDFs against the Residential Tenancies Act (RTA) and the Ontario Standard Lease (Form 2229E). Users upload a PDF lease, Claude AI reads it and flags illegal, suspect, or notable clauses with plain-language explanations and RTA references.

## Architecture

```
frontend/          React 19 + TypeScript + Tailwind CSS 4 + Vite 8
backend/           Python FastAPI + Anthropic SDK
  config.py        Pydantic settings (env vars: ANTHROPIC_API_KEY, ACCESS_CODE, etc.)
  main.py          FastAPI app, CORS, static file serving
  middleware.py     Access code validation (X-Access-Code header)
  routers/
    analyze.py     POST /api/analyze (PDF upload), GET /api/demo, GET /api/config, GET /api/health, GET /api/languages
  schemas/
    analysis.py    Pydantic models: AnalysisResponse, FlaggedClause, Severity (red/yellow/green)
  services/
    lease_analyzer.py   Claude API calls using tool_use for structured output
    pdf_extractor.py    PyMuPDF: text extraction + form field extraction + image rendering for scanned PDFs
  rta/
    sections.py         Verbatim RTA statutory text (s.105-106, s.14, s.20-26, s.25-27, s.116-120, s.95-98, s.37/48/77/83, s.22-23, s.20/89, s.108)
    standard_lease.py   Ontario Standard Lease (Form 2229E) key provisions
    prompt_builder.py   Builds system/user prompts, defines SUPPORTED_LANGUAGES (en, he)
scripts/
  generate_demo_lease.py   Generates a sample PDF with deliberately illegal clauses for testing
Dockerfile              Multi-stage: Node build frontend → Python serve everything
```

## How It Works

1. User uploads a PDF lease (or clicks "Try Demo Lease")
2. Backend extracts text via PyMuPDF (including fillable form fields); falls back to rendering pages as images for scanned PDFs
3. Backend sends lease text + RTA/Standard Lease reference to Claude (claude-sonnet-4-6) using tool_use to get structured JSON
4. Results stream back to frontend via SSE (Server-Sent Events) with step progress
5. Frontend displays results in Card View (clause cards sorted by severity) or Document View (inline highlighting in full lease text)

## Tech Stack

**Backend:**
- Python 3.13, FastAPI 0.115, Uvicorn
- anthropic SDK 0.52 (Claude claude-sonnet-4-6, tool_use for structured output)
- PyMuPDF 1.25 for PDF text extraction and image rendering
- Pydantic 2.11 + pydantic-settings for config

**Frontend:**
- React 19, TypeScript 5.9, Vite 8
- Tailwind CSS 4 (via @tailwindcss/vite plugin)
- No router, no state management library — single-page app with useState

## Key Design Decisions

- **Per-request cost cap** (`max_cost_per_request`, default $0.25): estimates input tokens and limits output tokens to stay within budget. No rate limiter.
- **Structured output via tool_use**: Claude is forced to call `report_lease_analysis` tool, returning typed `FlaggedClause[]` + `summary`.
- **SSE streaming**: analysis endpoint streams status updates (`extracting` → `rendering` → `analyzing` → `complete`) then the final result. Custom `parseSSE` on frontend handles the stream.
- **Access code protection**: optional trivia-style access code (set via `ACCESS_CODE` + `ACCESS_HINT` env vars). Stored in sessionStorage, sent via `X-Access-Code` header.
- **Hebrew mode**: toggles RTL layout, IDF blue theme (#0038A8), and instructs Claude to write analysis in Hebrew while keeping clause quotes in original language.
- **Document View**: highlights flagged clauses inline in the full lease text using whitespace-normalized string matching. Click to expand details.
- **Vision fallback**: if text extraction yields <50 chars, renders PDF pages as images and uses Claude vision.

## Running Locally

```bash
# Backend
cd backend
python -m venv .venv && source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
cp ../.env.example .env  # Add your ANTHROPIC_API_KEY
uvicorn main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev   # Vite dev server on :5173, proxies /api to :8000
```

## Docker

```bash
docker build -t lease-analyzer .
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=sk-ant-... lease-analyzer
```

The Dockerfile builds frontend → copies dist into backend's `static/` → serves everything from FastAPI on port 8000.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Yes | — | Claude API key |
| `CLAUDE_MODEL` | No | `claude-sonnet-4-6` | Model to use |
| `CLAUDE_MAX_TOKENS` | No | `8192` | Max output tokens |
| `MAX_FILE_SIZE_BYTES` | No | `10485760` (10MB) | Upload size limit |
| `MAX_COST_PER_REQUEST` | No | `0.25` | Cost cap in USD |
| `ACCESS_CODE` | No | — | If set, requires this code to use the app |
| `ACCESS_HINT` | No | — | Hint/question shown on access code screen |

## Current State (as of last commit 15ff3f5)

**Working:**
- PDF upload and text extraction (including form fields and scanned PDF vision fallback)
- Claude analysis with structured output (flagged clauses, severity, RTA references, standard lease comparison)
- SSE progress streaming
- Card View and Document View with inline highlighting
- English and Hebrew language support with RTL layout and themed UI
- Access code protection
- Demo lease with deliberately illegal clauses
- Docker deployment
- Frontend production build (dist/ exists)

**No known bugs or incomplete features at this point.** The codebase is clean and the git status is clean.

## Commit History (oldest → newest)

1. Initial commit: full working app
2. SSE progress updates + Claude vision fallback for scanned PDFs
3. Document View with inline clause highlighting
4. Access code protection + per-IP rate limiting
5. Trivia-style access code with hint question
6. Standard Lease comparison + SSE parsing fix
7. Redesigned Document View, replaced rate limiter with per-request cost cap
8. Multi-language support (14 languages)
9. Restricted to English and Hebrew only
10. Hebrew mode with IDF blue theme, renamed "Problematic" to "Suspect"
