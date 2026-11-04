"""Elementos simples (folhas da árvore): título, parágrafo, lista e tabela."""

from typing import TYPE_CHECKING

from docgen.elements.base import Element
from docgen.elements.text import TextComponent, to_text

if TYPE_CHECKING:
    from docgen.exporters.base import BaseExporter

MIN_HEADING_LEVEL = 1
MAX_HEADING_LEVEL = 6
# O nível 1 fica reservado para o título do documento, então os títulos internos começam no 2.
DEFAULT_HEADING_LEVEL = 2


class Heading(Element):
    """Um título dentro do documento, com nível de 1 (maior) a 6 (menor)."""

    def __init__(self, text: str | TextComponent, level: int = DEFAULT_HEADING_LEVEL) -> None:
        if level < MIN_HEADING_LEVEL or level > MAX_HEADING_LEVEL:
            raise ValueError(
                f"O nível do título deve estar entre {MIN_HEADING_LEVEL} e "
                f"{MAX_HEADING_LEVEL}, mas foi recebido {level}"
            )
        self.text = to_text(text)
        self.level = level

    def accept(self, visitor: "BaseExporter") -> str:
        return visitor.visit_heading(self)


class Paragraph(Element):
    """Um parágrafo de texto, que pode ter estilo (ex.: ``Bold(Text("..."))``)."""

    def __init__(self, content: str | TextComponent) -> None:
        self.content = to_text(content)

    def accept(self, visitor: "BaseExporter") -> str:
        return visitor.visit_paragraph(self)


class BulletList(Element):
    """Uma lista de itens com marcadores."""

    def __init__(self, items: list[str | TextComponent]) -> None:
        if not items:
            raise ValueError("A lista precisa ter pelo menos um item")
        self.items = [to_text(item) for item in items]

    def accept(self, visitor: "BaseExporter") -> str:
        return visitor.visit_bullet_list(self)


class Table(Element):
    """Uma tabela com uma linha de cabeçalho e várias linhas de dados."""

    def __init__(
        self,
        headers: list[str | TextComponent],
        rows: list[list[str | TextComponent]],
    ) -> None:
        if not headers:
            raise ValueError("A tabela precisa ter pelo menos uma coluna no cabeçalho")
        for row in rows:
            if len(row) != len(headers):
                raise ValueError(
                    f"Cada linha da tabela precisa ter {len(headers)} células, "
                    f"mas uma linha tem {len(row)}"
                )
        self.headers = [to_text(cell) for cell in headers]
        self.rows = [[to_text(cell) for cell in row] for row in rows]

    def accept(self, visitor: "BaseExporter") -> str:
        return visitor.visit_table(self)
