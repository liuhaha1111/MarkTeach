import re
import unicodedata

import bleach
import markdown

HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.*\S)\s*$')


def _slugify(value: str) -> str:
    normalized = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', normalized).strip().lower()
    return re.sub(r'[-\s]+', '-', slug) or 'section'


def _extract_toc(raw_markdown: str) -> list[dict]:
    toc: list[dict] = []
    for line in raw_markdown.splitlines():
        match = HEADING_PATTERN.match(line)
        if not match:
            continue
        level = len(match.group(1))
        text = match.group(2).strip()
        toc.append({'id': _slugify(text), 'text': text, 'level': level})
    return toc


def render_preview(raw_markdown: str, theme_id: str, preview_options: dict) -> dict:
    del theme_id

    html = markdown.markdown(
        raw_markdown,
        extensions=['fenced_code', 'tables', 'codehilite'],
    )

    allowed_tags = set(bleach.sanitizer.ALLOWED_TAGS).union(
        {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'code', 'div', 'span', 'hr'}
    )
    allowed_attributes = {
        **bleach.sanitizer.ALLOWED_ATTRIBUTES,
        'a': ['href', 'title', 'rel'],
        'code': ['class'],
        'div': ['class'],
        'span': ['class'],
    }
    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True,
        strip_comments=True,
    )

    toc = _extract_toc(raw_markdown)
    if preview_options.get('toc') is False:
        toc = []

    return {'html': clean_html, 'toc': toc, 'diagnostics': []}
