# MarkTeach Workbench Design

Date: 2026-03-12
Status: Approved

## Goal
Build a local workbench that converts Markdown notes into teaching-focused HTML pages with live preview, AI restructuring, theming, and ZIP export.

## Scope (MVP)
- Frontend: React + Vite workbench with editor, settings, and live preview.
- Backend: FastAPI orchestration for model calls, AST-based rendering, and export.
- Providers: OpenAI and DeepSeek.
- BYOK: both browser-local encrypted storage and backend encrypted local storage.

## Architecture
- `frontend/`: React + Vite + Tailwind UI.
- `backend/`: FastAPI app with orchestration and render pipelines.
- `docs/plans/`: design and implementation plans.
- Local runtime: browser app + local API server.

### Module Boundaries
1. Settings & Auth
- Manage provider credentials and active model.
- Encrypt/decrypt credentials locally.
- Never return plaintext API key from backend.

2. Editor & Preview
- Left: Markdown editor.
- Right: live teaching-page preview.
- Support TOC and code highlighting in preview.

3. AI Orchestration
- Markdown chunking and prompt injection.
- Async model communication with retries.
- Merge and validate required teaching structure:
  - Intro
  - Core Concepts
  - Case Analysis
  - Summary

4. Templating & Render
- Parse Markdown AST via remark.
- Transform/rewrite nodes via rehype pipeline.
- Generate TOC and component slots (sidebar/progress/QA area).
- Sanitize final HTML to prevent XSS.

5. Export
- Package HTML + CSS + JS + assets into ZIP.
- Provide download endpoint and artifact metadata.

## Data Model
- `WorkspaceConfig`: active provider/model, theme, preview options.
- `ProviderCredential`: provider, encrypted key, base URL (optional), updatedAt.
- `TransformJob`: source markdown, prompt profile, status, result, error.
- `ExportArtifact`: output html path, asset manifest, zip path, timestamp.

## Security Model
- Frontend encryption: WebCrypto AES-GCM with key derived from user master password (PBKDF2).
- Backend encryption: AES-GCM for credential files under backend data directory.
- Plaintext API keys are in-memory only during request execution.
- Logs contain trace IDs and status only (no sensitive values).

## Processing Flow
1. User edits Markdown.
2. Frontend requests local preview render.
3. User triggers AI rewrite.
4. Backend chunks markdown, calls selected provider, retries failed chunks.
5. Backend merges output, verifies structure, performs one repair pass if needed.
6. Backend renders sanitized HTML into selected template.
7. User exports ZIP artifact.

## API Contract (MVP)
- `POST /api/settings/credentials`
- `POST /api/settings/activate-model`
- `POST /api/transform/preview`
- `POST /api/transform/ai-rewrite`
- `GET /api/transform/jobs/{job_id}`
- `POST /api/export/zip`
- `GET /api/export/download/{artifact_id}`

## Milestones
- M1: scaffold and local run.
- M2: editor + preview pipeline.
- M3: BYOK and provider switching.
- M4: AI rewrite orchestration.
- M5: template skins and ZIP export.

## Test Strategy
- Backend: pytest for APIs, encryption, orchestration, export.
- Frontend: Vitest + Testing Library for editor/settings/preview behavior.
- E2E: Playwright for full user flow.
- Security tests: XSS sanitization and no-secret logging.
