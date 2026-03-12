import os
from pathlib import Path
from typing import Optional
from uuid import uuid4
from zipfile import ZIP_DEFLATED, ZipFile

from app.services.renderer import render_preview
from app.services.template_engine import TemplateEngine


class Exporter:
    def __init__(self, data_dir: Path, template_engine: Optional[TemplateEngine] = None) -> None:
        self.data_dir = data_dir
        self.exports_dir = self.data_dir / 'exports'
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        self.template_engine = template_engine or TemplateEngine()

    @classmethod
    def from_env(cls) -> 'Exporter':
        configured = os.getenv('MARKTEACH_DATA_DIR')
        if configured:
            return cls(Path(configured))

        default_dir = Path(__file__).resolve().parents[2] / 'data'
        return cls(default_dir)

    def export_zip(self, *, final_markdown: str, theme_id: str, preview_options: dict) -> dict[str, str]:
        artifact_id = str(uuid4())
        artifact_dir = self.exports_dir / artifact_id
        asset_dir = artifact_dir / 'assets'
        artifact_dir.mkdir(parents=True, exist_ok=True)
        asset_dir.mkdir(parents=True, exist_ok=True)

        preview = render_preview(final_markdown, theme_id, preview_options)
        final_html = self.template_engine.render(
            theme_id=theme_id,
            content_html=preview['html'],
            toc=preview['toc'],
        )

        index_path = artifact_dir / 'index.html'
        style_path = asset_dir / 'styles.css'
        index_path.write_text(final_html, encoding='utf-8')
        style_path.write_text(self._default_style(), encoding='utf-8')

        zip_path = self.exports_dir / f'{artifact_id}.zip'
        with ZipFile(zip_path, mode='w', compression=ZIP_DEFLATED) as archive:
            for file_path in artifact_dir.rglob('*'):
                if not file_path.is_file():
                    continue
                archive.write(file_path, arcname=file_path.relative_to(artifact_dir).as_posix())

        return {'artifactId': artifact_id, 'zipPath': str(zip_path)}

    def resolve_zip(self, artifact_id: str) -> Optional[Path]:
        candidate = self.exports_dir / f'{artifact_id}.zip'
        return candidate if candidate.exists() else None

    def _default_style(self) -> str:
        return (
            'code{padding:2px 4px;background:#f4f4f4;border-radius:4px;}'
            'pre{padding:12px;background:#111;color:#f0f0f0;border-radius:8px;overflow:auto;}'
        )
