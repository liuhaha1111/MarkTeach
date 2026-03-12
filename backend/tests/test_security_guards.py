import json

from app.services.renderer import render_preview
from app.services.settings_store import SettingsStore


def test_logs_do_not_leak_api_key(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv('MARKTEACH_DATA_DIR', str(tmp_path))
    store = SettingsStore.from_env()

    context = store.safe_log_context(provider='openai', api_key='sk-very-secret-123456')
    dumped = json.dumps(context)

    assert 'sk-very-secret-123456' not in dumped
    assert 'sk-' in dumped


def test_script_tags_are_removed_from_rendered_html() -> None:
    rendered = render_preview('<script>alert(1)</script><h1>Lesson</h1>', 'classic', {})

    assert '<script' not in rendered['html']
    assert 'Lesson' in rendered['html']
