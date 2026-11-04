"""Exportador para Markdown."""

from docgen.elements.blocks import BulletList, Heading, Paragraph, Table
from docgen.elements.document import Document, Section
from docgen.exporters.base import BaseExporter

HEADING_MARK = "#"
BULLET_MARK = "- "
TABLE_DIVIDER = "---"
BOLD_MARK = "**"
ITALIC_MARK = "*"
# Em Markdown, uma linha em branco separa um bloco do próximo.
BLOCK_SEPARATOR = "\n\n"
DOCUMENT_TITLE_LEVEL = 1
SECTION_TITLE_LEVEL = 2


class MarkdownExporter(BaseExporter):
    """Gera o documento em Markdown (``#`` para títulos, ``-`` para listas...)."""

    def header(self, document: Document) -> str:
        return self._heading_line(document.title, DOCUMENT_TITLE_LEVEL)

    def visit_section(self, section: Section) -> str:
        title = self._heading_line(section.title, SECTION_TITLE_LEVEL)
        return title + self.render_children(section)

    def visit_heading(self, heading: Heading) -> str:
        return self._heading_line(heading.text.render(self), heading.level)

    def visit_paragraph(self, paragraph: Paragraph) -> str:
        return paragraph.content.render(self) + BLOCK_SEPARATOR

    def visit_bullet_list(self, bullet_list: BulletList) -> str:
        lines = []
        for item in self.render_cells(bullet_list.items):
            lines.append(BULLET_MARK + item)
        return "\n".join(lines) + BLOCK_SEPARATOR

    def visit_table(self, table: Table) -> str:
        header_cells = self.render_cells(table.headers)
        divider_cells = [TABLE_DIVIDER] * len(header_cells)
        lines = [self._table_row(header_cells), self._table_row(divider_cells)]
        for row in table.rows:
            lines.append(self._table_row(self.render_cells(row)))
        return "\n".join(lines) + BLOCK_SEPARATOR

    def format_text(self, content: str) -> str:
        return content

    def format_bold(self, content: str) -> str:
        return BOLD_MARK + content + BOLD_MARK

    def format_italic(self, content: str) -> str:
        return ITALIC_MARK + content + ITALIC_MARK

    def format_link(self, content: str, url: str) -> str:
        return f"[{content}]({url})"

    def _heading_line(self, text: str, level: int) -> str:
        """Monta um título: ``## Texto`` para o nível 2, por exemplo."""
        return HEADING_MARK * level + " " + text + BLOCK_SEPARATOR

    def _table_row(self, cells: list[str]) -> str:
        """Monta uma linha de tabela: ``| a | b |``."""
        return "| " + " | ".join(cells) + " |"
