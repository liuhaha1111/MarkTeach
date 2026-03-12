import json

from fastapi.testclient import TestClient

from app.main import app


def test_save_credentials_masks_key(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv('MARKTEACH_DATA_DIR', str(tmp_path))
    client = TestClient(app)

    res = client.post(
        '/api/settings/credentials',
        json={
            'provider': 'openai',
            'apiKey': 'sk-test-123456',
            'masterPassword': 'pass1234',
        },
    )

    assert res.status_code == 200
    body = res.json()
    assert body['ok'] is True
    assert body['maskedKey'].startswith('sk-')
    assert body['provider'] == 'openai'
    assert 'apiKey' not in body

    stored = json.loads((tmp_path / 'credentials.enc.json').read_text())
    assert 'openai' in stored
    assert 'ciphertext' in stored['openai']


def test_activate_model_persists_selection(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv('MARKTEACH_DATA_DIR', str(tmp_path))
    client = TestClient(app)

    res = client.post(
        '/api/settings/activate-model',
        json={'provider': 'deepseek', 'model': 'deepseek-chat'},
    )

    assert res.status_code == 200
    assert res.json()['activeProvider'] == 'deepseek'
    assert res.json()['activeModel'] == 'deepseek-chat'

    workspace = json.loads((tmp_path / 'workspace.json').read_text())
    assert workspace['activeProvider'] == 'deepseek'
    assert workspace['activeModel'] == 'deepseek-chat'
