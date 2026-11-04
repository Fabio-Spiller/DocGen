"""DocGen: biblioteca para montar documentos por código e exportá-los em vários formatos.

Tudo o que o cliente precisa pode ser importado direto daqui, por exemplo:

    from docgen import DocGen, DocumentBuilder, Bold, Text
"""

from docgen.builder import DocumentBuilder
from docgen.elements.base import CompositeElement, Element
from docgen.elements.blocks import BulletList, Heading, Paragraph, Table
from docgen.elements.document import Document, Section
from docgen.elements.text import Bold, Italic, Link, Text, TextComponent, TextDecorator
from docgen.exporters.base import BaseExporter
from docgen.exporters.html import HtmlExporter
from docgen.exporters.markdown import MarkdownExporter
from docgen.exporters.plain_text import PlainTextExporter
from docgen.facade import DocGen

__all__ = [
    "BaseExporter",
    "Bold",
    "BulletList",
    "CompositeElement",
    "DocGen",
    "Document",
    "DocumentBuilder",
    "Element",
    "Heading",
    "HtmlExporter",
    "Italic",
    "Link",
    "MarkdownExporter",
    "Paragraph",
    "PlainTextExporter",
    "Section",
    "Table",
    "Text",
    "TextComponent",
    "TextDecorator",
]
