from docgen import (
    Bold,
    BulletList,
    Document,
    Heading,
    Italic,
    Link,
    Paragraph,
    PlainTextExporter,
    Section,
    Table,
    Text,
)


def export_with(element) -> str:
    document = Document("Doc")
    document.add(element)
    return PlainTextExporter().export(document)


def test_texto_puro_sublinha_titulo_do_documento_com_iguais():
    assert PlainTextExporter().export(Document("Relatório")) == "Relatório\n=========\n"


def test_texto_puro_sublinha_titulo_com_tracos():
    assert export_with(Heading("Resumo")) == "Doc\n===\n\nResumo\n------\n"


def test_texto_puro_exporta_paragrafo():
    assert export_with(Paragraph("Olá.")) == "Doc\n===\n\nOlá.\n"


def test_texto_puro_exporta_lista_com_tracos():
    assert export_with(BulletList(["a", "b"])) == "Doc\n===\n\n- a\n- b\n"


def test_texto_puro_exporta_tabela_com_colunas_alinhadas():
    table = Table(headers=["Mês", "Total"], rows=[["Jan", "100"], ["Fevereiro", "150"]])

    expected = (
        "Doc\n===\n\n"
        "Mês       | Total\n"
        "----------+------\n"
        "Jan       | 100\n"
        "Fevereiro | 150\n"
    )
    assert export_with(table) == expected


def test_texto_puro_exporta_secao_com_titulo_sublinhado_e_filhos():
    section = Section("Resumo")
    section.add(Paragraph("texto"))

    assert export_with(section) == "Doc\n===\n\nResumo\n------\n\ntexto\n"


def test_texto_puro_ignora_negrito_e_italico():
    assert export_with(Paragraph(Bold(Italic(Text("x"))))) == "Doc\n===\n\nx\n"


def test_texto_puro_mostra_endereco_do_link_entre_parenteses():
    paragraph = Paragraph(Link(Text("site"), "https://x.com"))

    assert export_with(paragraph) == "Doc\n===\n\nsite (https://x.com)\n"
