import pytest

from docgen import (
    BulletList,
    Document,
    Element,
    Heading,
    Link,
    Paragraph,
    Section,
    Table,
    Text,
)


def test_secao_guarda_os_filhos_na_ordem_em_que_foram_adicionados():
    section = Section("Introdução")
    first = Paragraph("primeiro")
    second = Paragraph("segundo")

    section.add(first)
    section.add(second)

    assert section.children == [first, second]


def test_secao_e_paragrafo_sao_tratados_como_element():
    # Composite: o grupo (seção) e a folha (parágrafo) têm o mesmo tipo base.
    assert isinstance(Section("Grupo"), Element)
    assert isinstance(Paragraph("folha"), Element)


def test_documento_pode_conter_secao_que_contem_elementos():
    document = Document("Relatório")
    section = Section("Resumo")
    section.add(Paragraph("texto"))
    document.add(section)

    assert document.children[0].children[0].content.content == "texto"


def test_documento_sem_titulo_gera_erro():
    with pytest.raises(ValueError, match="título do documento"):
        Document("   ")


def test_secao_sem_titulo_gera_erro():
    with pytest.raises(ValueError, match="título da seção"):
        Section("")


@pytest.mark.parametrize("level", [0, 7])
def test_titulo_com_nivel_fora_de_1_a_6_gera_erro(level):
    with pytest.raises(ValueError, match="nível do título"):
        Heading("Título", level)


def test_lista_vazia_gera_erro():
    with pytest.raises(ValueError, match="pelo menos um item"):
        BulletList([])


def test_tabela_sem_cabecalho_gera_erro():
    with pytest.raises(ValueError, match="pelo menos uma coluna"):
        Table(headers=[], rows=[])


def test_tabela_com_linha_de_tamanho_errado_gera_erro():
    with pytest.raises(ValueError, match="2 células"):
        Table(headers=["A", "B"], rows=[["só uma"]])


def test_texto_vazio_gera_erro():
    with pytest.raises(ValueError, match="texto não pode ser vazio"):
        Text("")


def test_link_sem_endereco_gera_erro():
    with pytest.raises(ValueError, match="endereço do link"):
        Link(Text("site"), "")


def test_string_comum_vira_text_automaticamente():
    paragraph = Paragraph("olá")

    assert isinstance(paragraph.content, Text)
    assert paragraph.content.content == "olá"
