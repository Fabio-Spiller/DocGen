"""Porta de entrada simples da biblioteca."""

from pathlib import Path

from docgen.elements.document import Document
from docgen.exporters.base import BaseExporter
from docgen.exporters.html import HtmlExporter
from docgen.exporters.markdown import MarkdownExporter
from docgen.exporters.plain_text import PlainTextExporter


class DocGen:
    """Padrão: Facade — esconde a escolha do exportador e a escrita em arquivo atrás de poucos métodos.

    O cliente só diz o nome do formato (``"html"``, ``"markdown"``, ``"text"``)
    e a fachada cuida do resto: encontra a classe certa, cria o exportador
    e devolve o texto ou grava o arquivo.

    Os métodos são ``@classmethod``: o cliente chama direto na classe
    (``DocGen.export(...)``), sem precisar criar um objeto ``DocGen``.
    """

    # Registro de formatos: liga um nome à classe que sabe gerar aquele formato.
    # A fachada só conhece BaseExporter (a abstração); ela nunca testa
    # "se o formato for html, faça X". Por isso formatos novos entram sem mudar este arquivo.
    _exporters: dict[str, type[BaseExporter]] = {
        "text": PlainTextExporter,
        "markdown": MarkdownExporter,
        "html": HtmlExporter,
    }

    @classmethod
    def register_exporter(cls, format_name: str, exporter_class: type[BaseExporter]) -> None:
        """Registra um formato novo (ou troca um existente) com o nome ``format_name``."""
        if not format_name.strip():
            raise ValueError("O nome do formato não pode ser vazio")
        cls._exporters[format_name] = exporter_class

    @classmethod
    def available_formats(cls) -> list[str]:
        """Lista, em ordem alfabética, os nomes de formato que podem ser usados."""
        return sorted(cls._exporters)

    @classmethod
    def export(cls, document: Document, format_name: str) -> str:
        """Exporta o documento no formato pedido e devolve o texto gerado."""
        return cls._create_exporter(format_name).export(document)

    @classmethod
    def save(cls, document: Document, format_name: str, path: str | Path) -> None:
        """Exporta o documento no formato pedido e grava o resultado no arquivo ``path``."""
        cls._create_exporter(format_name).save(document, path)

    @classmethod
    def _create_exporter(cls, format_name: str) -> BaseExporter:
        """Encontra a classe registrada para o formato e cria um exportador dela."""
        if format_name not in cls._exporters:
            available = ", ".join(cls.available_formats())
            raise ValueError(
                f"Formato desconhecido: '{format_name}'. Formatos disponíveis: {available}"
            )
        exporter_class = cls._exporters[format_name]
        return exporter_class()
