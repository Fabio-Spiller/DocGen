import pytest

from docgen import (
    DocGen,
    DocumentBuilder,
    HtmlExporter,
    MarkdownExporter,
    PlainTextExporter,
)


def sample_document():
    return DocumentBuilder("Relatório").heading("Resumo").paragraph("Tudo certo.").build()


def test_facade_lista_os_formatos_nativos():
    available = DocGen.available_formats()

    assert "html" in available
    assert "markdown" in available
    assert "text" in available


def test_facade_exporta_em_html():
    document = sample_document()

    assert DocGen.export(document, "html") == HtmlExporter().export(document)


def test_facade_exporta_em_markdown():
    document = sample_document()

    assert DocGen.export(document, "markdown") == MarkdownExporter().export(document)


def test_facade_exporta_em_texto_puro():
    document = sample_document()

    assert DocGen.export(document, "text") == PlainTextExporter().export(document)


def test_facade_com_formato_desconhecido_gera_erro_listando_os_disponiveis():
    with pytest.raises(ValueError) as error:
        DocGen.export(sample_document(), "docx")

    message = str(error.value)
    assert "Formato desconhecido: 'docx'" in message
    assert "html" in message
    assert "markdown" in message


def test_facade_save_escreve_o_arquivo(tmp_path):
    document = sample_document()
    path = tmp_path / "relatorio.md"

    DocGen.save(document, "markdown", path)

    assert path.read_text(encoding="utf-8") == MarkdownExporter().export(document)


def test_facade_save_com_formato_desconhecido_nao_cria_arquivo(tmp_path):
    path = tmp_path / "relatorio.xyz"

    with pytest.raises(ValueError):
        DocGen.save(sample_document(), "xyz", path)

    assert not path.exists()


def test_registrar_formato_com_nome_vazio_gera_erro():
    with pytest.raises(ValueError, match="nome do formato"):
        DocGen.register_exporter(" ", MarkdownExporter)
