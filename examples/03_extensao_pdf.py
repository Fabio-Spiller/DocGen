"""Exemplo 3: o cliente adiciona o formato PDF usando a biblioteca fpdf2.

A DocGen não gera PDF; este arquivo mostra que qualquer desenvolvedor pode
adicionar o formato sem alterar a biblioteca (Open/Closed).

A fpdf2 é dependência só deste exemplo, e não da DocGen. Para rodar:

    pip install fpdf2
    python examples/03_extensao_pdf.py
"""

from pathlib import Path

from fpdf import FPDF

from docgen import DocGen, DocumentBuilder, PlainTextExporter

OUTPUT_DIR = Path(__file__).parent / "saida"
# Courier já vem embutida no PDF, aceita acentos do português e é monoespaçada
# (todas as letras têm a mesma largura), o que mantém as colunas da tabela alinhadas.
PDF_FONT = "Courier"
PDF_FONT_SIZE = 12
PDF_LINE_HEIGHT = 6
FULL_WIDTH = 0  # no fpdf2, largura 0 significa "até a margem direita"


class PdfExporter(PlainTextExporter):
    """Gera um PDF com o mesmo conteúdo do texto puro.

    Herdamos de ``PlainTextExporter`` para reaproveitar todo o texto que ele
    já monta. Só trocamos o ``save``: em vez de gravar um ``.txt``, escrevemos
    o texto dentro de uma página PDF.
    """

    def save(self, document, path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font(PDF_FONT, size=PDF_FONT_SIZE)
        pdf.multi_cell(FULL_WIDTH, PDF_LINE_HEIGHT, self.export(document))
        pdf.output(str(path))


def main():
    report = (
        DocumentBuilder("Relatório de Vendas")
        .heading("Resumo")
        .paragraph("As vendas cresceram neste trimestre.")
        .bullet_list(["Janeiro", "Fevereiro", "Março"])
        .table(headers=["Mês", "Total"], rows=[["Jan", "100"], ["Fev", "150"]])
        .build()
    )

    # Registrado na Facade, o PDF passa a ser usado igual aos formatos nativos.
    DocGen.register_exporter("pdf", PdfExporter)

    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / "relatorio.pdf"
    DocGen.save(report, "pdf", path)
    print(f"PDF salvo em: {path}")


if __name__ == "__main__":
    main()
