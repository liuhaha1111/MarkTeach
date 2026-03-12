# MarkTeach Workbench MVP Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a local React + FastAPI workbench that transforms Markdown notes into teaching-style HTML pages with live preview, AI restructuring, and ZIP export.

**Architecture:** The frontend handles editing, local interaction, and preview orchestration, while FastAPI provides secure BYOK storage, provider routing, AI rewrite orchestration, template render, and artifact export. Backend remains the trust boundary for model credentials and model calls.

**Tech Stack:** React, Vite, TypeScript, Tailwind CSS, FastAPI, Pydantic, pytest, Vitest, Testing Library, Playwright, markdown-it, Prism.js, DOMPurify, Python zipfile.

---

Use @test-driven-development for every behavior change and @verification-before-completion before any completion claim.

### Task 1: Bootstrap Monorepo and Runtime Skeleton

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/App.tsx`
- Create: `backend/requirements.txt`
- Create: `backend/app/main.py`
- Create: `backend/tests/test_health.py`
- Create: `Makefile`

**Step 1: Write the failing test**

```python
from fastapi.testclient import TestClient
from app.main import app


def test_health_returns_ok():
    client = TestClient(app)
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json() == {'ok': True}
```

**Step 2: Run test to verify it fails**

Run: `cd backend && pytest tests/test_health.py -v`
Expected: FAIL with import or missing route error.

**Step 3: Write minimal implementation**

```python
from fastapi import FastAPI

app = FastAPI()


@app.get('/api/health')
def health():
    return {'ok': True}
```

**Step 4: Run test to verify it passes**

Run: `cd backend && pytest tests/test_health.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add backend/tests/test_health.py backend/app/main.py backend/requirements.txt frontend/package.json frontend/vite.config.ts frontend/src/main.tsx frontend/src/App.tsx Makefile
git commit -m "chore: scaffold frontend and backend runtimes"
```

### Task 2: Implement Backend Credential Encryption Core

**Files:**
- Create: `backend/app/security/crypto.py`
- Create: `backend/app/security/models.py`
- Create: `backend/tests/test_crypto.py`

**Step 1: Write the failing test**

```python
from app.security.crypto import encrypt_secret, decrypt_secret


def test_encrypt_roundtrip():
    payload = encrypt_secret('sk-123', 'master-pass')
    assert decrypt_secret(payload, 'master-pass') == 'sk-123'


def test_decrypt_fails_with_wrong_password():
    payload = encrypt_secret('sk-123', 'master-pass')
    try:
        decrypt_secret(payload, 'wrong-pass')
        assert False, 'expected decrypt to fail'
    except ValueError:
        assert True
```

**Step 2: Run test to verify it fails**

Run: `cd backend && pytest tests/test_crypto.py -v`
Expected: FAIL because module/functions do not exist.

**Step 3: Write minimal implementation**

```python
# app/security/crypto.py
# Use PBKDF2-HMAC-SHA256 + AES-GCM

def encrypt_secret(secret: str, password: str) -> dict:
    ...


def decrypt_secret(payload: dict, password: str) -> str:
    ...
```

**Step 4: Run test to verify it passes**

Run: `cd backend && pytest tests/test_crypto.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add backend/app/security/crypto.py backend/app/security/models.py backend/tests/test_crypto.py
git commit -m "feat: add credential encryption primitives"
```

### Task 3: Build Settings & Auth API (BYOK + Active Model)

**Files:**
- Create: `backend/app/api/settings.py`
- Create: `backend/app/services/settings_store.py`
- Modify: `backend/app/main.py`
- Create: `backend/tests/test_settings_api.py`
- Create: `backend/data/.gitkeep`

**Step 1: Write the failing test**

```python
from fastapi.testclient import TestClient
from app.main import app


def test_save_credentials_masks_key():
    client = TestClient(app)
    res = client.post('/api/settings/credentials', json={
        'provider': 'openai',
        'apiKey': 'sk-test-123456',
        'masterPassword': 'pass1234'
    })
    assert res.status_code == 200
    body = res.json()
    assert body['ok'] is True
    assert body['maskedKey'].startswith('sk-')
    assert 'apiKey' not in str(body)


def test_activate_model_persists_selection():
    client = TestClient(app)
    res = client.post('/api/settings/activate-model', json={
        'provider': 'deepseek',
        'model': 'deepseek-chat'
    })
    assert res.status_code == 200
    assert res.json()['activeProvider'] == 'deepseek'
```

**Step 2: Run test to verify it fails**

Run: `cd backend && pytest tests/test_settings_api.py -v`
Expected: FAIL with 404 endpoints.

**Step 3: Write minimal implementation**

```python
# app/api/settings.py
@router.post('/credentials')
def save_credentials(...):
    ...

@router.post('/activate-model')
def activate_model(...):
    ...
```

**Step 4: Run test to verify it passes**

Run: `cd backend && pytest tests/test_settings_api.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add backend/app/api/settings.py backend/app/services/settings_store.py backend/app/main.py backend/tests/test_settings_api.py backend/data/.gitkeep
git commit -m "feat: add settings and byok endpoints"
```

### Task 4: Implement Markdown Preview Render API

**Files:**
- Create: `backend/app/api/transform.py`
- Create: `backend/app/services/renderer.py`
- Create: `backend/tests/test_preview_api.py`
- Modify: `backend/app/main.py`

**Step 1: Write the failing test**

```python
from fastapi.testclient import TestClient
from app.main import app


def test_preview_generates_html_and_toc():
    client = TestClient(app)
    markdown = '# Title\n\n## Part\n\n```python\nprint(1)\n```'
    res = client.post('/api/transform/preview', json={
        'rawMarkdown': markdown,
        'themeId': 'classic',
        'previewOptions': {'toc': True}
    })
    assert res.status_code == 200
    body = res.json()
    assert '<h1' in body['html']
    assert len(body['toc']) == 2


def test_preview_sanitizes_xss():
    client = TestClient(app)
    res = client.post('/api/transform/preview', json={
        'rawMarkdown': '<script>alert(1)</script>',
        'themeId': 'classic',
        'previewOptions': {}
    })
    assert '<script' not in res.json()['html']
```

**Step 2: Run test to verify it fails**

Run: `cd backend && pytest tests/test_preview_api.py -v`
Expected: FAIL with missing endpoint.

**Step 3: Write minimal implementation**

```python
# renderer.py: markdown-it parse + heading extraction + sanitize

def render_preview(raw_markdown: str, theme_id: str, preview_options: dict) -> dict:
    return {'html': sanitized_html, 'toc': toc, 'diagnostics': []}
```

**Step 4: Run test to verify it passes**

Run: `cd backend && pytest tests/test_preview_api.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add backend/app/api/transform.py backend/app/services/renderer.py backend/app/main.py backend/tests/test_preview_api.py
git commit -m "feat: add markdown preview render endpoint"
```

### Task 5: Add AI Orchestration Job Pipeline (OpenAI + DeepSeek)

**Files:**
- Create: `backend/app/services/orchestrator.py`
- Create: `backend/app/services/providers/base.py`
- Create: `backend/app/services/providers/openai_provider.py`
- Create: `backend/app/services/providers/deepseek_provider.py`
- Modify: `backend/app/api/transform.py`
- Create: `backend/tests/test_orchestrator.py`
- Create: `backend/tests/test_ai_job_api.py`

**Step 1: Write the failing test**

```python
from app.services.orchestrator import chunk_markdown, merge_sections


def test_chunk_markdown_by_headings():
    md = '# A\ntext\n## B\ntext\n## C\ntext'
    chunks = chunk_markdown(md, max_chars=20)
    assert len(chunks) >= 2


def test_merge_sections_contains_required_structure():
    merged = merge_sections(['intro', 'core', 'case', 'summary'])
    assert '引言' in merged
    assert '核心概念' in merged
    assert '案例分析' in merged
    assert '课后总结' in merged
```

And API test:

```python
def test_ai_rewrite_job_lifecycle(client):
    create = client.post('/api/transform/ai-rewrite', json={...})
    assert create.status_code == 200
    job_id = create.json()['jobId']

    poll = client.get(f'/api/transform/jobs/{job_id}')
    assert poll.status_code == 200
    assert poll.json()['status'] in ['pending', 'running', 'done']
```

**Step 2: Run test to verify it fails**

Run: `cd backend && pytest tests/test_orchestrator.py tests/test_ai_job_api.py -v`
Expected: FAIL because orchestration does not exist.

**Step 3: Write minimal implementation**

```python
# orchestrator.py
# - chunk markdown
# - assemble prompt
# - call provider client
# - retry failed chunks with exponential backoff
# - merge and normalize section headings
```

**Step 4: Run test to verify it passes**

Run: `cd backend && pytest tests/test_orchestrator.py tests/test_ai_job_api.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add backend/app/services/orchestrator.py backend/app/services/providers/base.py backend/app/services/providers/openai_provider.py backend/app/services/providers/deepseek_provider.py backend/app/api/transform.py backend/tests/test_orchestrator.py backend/tests/test_ai_job_api.py
git commit -m "feat: add ai rewrite orchestration and job polling"
```

### Task 6: Implement Template Injection and ZIP Export

**Files:**
- Create: `backend/app/api/export.py`
- Create: `backend/app/services/template_engine.py`
- Create: `backend/app/services/exporter.py`
- Create: `backend/app/templates/classic.html`
- Create: `backend/app/templates/modern.html`
- Modify: `backend/app/main.py`
- Create: `backend/tests/test_export_api.py`

**Step 1: Write the failing test**

```python
from fastapi.testclient import TestClient
from app.main import app


def test_export_creates_zip_and_downloads():
    client = TestClient(app)
    create = client.post('/api/export/zip', json={
        'finalMarkdown': '# Lesson',
        'themeId': 'classic',
        'previewOptions': {'toc': True}
    })
    assert create.status_code == 200
    artifact = create.json()['artifactId']

    download = client.get(f'/api/export/download/{artifact}')
    assert download.status_code == 200
    assert download.headers['content-type'] == 'application/zip'
```

**Step 2: Run test to verify it fails**

Run: `cd backend && pytest tests/test_export_api.py -v`
Expected: FAIL with missing endpoint.

**Step 3: Write minimal implementation**

```python
# exporter.py
# 1) render html via template_engine
# 2) write html/css/js into temp dir
# 3) zip directory
# 4) return artifact id + path
```

**Step 4: Run test to verify it passes**

Run: `cd backend && pytest tests/test_export_api.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add backend/app/api/export.py backend/app/services/template_engine.py backend/app/services/exporter.py backend/app/templates/classic.html backend/app/templates/modern.html backend/app/main.py backend/tests/test_export_api.py
git commit -m "feat: add template render and zip export api"
```

### Task 7: Build Frontend Workspace Shell (Editor + Preview)

**Files:**
- Create: `frontend/src/components/MarkdownEditor.tsx`
- Create: `frontend/src/components/PreviewPane.tsx`
- Create: `frontend/src/lib/api.ts`
- Create: `frontend/src/state/useWorkbenchStore.ts`
- Modify: `frontend/src/App.tsx`
- Create: `frontend/src/components/__tests__/preview-pane.test.tsx`

**Step 1: Write the failing test**

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../../App';

test('typing markdown refreshes preview pane', async () => {
  render(<App />);
  const editor = screen.getByLabelText(/markdown input/i);
  await userEvent.type(editor, '# Demo');
  expect(await screen.findByText('Demo')).toBeInTheDocument();
});
```

**Step 2: Run test to verify it fails**

Run: `cd frontend && npm test -- src/components/__tests__/preview-pane.test.tsx`
Expected: FAIL with missing editor/preview behavior.

**Step 3: Write minimal implementation**

```tsx
// App.tsx
// - render left editor and right preview
// - debounce preview request to /api/transform/preview
```

**Step 4: Run test to verify it passes**

Run: `cd frontend && npm test -- src/components/__tests__/preview-pane.test.tsx`
Expected: PASS.

**Step 5: Commit**

```bash
git add frontend/src/components/MarkdownEditor.tsx frontend/src/components/PreviewPane.tsx frontend/src/lib/api.ts frontend/src/state/useWorkbenchStore.ts frontend/src/App.tsx frontend/src/components/__tests__/preview-pane.test.tsx
git commit -m "feat: add editor and live preview workspace"
```

### Task 8: Add Settings/Auth UI and AI Rewrite Controls

**Files:**
- Create: `frontend/src/components/SettingsDrawer.tsx`
- Create: `frontend/src/components/ModelControls.tsx`
- Modify: `frontend/src/App.tsx`
- Create: `frontend/src/components/__tests__/settings-drawer.test.tsx`
- Create: `frontend/src/components/__tests__/ai-rewrite-flow.test.tsx`

**Step 1: Write the failing tests**

```tsx
test('saves provider credentials via settings api', async () => {
  // open settings, fill provider/key/password, submit, assert success toast
});

test('ai rewrite replaces preview content after job done', async () => {
  // trigger rewrite and assert transformed section titles appear
});
```

**Step 2: Run test to verify it fails**

Run: `cd frontend && npm test -- src/components/__tests__/settings-drawer.test.tsx src/components/__tests__/ai-rewrite-flow.test.tsx`
Expected: FAIL due missing UI/actions.

**Step 3: Write minimal implementation**

```tsx
// SettingsDrawer: save credentials + activate model
// ModelControls: audience/style/length + rewrite button + polling
```

**Step 4: Run test to verify it passes**

Run: `cd frontend && npm test -- src/components/__tests__/settings-drawer.test.tsx src/components/__tests__/ai-rewrite-flow.test.tsx`
Expected: PASS.

**Step 5: Commit**

```bash
git add frontend/src/components/SettingsDrawer.tsx frontend/src/components/ModelControls.tsx frontend/src/App.tsx frontend/src/components/__tests__/settings-drawer.test.tsx frontend/src/components/__tests__/ai-rewrite-flow.test.tsx
git commit -m "feat: add settings auth and ai rewrite controls"
```

### Task 9: Implement Export UX and End-to-End Verification

**Files:**
- Create: `frontend/src/components/ExportPanel.tsx`
- Modify: `frontend/src/App.tsx`
- Create: `frontend/e2e/workbench.spec.ts`
- Create: `README.md`

**Step 1: Write the failing E2E test**

```ts
import { test, expect } from '@playwright/test';

test('markdown to ai rewrite to zip export', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await page.getByLabel('Markdown Input').fill('# Topic');
  await page.getByRole('button', { name: 'AI Rewrite' }).click();
  await expect(page.getByText('核心概念')).toBeVisible();
  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Export ZIP' }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toContain('.zip');
});
```

**Step 2: Run test to verify it fails**

Run: `cd frontend && npm run e2e -- workbench.spec.ts`
Expected: FAIL before export flow exists.

**Step 3: Write minimal implementation**

```tsx
// ExportPanel calls POST /api/export/zip then downloads artifact
```

**Step 4: Run full verification**

Run: `cd backend && pytest -v`
Expected: all backend tests PASS.

Run: `cd frontend && npm test`
Expected: all frontend tests PASS.

Run: `cd frontend && npm run build`
Expected: build succeeds.

Run: `cd frontend && npm run e2e -- workbench.spec.ts`
Expected: PASS.

**Step 5: Commit**

```bash
git add frontend/src/components/ExportPanel.tsx frontend/src/App.tsx frontend/e2e/workbench.spec.ts README.md
git commit -m "feat: add export workflow and end-to-end verification"
```

### Task 10: Final Hardening and Release Checklist

**Files:**
- Modify: `backend/app/services/renderer.py`
- Modify: `backend/app/services/settings_store.py`
- Modify: `frontend/src/components/PreviewPane.tsx`
- Create: `backend/tests/test_security_guards.py`
- Create: `docs/plans/2026-03-12-markteach-workbench-release-checklist.md`

**Step 1: Write failing security tests**

```python
def test_logs_do_not_leak_api_key():
    ...

def test_script_tags_are_removed_from_rendered_html():
    ...
```

**Step 2: Run test to verify it fails**

Run: `cd backend && pytest tests/test_security_guards.py -v`
Expected: FAIL before hardening.

**Step 3: Write minimal hardening implementation**

```python
# enforce scrubbers in logs and sanitizer allow-list
```

**Step 4: Run test to verify it passes**

Run: `cd backend && pytest tests/test_security_guards.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add backend/app/services/renderer.py backend/app/services/settings_store.py frontend/src/components/PreviewPane.tsx backend/tests/test_security_guards.py docs/plans/2026-03-12-markteach-workbench-release-checklist.md
git commit -m "chore: security hardening and release checklist"
```

## Execution Notes
- Keep each task in strict RED -> GREEN -> REFACTOR order.
- Do not start next task until current task tests are green.
- Keep commits small and task-scoped.
- If a test fails unexpectedly, invoke @systematic-debugging before code changes.
