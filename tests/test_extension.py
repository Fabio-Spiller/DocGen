"""Testes de extensão: tudo aqui é código de "cliente" criado sem alterar a biblioteca.

Eles provam o Open/Closed (dá para estender sem modificar a lib) e o
Liskov (as classes do cliente funcionam onde as nativas funcionam).
"""

import pytest

from docgen import (
    BaseExporter,
    Bold,
    DocGen,
    DocumentBuilder,
    Element,
    HtmlExporter,
    MarkdownExporter,
    Paragraph,
    PlainTextExporter,
    Text,
    TextDecorator,
)


class OutlineExporter(BaseExporter):
    """Exportador do cliente: mostra só a estrutura (títulos e quantidades)."""

    def header(self, document):
        return f"[{document.title}]\n"

    def visit_section(self, section):
        return f"+ {section.title}\n" + self.render_children(section)

    def visit_heading(self, heading):
        return f"  # {heading.text.render(self)}\n"

    def visit_paragraph(self, paragraph):
        return "  (parágrafo)\n"

    def visit_bullet_list(self, bullet_list):
        return f"  (lista com {len(bullet_list.items)} itens)\n"

    def visit_table(self, table):
        return f"  (tabela com {len(table.rows)} linhas)\n"

    def format_text(self, content):
        return content

    def format_bold(self, content):
        return content

    def format_italic(self, content):
        return content

    def format_link(self, content, url):
        return content


class Quoted(TextDecorator):
    """Estilo do cliente: coloca o texto entre aspas."""

    def render(self, exporter):
        return "“" + self.inner.render(exporter) + "”"


class Alert(Element):
    """Elemento do cliente montado a partir de um elemento que já existe."""

    def __init__(self, message):
        self.message = message

    def accept(self, visitor):
        return Paragraph(Bold(Text("Aviso: " + self.message))).accept(visitor)


def sample_document():
    return (
        DocumentBuilder("Relatório")
        .section("Vendas")
        .heading("Resumo")
        .paragraph("texto")
        .bullet_list(["a", "b"])
        .table(headers=["Mês"], rows=[["Jan"], ["Fev"]])
        .build()
    )


def test_exportador_do_cliente_funciona_direto():
    expected = (
        "[Relatório]\n"
        "+ Vendas\n"
        "  # Resumo\n"
        "  (parágrafo)\n"
        "  (lista com 2 itens)\n"
        "  (tabela com 2 linhas)\n"
    )
    assert OutlineExporter().export(sample_document()) == expected


def test_exportador_do_cliente_funciona_pela_facade_depois_de_registrado():
    DocGen.register_exporter("outline", OutlineExporter)

    result = DocGen.export(sample_document(), "outline")

    assert result == OutlineExporter().export(sample_document())
    assert "outline" in DocGen.available_formats()


def test_exportador_do_cliente_pode_usar_o_gancho_de_rodape():
    class SignedMarkdownExporter(MarkdownExporter):
        def footer(self, document):
            return "---\nGerado pela DocGen\n"

    document = DocumentBuilder("Doc").paragraph("texto").build()

    expected = "# Doc\n\ntexto\n\n---\nGerado pela DocGen\n"
    assert SignedMarkdownExporter().export(document) == expected


@pytest.mark.parametrize(
    "exporter, expected",
    [
        (MarkdownExporter(), "“**oi**”"),
        (HtmlExporter(), "“<strong>oi</strong>”"),
        (PlainTextExporter(), "“oi”"),
    ],
)
def test_estilo_do_cliente_funciona_em_todos_os_exportadores_nativos(exporter, expected):
    assert Quoted(Bold(Text("oi"))).render(exporter) == expected


def test_estilo_do_cliente_pode_ser_envolvido_por_estilo_nativo():
    assert Bold(Quoted(Text("oi"))).render(MarkdownExporter()) == "**“oi”**"


def test_elemento_do_cliente_funciona_em_todos_os_formatos():
    document = DocumentBuilder("Doc").add(Alert("cuidado")).build()

    assert DocGen.export(document, "markdown") == "# Doc\n\n**Aviso: cuidado**\n"
    assert "<p><strong>Aviso: cuidado</strong></p>" in DocGen.export(document, "html")
    assert DocGen.export(document, "text") == "Doc\n===\n\nAviso: cuidado\n"
