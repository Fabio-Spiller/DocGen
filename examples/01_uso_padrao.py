"""Exemplo 1: uso padrão da DocGen, só com o que já vem pronto na biblioteca.

Para rodar (na raiz do projeto, depois de ``pip install -e .``):

    python examples/01_uso_padrao.py
"""

from pathlib import Path

from docgen import Bold, DocGen, DocumentBuilder, Italic, Link, MarkdownExporter, Text

OUTPUT_DIR = Path(__file__).parent / "saida"


def build_report():
    """Monta o documento com o Builder, encadeando as chamadas."""
    return (
        DocumentBuilder("Relatório de Vendas")
        .heading("Resumo")
        .paragraph("As vendas cresceram neste trimestre.")
        .paragraph(Bold(Text("Meta atingida!")))
        .section("Detalhes")
        .bullet_list(["Janeiro", "Fevereiro", Italic(Text("Março (parcial)"))])
        .table(headers=["Mês", "Total"], rows=[["Jan", "100"], ["Fev", "150"]])
        .end_section()
        .paragraph(Link(Text("Ver painel completo"), "https://exemplo.com/painel"))
        .build()
    )


def main():
    report = build_report()

    # Jeito 1: pela Facade, escolhendo o formato pelo nome.
    print(DocGen.export(report, "text"))

    # Jeito 2: usando um exportador diretamente, sem a Facade.
    print(MarkdownExporter().export(report))

    # Salvando em arquivos: a Facade escolhe o exportador e grava o arquivo.
    OUTPUT_DIR.mkdir(exist_ok=True)
    DocGen.save(report, "html", OUTPUT_DIR / "relatorio.html")
    DocGen.save(report, "markdown", OUTPUT_DIR / "relatorio.md")
    DocGen.save(report, "text", OUTPUT_DIR / "relatorio.txt")
    print(f"Arquivos salvos em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
