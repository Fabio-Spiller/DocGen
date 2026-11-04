from docgen import (
    Bold,
    BulletList,
    Document,
    Heading,
    HtmlExporter,
    Italic,
    Link,
    Paragraph,
    Section,
    Table,
    Text,
)


def html_page(body: str, title: str = "Doc") -> str:
    """Página HTML esperada, com o ``body`` informado no meio."""
    return (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head>\n"
        '<meta charset="utf-8">\n'
        f"<title>{title}</title>\n"
        "</head>\n"
        "<body>\n"
        f"<h1>{title}</h1>\n"
        f"{body}"
        "</body>\n"
        "</html>\n"
    )


def export_with(element) -> str:
    document = Document("Doc")
    document.add(element)
    return HtmlExporter().export(document)


def test_html_exporta_pagina_completa_com_titulo():
    assert HtmlExporter().export(Document("Doc")) == html_page("")


def test_html_exporta_titulo_com_tag_do_nivel():
    assert export_with(Heading("Resumo", level=3)) == html_page("<h3>Resumo</h3>\n")


def test_html_exporta_paragrafo_com_tag_p():
    assert export_with(Paragraph("Olá")) == html_page("<p>Olá</p>\n")


def test_html_exporta_lista_com_ul_e_li():
    expected = html_page("<ul>\n<li>a</li>\n<li>b</li>\n</ul>\n")
    assert export_with(BulletList(["a", "b"])) == expected


def test_html_exporta_tabela_com_th_no_cabecalho_e_td_nos_dados():
    table = Table(headers=["Mês", "Total"], rows=[["Jan", "100"]])

    expected = html_page(
        "<table>\n"
        "<tr><th>Mês</th><th>Total</th></tr>\n"
        "<tr><td>Jan</td><td>100</td></tr>\n"
        "</table>\n"
    )
    assert export_with(table) == expected


def test_html_exporta_secao_com_tag_section():
    section = Section("Resumo")
    section.add(Paragraph("texto"))

    expected = html_page("<section>\n<h2>Resumo</h2>\n<p>texto</p>\n</section>\n")
    assert export_with(section) == expected


def test_html_exporta_estilos_de_texto():
    assert export_with(Paragraph(Bold(Text("x")))) == html_page("<p><strong>x</strong></p>\n")
    assert export_with(Paragraph(Italic(Text("x")))) == html_page("<p><em>x</em></p>\n")
    assert export_with(Paragraph(Link(Text("site"), "https://x.com"))) == html_page(
        '<p><a href="https://x.com">site</a></p>\n'
    )


def test_html_escapa_caracteres_especiais_do_texto():
    paragraph = Paragraph(Bold(Text("<script> & \"aspas\"")))

    expected = html_page("<p><strong>&lt;script&gt; &amp; &quot;aspas&quot;</strong></p>\n")
    assert export_with(paragraph) == expected


def test_html_escapa_titulo_do_documento_e_da_secao():
    document = Document("A & B")
    document.add(Section("<C>"))

    expected = html_page("<section>\n<h2>&lt;C&gt;</h2>\n</section>\n", title="A &amp; B")
    assert HtmlExporter().export(document) == expected
