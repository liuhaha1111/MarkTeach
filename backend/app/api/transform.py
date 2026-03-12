from typing import Any
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.orchestrator import rewrite_markdown
from app.services.renderer import render_preview

router = APIRouter(prefix='/api/transform', tags=['transform'])

_jobs: dict[str, dict[str, Any]] = {}


class PreviewRequest(BaseModel):
    rawMarkdown: str = Field(default='')
    themeId: str = Field(default='classic')
    previewOptions: dict[str, Any] = Field(default_factory=dict)


class AiRewriteRequest(BaseModel):
    rawMarkdown: str = Field(min_length=1)
    audienceLevel: str = Field(default='beginner')
    style: str = Field(default='teaching')
    length: str = Field(default='medium')
    themeId: str = Field(default='classic')
    provider: str = Field(default='openai')
    model: str = Field(default='default')


@router.post('/preview')
def preview(payload: PreviewRequest) -> dict:
    return render_preview(payload.rawMarkdown, payload.themeId, payload.previewOptions)


@router.post('/ai-rewrite')
def ai_rewrite(payload: AiRewriteRequest) -> dict[str, str]:
    job_id = str(uuid4())
    _jobs[job_id] = {
        'status': 'pending',
        'resultMarkdown': '',
        'html': '',
        'error': None,
        'traceId': job_id,
    }

    _jobs[job_id]['status'] = 'running'
    try:
        rewritten = rewrite_markdown(
            payload.rawMarkdown,
            provider='deepseek' if payload.provider == 'deepseek' else 'openai',
            model=payload.model,
            audience_level=payload.audienceLevel,
            style=payload.style,
            length=payload.length,
        )
        rendered = render_preview(rewritten, payload.themeId, {'toc': True})
        _jobs[job_id].update(
            {
                'status': 'done',
                'resultMarkdown': rewritten,
                'html': rendered['html'],
            }
        )
    except Exception as exc:
        _jobs[job_id].update({'status': 'failed', 'error': str(exc)})

    return {'jobId': job_id}


@router.get('/jobs/{job_id}')
def get_job(job_id: str) -> dict[str, Any]:
    job = _jobs.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail='job not found')
    return job
