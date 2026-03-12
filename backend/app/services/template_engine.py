from html import escape
from pathlib import Path
from typing import Optional


class TemplateEngine:
    def __init__(self, templates_dir: Optional[Path] = None) -> None:
        self.templates_dir = templates_dir or Path(__file__).resolve().parents[1] / 'templates'

    def render(self, *, theme_id: str, content_html: str, toc: list[dict]) -> str:
        template_path = self.templates_dir / f'{theme_id}.html'
        if not template_path.exists():
            template_path = self.templates_dir / 'classic.html'

        template = template_path.read_text(encoding='utf-8')
        toc_html = ''.join(
            f"<li class='toc-level-{item['level']}'><a href='#{escape(item['id'])}'>{escape(item['text'])}</a></li>"
            for item in toc
        )

        return (
            template.replace('{{TITLE}}', 'MarkTeach Lesson')
            .replace('{{TOC}}', toc_html)
            .replace('{{CONTENT}}', content_html)
        )
