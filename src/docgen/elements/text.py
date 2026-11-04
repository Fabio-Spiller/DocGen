"""Texto com estilo: Text (simples) e os decorators Bold, Italic e Link."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from docgen.exporters.base import BaseExporter


class TextComponent(ABC):
    """Padrão: Decorator (componente) — tudo que pode ser desenhado como texto.

    Tanto o texto simples (``Text``) quanto os estilos (``Bold``, ``Italic``...)
    seguem esta interface. Por isso um estilo pode envolver outro estilo.
    """

    @abstractmethod
    def render(self, exporter: "BaseExporter") -> str:
        """Devolve o texto pronto no formato do exportador recebido."""


class Text(TextComponent):
    """Texto simples, sem estilo. É o "miolo" que os decorators envolvem."""

    def __init__(self, content: str) -> None:
        if not content:
            raise ValueError("O texto não pode ser vazio")
        self.content = content

    def render(self, exporter: "BaseExporter") -> str:
        return exporter.format_text(self.content)


class TextDecorator(TextComponent):
    """Padrão: Decorator — permite combinar estilos de texto sem criar uma classe para cada combinação.

    Um decorator guarda outro texto dentro dele (``inner``) e acrescenta um
    estilo por fora. Exemplo: ``Bold(Italic(Text("oi")))`` é negrito + itálico,
    sem existir uma classe ``BoldItalic``.
    """

    def __init__(self, inner: TextComponent) -> None:
        self.inner = inner

    @abstractmethod
    def render(self, exporter: "BaseExporter") -> str:
        """Desenha o texto de dentro e aplica o estilo deste decorator por fora."""


class Bold(TextDecorator):
    """Deixa o texto em negrito."""

    def render(self, exporter: "BaseExporter") -> str:
        return exporter.format_bold(self.inner.render(exporter))


class Italic(TextDecorator):
    """Deixa o texto em itálico."""

    def render(self, exporter: "BaseExporter") -> str:
        return exporter.format_italic(self.inner.render(exporter))


class Link(TextDecorator):
    """Transforma o texto em um link para o endereço ``url``."""

    def __init__(self, inner: TextComponent, url: str) -> None:
        if not url.strip():
            raise ValueError("O endereço do link não pode ser vazio")
        super().__init__(inner)
        self.url = url

    def render(self, exporter: "BaseExporter") -> str:
        return exporter.format_link(self.inner.render(exporter), self.url)


def to_text(content: str | TextComponent) -> TextComponent:
    """Converte uma string comum em ``Text``; um texto com estilo volta do jeito que veio.

    Isso deixa o cliente escrever ``Paragraph("olá")`` em vez de
    ``Paragraph(Text("olá"))``. O ``isinstance`` aqui só converte a entrada;
    ele não decide nada sobre o formato de saída.
    """
    if isinstance(content, str):
        return Text(content)
    return content
