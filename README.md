# DocGen

**DocGen** é uma biblioteca Python para montar documentos por código e exportá-los em vários formatos (texto puro, Markdown e HTML).
Você descreve o documento uma única vez (títulos, parágrafos, listas, tabelas) e escolhe o formato de saída só no final, sem reescrever nada.
A biblioteca também é fácil de estender: dá para criar formatos, elementos e estilos novos sem alterar o código dela.

Trabalho acadêmico da disciplina de Design Patterns (PUCPR).

## Equipe

- Fabio Henrique Spiller Veloso
- Lucas Gabriel Nunes dos Santos
- Vinícius Wamser Gogoglla

## Vídeo

TODO: link do YouTube

## Instalação

Requer Python 3.10 ou mais novo. A biblioteca não tem dependências: usa só a biblioteca padrão.

```bash
pip install -e .
```

Para rodar os testes:

```bash
pip install -e ".[dev]"
pytest
```

## Uso rápido

```python
from docgen import Bold, DocGen, DocumentBuilder, Italic, Link, Text

doc = (
    DocumentBuilder("Relatório de Vendas")
    .heading("Resumo")
    .paragraph("As vendas cresceram neste trimestre.")
    .paragraph(Bold(Text("Meta atingida!")))
    .section("Detalhes")
    .bullet_list(["Janeiro", "Fevereiro", Italic(Text("Março"))])
    .table(headers=["Mês", "Total"], rows=[["Jan", "100"], ["Fev", "150"]])
    .end_section()
    .paragraph(Link(Text("Ver painel"), "https://exemplo.com"))
    .build()
)

html = DocGen.export(doc, "html")             # devolve uma str
DocGen.save(doc, "markdown", "relatorio.md")  # grava em arquivo
```

Formatos prontos: `"text"`, `"markdown"` e `"html"`. Use `DocGen.available_formats()` para ver a lista.

Também dá para usar um exportador diretamente, sem a fachada:

```python
from docgen import MarkdownExporter

markdown = MarkdownExporter().export(doc)
```

### O que vem pronto

| Tipo | Classes |
|------|---------|
| Elementos | `Document`, `Section`, `Heading`, `Paragraph`, `BulletList`, `Table` |
| Estilos de texto | `Text`, `Bold`, `Italic`, `Link` (podem ser combinados: `Bold(Italic(Text("x")))`) |
| Exportadores | `PlainTextExporter`, `MarkdownExporter`, `HtmlExporter` |
| Montagem | `DocumentBuilder` (`heading`, `paragraph`, `bullet_list`, `table`, `section`, `end_section`, `add`, `build`) |
| Entrada simples | `DocGen` (`export`, `save`, `register_exporter`, `available_formats`) |

Em qualquer lugar que recebe texto, você pode passar uma `str` comum ou um texto com estilo.

## Como estender (sem alterar a biblioteca)

### Novo formato de saída

Crie uma subclasse de `BaseExporter` e implemente o cabeçalho, os métodos `visit_*` (um por elemento) e os `format_*` (um por estilo). Depois registre o formato com um nome:

```python
from docgen import BaseExporter, DocGen

class OutlineExporter(BaseExporter):
    def header(self, document):
        return f"[{document.title}]\n"

    def visit_section(self, section):
        return f"+ {section.title}\n" + self.render_children(section)

    def visit_heading(self, heading):
        return f"  # {heading.text.render(self)}\n"

    def visit_paragraph(self, paragraph):
        return "  (parágrafo)\n"

    def visit_bullet_list(self, bullet_list):
        return f"  (lista com {len(bullet_list.items)} itens)\n"

    def visit_table(self, table):
        return f"  (tabela com {len(table.rows)} linhas)\n"

    def format_text(self, content):
        return content

    def format_bold(self, content):
        return content

    def format_italic(self, content):
        return content

    def format_link(self, content, url):
        return content

DocGen.register_exporter("outline", OutlineExporter)
DocGen.export(doc, "outline")
```

Para só ajustar um formato existente, herde dele. Por exemplo, para adicionar um rodapé:

```python
from docgen import MarkdownExporter

class SignedMarkdownExporter(MarkdownExporter):
    def footer(self, document):
        return "---\nGerado pela DocGen\n"
```

### Novo elemento

Crie uma subclasse de `Element` e implemente `accept`. O jeito mais simples é montar o elemento novo a partir dos que já existem. Assim ele funciona em todos os formatos:

```python
from docgen import Bold, DocumentBuilder, Element, Paragraph, Text

class Alert(Element):
    def __init__(self, message):
        self.message = message

    def accept(self, visitor):
        return Paragraph(Bold(Text("Aviso: " + self.message))).accept(visitor)

doc = DocumentBuilder("Doc").add(Alert("prazo amanhã")).build()
```

### Novo estilo de texto

Crie uma subclasse de `TextDecorator` e implemente `render`:

```python
from docgen import Bold, Text, TextDecorator

class Quoted(TextDecorator):
    def render(self, exporter):
        return "“" + self.inner.render(exporter) + "”"

Quoted(Bold(Text("frase de efeito")))
```

### Exemplos completos

A pasta [examples/](examples/) tem scripts de cliente usando a biblioteca:

- [01_uso_padrao.py](examples/01_uso_padrao.py): uso com o que já vem pronto.
- [02_extensao_csv.py](examples/02_extensao_csv.py): formato CSV e estilo `Quoted` criados pelo cliente.
- [03_extensao_pdf.py](examples/03_extensao_pdf.py): formato PDF criado pelo cliente com a `fpdf2` (rode `pip install fpdf2` antes).

## Padrões de projeto

| Padrão | Onde | Para quê |
|--------|------|----------|
| Composite | [elements/base.py](src/docgen/elements/base.py), [elements/document.py](src/docgen/elements/document.py) | Tratar um elemento sozinho e um grupo de elementos do mesmo jeito. |
| Builder | [builder.py](src/docgen/builder.py) | Montar o documento passo a passo, com chamadas encadeadas. |
| Visitor | [exporters/base.py](src/docgen/exporters/base.py) (`visit_*`) + `accept` nos elementos | Criar formatos novos sem mexer nas classes dos elementos. |
| Template Method | [exporters/base.py](src/docgen/exporters/base.py) (`export`) | Fixar o roteiro da exportação: cabeçalho → elementos → rodapé. |
| Decorator | [elements/text.py](src/docgen/elements/text.py) | Combinar estilos de texto sem uma classe para cada combinação. |
| Facade | [facade.py](src/docgen/facade.py) | Esconder a escolha do exportador e a escrita do arquivo. |
