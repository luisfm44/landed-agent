from pathlib import Path
from typing import TypedDict

KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parent


class KnowledgeSection(TypedDict):
    source: str
    title: str
    content: str


def _read_text_file(file_path: Path) -> str:
    """Read text files defensively across common encodings."""
    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    return file_path.read_text(encoding="utf-8", errors="replace")


def _split_markdown_sections(content: str) -> list[tuple[str, str]]:
    """Split markdown content into sections using headings."""
    sections: list[tuple[str, str]] = []
    current_title = "General"
    current_lines: list[str] = []

    for line in content.splitlines():
        if line.startswith("## "):
            if current_lines:
                sections.append(
                    (
                        current_title,
                        "\n".join(current_lines).strip(),
                    )
                )

            current_title = line.replace("## ", "").strip()
            current_lines = []

        elif line.startswith("# "):
            current_title = line.replace("# ", "").strip()

        else:
            current_lines.append(line)

    if current_lines:
        sections.append(
            (
                current_title,
                "\n".join(current_lines).strip(),
            )
        )

    return [
        (title, body)
        for title, body in sections
        if body
    ]


def _source_relative_path(file_path: Path) -> str:
    return str(file_path.relative_to(KNOWLEDGE_BASE_DIR.parent))


def load_knowledge_sections(
    knowledge_dir: Path | None = None,
) -> list[KnowledgeSection]:
    """Load all markdown sections from the unified knowledge base."""
    base_dir = knowledge_dir or KNOWLEDGE_BASE_DIR
    sections: list[KnowledgeSection] = []

    if not base_dir.exists():
        return sections

    for file_path in sorted(base_dir.rglob("*.md")):
        if file_path.name.startswith("._"):
            continue

        content = _read_text_file(file_path)
        rel_source = _source_relative_path(file_path)

        for title, body in _split_markdown_sections(content):
            sections.append(
                {
                    "source": rel_source,
                    "title": title,
                    "content": body,
                }
            )

    return sections
