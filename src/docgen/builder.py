"""Montagem do documento passo a passo."""

from docgen.elements.base import CompositeElement, Element
from docgen.elements.blocks import DEFAULT_HEADING_LEVEL, BulletList, Heading, Paragraph, Table
from docgen.elements.document import Document, Section
from docgen.elements.text import TextComponent


class DocumentBuilder:
    """Padrão: Builder — monta a árvore do documento passo a passo, com chamadas encadeadas.

    Sem o builder, o cliente teria que criar cada objeto e ligar um ao outro
    à mão. Com ele, basta descrever o documento na ordem em que ele é lido::

        DocumentBuilder("Relatório").heading("Resumo").paragraph("...").build()

    Cada método devolve o próprio builder (``return self``); é isso que
    permite encadear as chamadas.
    """

    def __init__(self, title: str) -> None:
        self._document = Document(title)
        # Contêiner que recebe os próximos elementos. Começa sendo o documento
        # e passa a ser a seção mais recente quando ``section()`` é chamado.
        self._current: CompositeElement = self._document

    def section(self, title: str) -> "DocumentBuilder":
        """Abre uma nova seção. Os próximos elementos entram dentro dela."""
        new_section = Section(title)
        self._document.add(new_section)
        self._current = new_section
        return self

    def end_section(self) -> "DocumentBuilder":
        """Fecha a seção aberta. Os próximos elementos voltam para o documento."""
        self._current = self._document
        return self

    def heading(self, text: str | TextComponent, level: int = DEFAULT_HEADING_LEVEL) -> "DocumentBuilder":
        """Adiciona um título."""
        return self.add(Heading(text, level))

    def paragraph(self, content: str | TextComponent) -> "DocumentBuilder":
        """Adiciona um parágrafo."""
        return self.add(Paragraph(content))

    def bullet_list(self, items: list[str | TextComponent]) -> "DocumentBuilder":
        """Adiciona uma lista com marcadores."""
        return self.add(BulletList(items))

    def table(
        self,
        headers: list[str | TextComponent],
        rows: list[list[str | TextComponent]],
    ) -> "DocumentBuilder":
        """Adiciona uma tabela."""
        return self.add(Table(headers, rows))

    def add(self, element: Element) -> "DocumentBuilder":
        """Adiciona qualquer elemento, inclusive um criado pelo próprio cliente."""
        self._current.add(element)
        return self

    def build(self) -> Document:
        """Entrega o documento pronto."""
        return self._document
