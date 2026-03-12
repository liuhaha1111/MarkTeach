from fastapi.testclient import TestClient

from app.main import app


def test_export_creates_zip_and_downloads(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv('MARKTEACH_DATA_DIR', str(tmp_path))
    client = TestClient(app)

    create = client.post(
        '/api/export/zip',
        json={
            'finalMarkdown': '# Lesson',
            'themeId': 'classic',
            'previewOptions': {'toc': True},
        },
    )
    assert create.status_code == 200
    artifact = create.json()['artifactId']

    download = client.get(f'/api/export/download/{artifact}')
    assert download.status_code == 200
    assert download.headers['content-type'] == 'application/zip'
