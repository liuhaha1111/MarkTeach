import re
from typing import Literal

from app.services.providers.deepseek_provider import DeepSeekProvider
from app.services.providers.openai_provider import OpenAIProvider

ProviderName = Literal['openai', 'deepseek']


def chunk_markdown(raw_markdown: str, max_chars: int = 1200) -> list[str]:
    if not raw_markdown.strip():
        return ['']

    blocks = [block.strip() for block in re.split(r'(?m)(?=^#{1,6}\s)', raw_markdown) if block.strip()]
    if not blocks:
        blocks = [raw_markdown.strip()]

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for block in blocks:
        block_len = len(block)
        if current and current_len + block_len + 2 > max_chars:
            chunks.append('\n\n'.join(current))
            current = [block]
            current_len = block_len
        else:
            current.append(block)
            current_len += block_len + (2 if current_len else 0)

    if current:
        chunks.append('\n\n'.join(current))

    return chunks


def merge_sections(sections: list[str]) -> str:
    titles = [
        '\u5f15\u8a00',
        '\u6838\u5fc3\u6982\u5ff5',
        '\u6848\u4f8b\u5206\u6790',
        '\u8bfe\u540e\u603b\u7ed3',
    ]

    normalized = [section.strip() for section in sections]
    while len(normalized) < 4:
        normalized.append('\u5f85\u8865\u5145\u5185\u5bb9\u3002')

    rendered = []
    for idx, title in enumerate(titles):
        content = normalized[idx] if normalized[idx] else '\u5f85\u8865\u5145\u5185\u5bb9\u3002'
        rendered.append(f'## {title}\n\n{content}')

    return '\n\n'.join(rendered)


def _provider_for(name: ProviderName):
    if name == 'deepseek':
        return DeepSeekProvider()
    return OpenAIProvider()


def rewrite_markdown(
    raw_markdown: str,
    *,
    provider: ProviderName = 'openai',
    model: str = 'default',
    audience_level: str = 'beginner',
    style: str = 'teaching',
    length: str = 'medium',
) -> str:
    chunks = chunk_markdown(raw_markdown)
    provider_client = _provider_for(provider)

    prompt = (
        f'Audience: {audience_level}; Style: {style}; Length: {length}. '
        'Restructure to teaching content.'
    )

    generated = [
        provider_client.generate_section(chunk, model=model, prompt=prompt)
        for chunk in chunks[:4]
    ]

    if not generated:
        generated = ['']

    return merge_sections(generated)
