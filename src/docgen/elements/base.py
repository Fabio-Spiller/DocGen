"""Classes base de todos os elementos do documento."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Este import só existe para os type hints e não roda de verdade.
# Assim evitamos um import circular (os exportadores também importam os elementos).
if TYPE_CHECKING:
    from docgen.exporters.base import BaseExporter


class Element(ABC):
    """Padrão: Composite (componente) — interface comum a todas as partes do documento.

    Um parágrafo sozinho e uma seção cheia de parágrafos são tratados do mesmo
    jeito, porque os dois são um ``Element``. O único método é ``accept``: é por
    ele que o exportador (padrão Visitor) transforma o elemento em texto.
    """

    @abstractmethod
    def accept(self, visitor: "BaseExporter") -> str:
        """Entrega este elemento ao exportador e devolve o texto gerado."""


class CompositeElement(Element):
    """Padrão: Composite (composto) — elemento que guarda outros elementos dentro dele.

    ``Section`` e ``Document`` herdam desta classe. Como os filhos também são
    ``Element``, um contêiner pode guardar parágrafos, tabelas ou até elementos
    criados pelo cliente, sem precisar saber qual é qual.
    """

    def __init__(self) -> None:
        self.children: list[Element] = []

    def add(self, element: Element) -> None:
        """Adiciona um elemento filho no final da lista."""
        self.children.append(element)
