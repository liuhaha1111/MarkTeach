# MarkTeach Workbench Release Checklist

Date: 2026-03-12

- [x] Backend unit tests pass (`pytest -v`).
- [x] Frontend unit tests pass (`npm test`).
- [x] Frontend build passes (`npm run build`).
- [x] E2E critical flow passes (`npm run e2e -- e2e/workbench.spec.ts`).
- [x] Markdown rendering strips script tags.
- [x] Settings log context masks API keys.
- [ ] Manual smoke test with real OpenAI key.
- [ ] Manual smoke test with real DeepSeek key.
- [ ] Validate generated ZIP on a static host.
