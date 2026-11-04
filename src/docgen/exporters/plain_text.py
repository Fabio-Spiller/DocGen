"""Exportador para texto puro (sem marcação nenhuma)."""

from docgen.elements.blocks import BulletList, Heading, Paragraph, Table
from docgen.elements.document import Document, Section
from docgen.exporters.base import BaseExporter

TITLE_UNDERLINE = "="
HEADING_UNDERLINE = "-"
BULLET_MARK = "- "
COLUMN_SEPARATOR = " | "
TABLE_DIVIDER_LINE = "-"
TABLE_DIVIDER_CROSSING = "-+-"
BLOCK_SEPARATOR = "\n\n"


class PlainTextExporter(BaseExporter):
    """Gera o documento em texto puro, bom para terminal ou arquivos ``.txt``.

    Texto puro não tem negrito nem itálico, então esses estilos são ignorados.
    """

    def header(self, document: Document) -> str:
        return self._underlined(document.title, TITLE_UNDERLINE)

    def visit_section(self, section: Section) -> str:
        title = self._underlined(section.title, HEADING_UNDERLINE)
        return title + self.render_children(section)

    def visit_heading(self, heading: Heading) -> str:
        return self._underlined(heading.text.render(self), HEADING_UNDERLINE)

    def visit_paragraph(self, paragraph: Paragraph) -> str:
        return paragraph.content.render(self) + BLOCK_SEPARATOR

    def visit_bullet_list(self, bullet_list: BulletList) -> str:
        lines = []
        for item in self.render_cells(bullet_list.items):
            lines.append(BULLET_MARK + item)
        return "\n".join(lines) + BLOCK_SEPARATOR

    def visit_table(self, table: Table) -> str:
        header_cells = self.render_cells(table.headers)
        body_rows = []
        for row in table.rows:
            body_rows.append(self.render_cells(row))

        widths = self._column_widths(header_cells, body_rows)
        lines = [self._table_row(header_cells, widths), self._table_divider(widths)]
        for cells in body_rows:
            lines.append(self._table_row(cells, widths))
        return "\n".join(lines) + BLOCK_SEPARATOR

    def format_text(self, content: str) -> str:
        return content

    def format_bold(self, content: str) -> str:
        return content

    def format_italic(self, content: str) -> str:
        return content

    def format_link(self, content: str, url: str) -> str:
        return f"{content} ({url})"

    def _underlined(self, text: str, underline_char: str) -> str:
        """Escreve o texto e, na linha de baixo, um traço do mesmo tamanho."""
        return text + "\n" + underline_char * len(text) + BLOCK_SEPARATOR

    def _column_widths(self, header_cells: list[str], body_rows: list[list[str]]) -> list[int]:
        """Descobre a largura de cada coluna: o tamanho do maior texto dela."""
        widths = []
        for cell in header_cells:
            widths.append(len(cell))
        for cells in body_rows:
            for index, cell in enumerate(cells):
                widths[index] = max(widths[index], len(cell))
        return widths

    def _table_row(self, cells: list[str], widths: list[int]) -> str:
        """Completa cada célula com espaços para as colunas ficarem alinhadas."""
        padded = []
        for cell, width in zip(cells, widths):
            padded.append(cell.ljust(width))
        return COLUMN_SEPARATOR.join(padded).rstrip()

    def _table_divider(self, widths: list[int]) -> str:
        """Linha que separa o cabeçalho dos dados, ex.: ``----+------``."""
        dashes = []
        for width in widths:
            dashes.append(TABLE_DIVIDER_LINE * width)
        return TABLE_DIVIDER_CROSSING.join(dashes)
