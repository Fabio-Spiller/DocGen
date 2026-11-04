"""Contêineres do documento: o próprio Document e as seções."""

from typing import TYPE_CHECKING

from docgen.elements.base import CompositeElement

if TYPE_CHECKING:
    from docgen.exporters.base import BaseExporter


class Document(CompositeElement):
    """Padrão: Composite — a raiz da árvore. Guarda o título e os elementos do documento."""

    def __init__(self, title: str) -> None:
        if not title.strip():
            raise ValueError("O título do documento não pode ser vazio")
        super().__init__()
        self.title = title

    def accept(self, visitor: "BaseExporter") -> str:
        return visitor.visit_document(self)


class Section(CompositeElement):
    """Padrão: Composite — um grupo de elementos com título próprio, dentro do documento."""

    def __init__(self, title: str) -> None:
        if not title.strip():
            raise ValueError("O título da seção não pode ser vazio")
        super().__init__()
        self.title = title

    def accept(self, visitor: "BaseExporter") -> str:
        return visitor.visit_section(self)
