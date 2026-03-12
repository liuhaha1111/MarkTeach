from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.services.exporter import Exporter

router = APIRouter(prefix='/api/export', tags=['export'])


class ExportRequest(BaseModel):
    finalMarkdown: str = Field(default='')
    themeId: str = Field(default='classic')
    previewOptions: dict[str, Any] = Field(default_factory=dict)


@router.post('/zip')
def export_zip(payload: ExportRequest) -> dict[str, str]:
    exporter = Exporter.from_env()
    artifact = exporter.export_zip(
        final_markdown=payload.finalMarkdown,
        theme_id=payload.themeId,
        preview_options=payload.previewOptions,
    )
    return {
        'artifactId': artifact['artifactId'],
        'downloadUrl': f"/api/export/download/{artifact['artifactId']}",
    }


@router.get('/download/{artifact_id}')
def download_artifact(artifact_id: str):
    exporter = Exporter.from_env()
    zip_path = exporter.resolve_zip(artifact_id)

    if zip_path is None:
        raise HTTPException(status_code=404, detail='artifact not found')

    return FileResponse(zip_path, media_type='application/zip', filename=f'{artifact_id}.zip')
