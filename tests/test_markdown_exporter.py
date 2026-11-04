from docgen import (
    Bold,
    BulletList,
    Document,
    Heading,
    Italic,
    Link,
    MarkdownExporter,
    Paragraph,
    Section,
    Table,
    Text,
)


def export_with(element) -> str:
    document = Document("Doc")
    document.add(element)
    return MarkdownExporter().export(document)


def test_markdown_exporta_titulo_do_documento_com_uma_hashtag():
    assert MarkdownExporter().export(Document("Relatório")) == "# Relatório\n"


def test_markdown_exporta_titulo_com_hashtags_do_nivel():
    assert export_with(Heading("Detalhes", level=3)) == "# Doc\n\n### Detalhes\n"


def test_markdown_exporta_paragrafo():
    assert export_with(Paragraph("Olá, mundo.")) == "# Doc\n\nOlá, mundo.\n"


def test_markdown_exporta_lista_com_tracos():
    assert export_with(BulletList(["Jan", "Fev"])) == "# Doc\n\n- Jan\n- Fev\n"


def test_markdown_exporta_tabela_com_barras():
    table = Table(headers=["Mês", "Total"], rows=[["Jan", "100"]])

    expected = "# Doc\n\n| Mês | Total |\n| --- | --- |\n| Jan | 100 |\n"
    assert export_with(table) == expected


def test_markdown_exporta_secao_com_titulo_de_nivel_2_e_filhos():
    section = Section("Resumo")
    section.add(Paragraph("texto"))

    assert export_with(section) == "# Doc\n\n## Resumo\n\ntexto\n"


def test_markdown_exporta_estilos_de_texto():
    assert export_with(Paragraph(Bold(Text("forte")))) == "# Doc\n\n**forte**\n"
    assert export_with(Paragraph(Italic(Text("leve")))) == "# Doc\n\n*leve*\n"
    assert export_with(Paragraph(Link(Text("site"), "https://x.com"))) == (
        "# Doc\n\n[site](https://x.com)\n"
    )


def test_markdown_separa_blocos_com_linha_em_branco():
    document = Document("Doc")
    document.add(Paragraph("um"))
    document.add(Paragraph("dois"))

    assert MarkdownExporter().export(document) == "# Doc\n\num\n\ndois\n"
