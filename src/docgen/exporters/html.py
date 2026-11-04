"""Exportador para HTML."""

import html

from docgen.elements.blocks import BulletList, Heading, Paragraph, Table
from docgen.elements.document import Document, Section
from docgen.exporters.base import BaseExporter

HTML_CHARSET = "utf-8"
DOCUMENT_TITLE_LEVEL = 1
SECTION_TITLE_LEVEL = 2
HEADER_CELL_TAG = "th"
DATA_CELL_TAG = "td"


class HtmlExporter(BaseExporter):
    """Gera uma página HTML completa.

    Todo texto do cliente passa por ``html.escape``. Assim um ``<`` digitado
    pelo usuário aparece como texto, e não vira uma tag que quebra a página.
    """

    def header(self, document: Document) -> str:
        title = html.escape(document.title)
        return (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<head>\n"
            f'<meta charset="{HTML_CHARSET}">\n'
            f"<title>{title}</title>\n"
            "</head>\n"
            "<body>\n"
            + self._heading_tag(title, DOCUMENT_TITLE_LEVEL)
        )

    def footer(self, document: Document) -> str:
        return "</body>\n</html>\n"

    def visit_section(self, section: Section) -> str:
        title = self._heading_tag(html.escape(section.title), SECTION_TITLE_LEVEL)
        return "<section>\n" + title + self.render_children(section) + "</section>\n"

    def visit_heading(self, heading: Heading) -> str:
        return self._heading_tag(heading.text.render(self), heading.level)

    def visit_paragraph(self, paragraph: Paragraph) -> str:
        return f"<p>{paragraph.content.render(self)}</p>\n"

    def visit_bullet_list(self, bullet_list: BulletList) -> str:
        lines = []
        for item in self.render_cells(bullet_list.items):
            lines.append(f"<li>{item}</li>\n")
        return "<ul>\n" + "".join(lines) + "</ul>\n"

    def visit_table(self, table: Table) -> str:
        lines = [self._table_row(self.render_cells(table.headers), HEADER_CELL_TAG)]
        for row in table.rows:
            lines.append(self._table_row(self.render_cells(row), DATA_CELL_TAG))
        return "<table>\n" + "".join(lines) + "</table>\n"

    def format_text(self, content: str) -> str:
        return html.escape(content)

    def format_bold(self, content: str) -> str:
        return f"<strong>{content}</strong>"

    def format_italic(self, content: str) -> str:
        return f"<em>{content}</em>"

    def format_link(self, content: str, url: str) -> str:
        return f'<a href="{html.escape(url)}">{content}</a>'

    def _heading_tag(self, text: str, level: int) -> str:
        """Monta um título: ``<h2>Texto</h2>`` para o nível 2, por exemplo."""
        return f"<h{level}>{text}</h{level}>\n"

    def _table_row(self, cells: list[str], cell_tag: str) -> str:
        """Monta uma linha ``<tr>`` usando ``<th>`` (cabeçalho) ou ``<td>`` (dados)."""
        parts = []
        for cell in cells:
            parts.append(f"<{cell_tag}>{cell}</{cell_tag}>")
        return "<tr>" + "".join(parts) + "</tr>\n"
