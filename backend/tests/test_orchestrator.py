from app.services.orchestrator import chunk_markdown, merge_sections


def test_chunk_markdown_by_headings() -> None:
    md = '# A\ntext\n## B\ntext\n## C\ntext'
    chunks = chunk_markdown(md, max_chars=20)

    assert len(chunks) >= 2


def test_merge_sections_contains_required_structure() -> None:
    merged = merge_sections(['intro', 'core', 'case', 'summary'])

    assert '\u5f15\u8a00' in merged
    assert '\u6838\u5fc3\u6982\u5ff5' in merged
    assert '\u6848\u4f8b\u5206\u6790' in merged
    assert '\u8bfe\u540e\u603b\u7ed3' in merged
