from fastapi.testclient import TestClient

from app.main import app


def test_preview_generates_html_and_toc() -> None:
    client = TestClient(app)
    markdown = '# Title\n\n## Part\n\n```python\nprint(1)\n```'

    res = client.post(
        '/api/transform/preview',
        json={
            'rawMarkdown': markdown,
            'themeId': 'classic',
            'previewOptions': {'toc': True},
        },
    )

    assert res.status_code == 200
    body = res.json()
    assert '<h1' in body['html']
    assert len(body['toc']) == 2


def test_preview_sanitizes_xss() -> None:
    client = TestClient(app)

    res = client.post(
        '/api/transform/preview',
        json={
            'rawMarkdown': '<script>alert(1)</script>',
            'themeId': 'classic',
            'previewOptions': {},
        },
    )

    assert '<script' not in res.json()['html']
