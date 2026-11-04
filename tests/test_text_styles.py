from docgen import Bold, HtmlExporter, Italic, Link, MarkdownExporter, Text, TextComponent


def test_negrito_com_italico_combinados_em_markdown():
    styled = Bold(Italic(Text("importante")))

    assert styled.render(MarkdownExporter()) == "***importante***"


def test_negrito_com_italico_combinados_em_html():
    styled = Bold(Italic(Text("importante")))

    assert styled.render(HtmlExporter()) == "<strong><em>importante</em></strong>"


def test_link_com_texto_em_negrito_em_html():
    styled = Link(Bold(Text("site")), "https://exemplo.com")

    assert styled.render(HtmlExporter()) == '<a href="https://exemplo.com"><strong>site</strong></a>'


def test_ordem_dos_decorators_muda_a_ordem_das_marcas():
    exporter = HtmlExporter()

    assert Bold(Italic(Text("x"))).render(exporter) == "<strong><em>x</em></strong>"
    assert Italic(Bold(Text("x"))).render(exporter) == "<em><strong>x</strong></em>"


def test_decorators_sao_text_component():
    # Por terem a mesma interface, um estilo pode envolver outro estilo.
    assert isinstance(Bold(Text("x")), TextComponent)
    assert isinstance(Text("x"), TextComponent)
