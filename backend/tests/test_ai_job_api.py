from fastapi.testclient import TestClient

from app.main import app


def test_ai_rewrite_job_lifecycle() -> None:
    client = TestClient(app)

    create = client.post(
        '/api/transform/ai-rewrite',
        json={
            'rawMarkdown': '# Topic\n\nSome notes',
            'audienceLevel': 'beginner',
            'style': 'teaching',
            'length': 'medium',
            'themeId': 'classic',
        },
    )
    assert create.status_code == 200
    job_id = create.json()['jobId']

    poll = client.get(f'/api/transform/jobs/{job_id}')
    assert poll.status_code == 200
    assert poll.json()['status'] in ['pending', 'running', 'done']
