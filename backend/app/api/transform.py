from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.renderer import render_preview

router = APIRouter(prefix='/api/transform', tags=['transform'])


class PreviewRequest(BaseModel):
    rawMarkdown: str = Field(default='')
    themeId: str = Field(default='classic')
    previewOptions: dict[str, Any] = Field(default_factory=dict)


@router.post('/preview')
def preview(payload: PreviewRequest) -> dict:
    return render_preview(payload.rawMarkdown, payload.themeId, payload.previewOptions)
