from docgen import (
    Bold,
    BulletList,
    Document,
    DocumentBuilder,
    Element,
    Heading,
    Paragraph,
    Section,
    Table,
    Text,
)


def test_builder_cria_documento_com_o_titulo_informado():
    document = DocumentBuilder("Relatório").build()

    assert isinstance(document, Document)
    assert document.title == "Relatório"


def test_builder_adiciona_elementos_na_ordem_das_chamadas():
    document = (
        DocumentBuilder("Relatório")
        .heading("Resumo")
        .paragraph("texto")
        .bullet_list(["a", "b"])
        .table(headers=["Mês"], rows=[["Jan"]])
        .build()
    )

    types = [type(child) for child in document.children]
    assert types == [Heading, Paragraph, BulletList, Table]


def test_builder_coloca_elementos_dentro_da_secao_aberta():
    document = (
        DocumentBuilder("Relatório")
        .section("Vendas")
        .paragraph("dentro da seção")
        .build()
    )

    section = document.children[0]
    assert isinstance(section, Section)
    assert section.title == "Vendas"
    assert section.children[0].content.content == "dentro da seção"


def test_nova_secao_fecha_a_anterior():
    document = (
        DocumentBuilder("Relatório")
        .section("Primeira")
        .paragraph("a")
        .section("Segunda")
        .paragraph("b")
        .build()
    )

    assert len(document.children) == 2
    assert len(document.children[0].children) == 1
    assert len(document.children[1].children) == 1


def test_end_section_volta_a_adicionar_no_documento():
    document = (
        DocumentBuilder("Relatório")
        .section("Vendas")
        .paragraph("dentro")
        .end_section()
        .paragraph("fora")
        .build()
    )

    assert len(document.children) == 2
    assert isinstance(document.children[1], Paragraph)


def test_builder_aceita_texto_com_estilo():
    document = DocumentBuilder("Relatório").paragraph(Bold(Text("Meta!"))).build()

    assert isinstance(document.children[0].content, Bold)


def test_builder_aceita_elemento_criado_pelo_cliente():
    class Divider(Element):
        def accept(self, visitor):
            return ""

    divider = Divider()
    document = DocumentBuilder("Relatório").add(divider).build()

    assert document.children == [divider]
