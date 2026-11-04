"""Classe base de todos os exportadores."""

from abc import ABC, abstractmethod
from pathlib import Path

from docgen.elements.base import CompositeElement
from docgen.elements.blocks import BulletList, Heading, Paragraph, Table
from docgen.elements.document import Document, Section
from docgen.elements.text import TextComponent

FILE_ENCODING = "utf-8"


class BaseExporter(ABC):
    """Padrões: Template Method + Visitor — base de todos os exportadores.

    Esta classe usa dois padrões, cada um em métodos diferentes:

    * Template Method: o método ``export`` define a ordem fixa da exportação
      (cabeçalho → elementos → rodapé). As subclasses só preenchem as etapas.
    * Visitor: os métodos ``visit_*`` dizem como cada tipo de elemento vira
      texto. Para criar um formato novo, basta criar uma subclasse com esses
      métodos, sem mexer em nenhuma classe de elemento.

    Os métodos ``format_*`` dizem como cada estilo de texto (negrito, itálico,
    link) aparece neste formato. Eles são chamados pelos decorators de texto.
    """

    # ------------------------------------------------------------------
    # Template Method
    # ------------------------------------------------------------------

    def export(self, document: Document) -> str:
        """Padrão: Template Method — o "roteiro" fixo de toda exportação.

        1. gera o cabeçalho;
        2. percorre os elementos do documento (Visitor);
        3. gera o rodapé.

        As subclasses não mudam esta ordem: elas só implementam as etapas.
        """
        header = self.header(document)
        body = document.accept(self)
        footer = self.footer(document)
        content = header + body + footer
        # Garante que toda saída termine com exatamente uma quebra de linha.
        return content.rstrip() + "\n"

    @abstractmethod
    def header(self, document: Document) -> str:
        """Etapa obrigatória: o começo da saída (geralmente o título do documento)."""

    def footer(self, document: Document) -> str:
        """Etapa opcional (um "gancho"): por padrão não há rodapé."""
        return ""

    def save(self, document: Document, path: str | Path) -> None:
        """Exporta o documento e grava o resultado no arquivo ``path``.

        Um formato binário (como PDF) pode sobrescrever este método para
        gravar o arquivo do seu próprio jeito.
        """
        Path(path).write_text(self.export(document), encoding=FILE_ENCODING)

    # ------------------------------------------------------------------
    # Visitor
    # ------------------------------------------------------------------

    def visit_document(self, document: Document) -> str:
        """O corpo do documento é simplesmente o texto de todos os seus filhos."""
        return self.render_children(document)

    @abstractmethod
    def visit_section(self, section: Section) -> str:
        """Devolve o texto de uma seção (título + filhos)."""

    @abstractmethod
    def visit_heading(self, heading: Heading) -> str:
        """Devolve o texto de um título."""

    @abstractmethod
    def visit_paragraph(self, paragraph: Paragraph) -> str:
        """Devolve o texto de um parágrafo."""

    @abstractmethod
    def visit_bullet_list(self, bullet_list: BulletList) -> str:
        """Devolve o texto de uma lista com marcadores."""

    @abstractmethod
    def visit_table(self, table: Table) -> str:
        """Devolve o texto de uma tabela."""

    # ------------------------------------------------------------------
    # Estilos de texto (chamados pelos decorators Bold, Italic e Link)
    # ------------------------------------------------------------------

    @abstractmethod
    def format_text(self, content: str) -> str:
        """Devolve um texto simples, já preparado para este formato."""

    @abstractmethod
    def format_bold(self, content: str) -> str:
        """Devolve o conteúdo em negrito."""

    @abstractmethod
    def format_italic(self, content: str) -> str:
        """Devolve o conteúdo em itálico."""

    @abstractmethod
    def format_link(self, content: str, url: str) -> str:
        """Devolve o conteúdo como um link para ``url``."""

    # ------------------------------------------------------------------
    # Ajudantes para as subclasses
    # ------------------------------------------------------------------

    def render_children(self, container: CompositeElement) -> str:
        """Visita cada filho do contêiner, na ordem, e junta os textos gerados."""
        parts = []
        for child in container.children:
            parts.append(child.accept(self))
        return "".join(parts)

    def render_cells(self, cells: list[TextComponent]) -> list[str]:
        """Transforma cada célula (ou item) em texto deste formato."""
        rendered = []
        for cell in cells:
            rendered.append(cell.render(self))
        return rendered
