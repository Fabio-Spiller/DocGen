"""Exemplo 2: o cliente estende a DocGen sem alterar nenhuma linha da biblioteca.

Este arquivo cria, só com Python puro:

* um formato novo: ``CsvTableExporter``, que exporta as tabelas do documento em CSV;
* um estilo de texto novo: ``Quoted``, que coloca o texto entre aspas.

Isso é o princípio Aberto/Fechado (Open/Closed): a biblioteca está aberta
para extensão (herdando das classes base) e fechada para modificação.

Para rodar:

    python examples/02_extensao_csv.py
"""

import csv
import io
from pathlib import Path

from docgen import BaseExporter, Bold, DocGen, DocumentBuilder, Text, TextDecorator

OUTPUT_DIR = Path(__file__).parent / "saida"
NO_TEXT = ""
CSV_LINE_END = "\n"


class CsvTableExporter(BaseExporter):
    """Exporta apenas as tabelas do documento, no formato CSV.

    Títulos, parágrafos e listas não cabem em CSV, então viram texto vazio.
    Várias tabelas ficam separadas por uma linha em branco.
    """

    def header(self, document):
        return NO_TEXT

    def visit_section(self, section):
        return self.render_children(section)

    def visit_heading(self, heading):
        return NO_TEXT

    def visit_paragraph(self, paragraph):
        return NO_TEXT

    def visit_bullet_list(self, bullet_list):
        return NO_TEXT

    def visit_table(self, table):
        # O módulo csv da biblioteca padrão cuida das vírgulas e aspas dentro das células.
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator=CSV_LINE_END)
        writer.writerow(self.render_cells(table.headers))
        for row in table.rows:
            writer.writerow(self.render_cells(row))
        return buffer.getvalue() + CSV_LINE_END

    def format_text(self, content):
        return content

    def format_bold(self, content):
        return content

    def format_italic(self, content):
        return content

    def format_link(self, content, url):
        return content


class Quoted(TextDecorator):
    """Estilo novo: coloca o texto entre aspas.

    Funciona em qualquer formato (Markdown, HTML, texto puro, CSV...) porque
    só acrescenta aspas em volta do que o texto de dentro já produziu.
    """

    def render(self, exporter):
        return "“" + self.inner.render(exporter) + "”"


def main():
    report = (
        DocumentBuilder("Relatório de Vendas")
        .paragraph(Quoted(Bold(Text("O melhor trimestre do ano"))))
        .table(headers=["Mês", "Total"], rows=[["Jan", "100"], ["Fev", "1,5 mil"]])
        .table(headers=["Vendedor", "Vendas"], rows=[["Ana", "30"], ["Bruno", "25"]])
        .build()
    )

    # O formato novo entra na Facade com uma linha, sem mexer na biblioteca.
    DocGen.register_exporter("csv", CsvTableExporter)

    print("--- CSV (formato do cliente) ---")
    print(DocGen.export(report, "csv"))

    print("--- Markdown (estilo do cliente dentro de um formato nativo) ---")
    print(DocGen.export(report, "markdown"))

    # O formato do cliente também pode ser salvo em arquivo, igual aos nativos.
    OUTPUT_DIR.mkdir(exist_ok=True)
    DocGen.save(report, "csv", OUTPUT_DIR / "tabelas.csv")
    DocGen.save(report, "markdown", OUTPUT_DIR / "extensao.md")
    print(f"Arquivos salvos em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
