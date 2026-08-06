# Grafo de referências da T199 — desenho

**Data:** 6 de agosto de 2026

**Disciplina:** T199 — Métodos Quantitativos

**Estado:** desenho integral com primeira entrega incremental aprovada

## 1. Objetivo

Construir um grafo canônico das referências disponíveis em `prof/refs/`
para localizar conteúdos destinados à futura geração de notebooks de aula,
APs, ATs, exercícios e outros materiais didáticos.

Esses artefatos serão consumidores do grafo. Eles não serão indexados na
primeira versão.

O grafo funcionará como índice de localização e relacionamento. Ele não
substituirá a consulta às páginas originais nem armazenará transcrições
extensas das fontes.

## 2. Estratégia incremental

O objetivo final permanece sendo o mapeamento integral definido nesta
especificação. A primeira entrega, porém, mapeará exclusivamente os conteúdos
curriculares `01.01`, `01.02`, `01.03` e `01.04`.

Não será criado um arquivo separado para a Unidade I. A entrega parcial usará
desde o início os nomes canônicos:

```text
prof/refs/mapas/
├── grafo_referencias.json
├── schema_grafo_referencias.json
└── grafo_referencias.md
```

As nove fontes serão inventariadas na primeira entrega. A curadoria de
capítulos, seções e itens pedagógicos será limitada aos quatro conteúdos
concluídos. As fases posteriores acrescentarão nós e relações aos mesmos
arquivos, sem substituir IDs já publicados.

### 2.1 Cobertura declarada

O grafo parcial deverá declarar sua cobertura em `metadados`:

```json
{
  "cobertura": {
    "estado": "parcial",
    "criterio": "conteudo_curricular",
    "conteudos_concluidos": [
      "01.01",
      "01.02",
      "01.03",
      "01.04"
    ],
    "conteudos_pendentes": [
      "02.01",
      "02.02",
      "02.03",
      "02.04",
      "03.01",
      "03.02",
      "03.03",
      "03.04"
    ],
    "fontes_inventariadas": 9
  }
}
```

O estado somente poderá ser alterado para `completo` após o cumprimento dos
critérios integrais da seção 12.

### 2.2 Regras da primeira entrega

Serão incluídos capítulos, seções, questões e exercícios relacionados a
`01.01`–`01.04`. Itens híbridos cuja resolução dependa materialmente de um
conteúdo pendente serão adiados, pois uma representação parcial do item
produziria relações curriculares enganosas.

Capítulos e seções sem relação com os quatro conteúdos não serão
representados nesta fase. Questões ausentes também não serão classificadas
automaticamente como `fora_do_escopo`.

O valor `fora_do_escopo` poderá ser atribuído apenas a um item efetivamente
examinado durante a busca dos conteúdos da Unidade I. Portanto, uma consulta
vazia fora de `01.01`–`01.04` significará “ainda não mapeado”, e não
“inexistente no corpus”.

O Markdown derivado deverá começar com:

> **Cobertura parcial:** esta versão mapeia somente os conteúdos `01.01` a
> `01.04`. Ausência de resultados para outros conteúdos não indica ausência
> de referências no corpus.

Esta entrega não apoiará as duas questões de `02.01` previstas para a AT1.
Esse limite é consequência explícita da escolha pelo recorte curricular
estrito da Unidade I.

## 3. Corpus

Serão indexados os seguintes PDFs:

```text
prof/refs/
├── apostila/
│   └── banco_questoes_provas_2026_2.pdf
├── exs/
│   └── apostila_mq.pdf
└── livros/
    └── *.pdf
```

A pasta `prof/refs/livros/sumarios/` não será representada como fonte no
grafo. Seus arquivos poderão auxiliar a extração da estrutura editorial,
mas o PDF prevalecerá em qualquer divergência.

## 4. Granularidade

| Tipo de fonte | Cobertura |
| --- | --- |
| Banco de questões | Todas as questões, individualmente |
| Apostila MQ | Todos os capítulos, seções, questões e exercícios |
| Livros | Todos os capítulos e seções |
| Exemplos e exercícios dos livros | Individualizados somente quando já selecionados para a T199 ou usados posteriormente |
| Sumários em Markdown | Apenas insumo auxiliar |

Nos livros, cobertura integral significa que todas as seções serão
localizáveis. Não significa transcrever ou individualizar cada exemplo e
exercício.

Na primeira entrega, a tabela descreve a granularidade final, não a cobertura
imediata. O banco de questões, a apostila e os livros terão somente os nós
relacionados a `01.01`–`01.04`; as demais entradas serão incorporadas nas
fases posteriores.

## 5. Arquitetura

Será adotado um grafo de propriedades em JSON:

```text
fonte
  └── contém → capítulo
                 └── contém → seção
                                ├── aborda → tópico
                                ├── corresponde_a → conteúdo curricular
                                └── contém → item pedagógico
```

Os artefatos serão armazenados em:

```text
prof/refs/mapas/
├── grafo_referencias.json
├── schema_grafo_referencias.json
└── grafo_referencias.md
```

As responsabilidades serão:

- `grafo_referencias.json`: fonte canônica;
- `schema_grafo_referencias.json`: regras estruturais e vocabulários;
- `grafo_referencias.md`: visão humana gerada do JSON.

O Markdown será sempre derivado do JSON e não deverá receber edições
manuais.

## 6. Modelo de dados

O documento canônico terá quatro coleções de nível superior:

```json
{
  "metadados": {},
  "vocabularios": {},
  "nos": [],
  "relacoes": []
}
```

### 6.1 Metadados

`metadados` registrará a versão do esquema, a data de geração, o semestre de
referência e o objeto `cobertura` definido na seção 2.1. A versão permitirá
ampliar o grafo posteriormente sem alterar silenciosamente o significado dos
campos atuais.

### 6.2 Vocabulários

`vocabularios` registrará os valores permitidos para tipos de nós, subtipos,
relações e pertinência à T199. Os valores efetivamente permitidos também
serão validados pelo JSON Schema.

### 6.3 Nós

#### Fonte

Representa cada PDF.

```json
{
  "id": "fonte-barbetta-2010",
  "tipo": "fonte",
  "tipo_fonte": "livro",
  "titulo": "Estatística para cursos de engenharia e informática",
  "arquivo": "prof/refs/livros/Barbetta_2010  Estatística  para cursos de engenharia e informática.pdf",
  "paginas_pdf": 412,
  "idioma": "pt-BR",
  "hash_sha256": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"
}
```

O valor de `hash_sha256` acima é apenas ilustrativo. Na implementação, o
campo receberá o hash calculado do arquivo correspondente para detectar
substituição ou alteração da fonte e exigir nova validação do respectivo
subgrafo.

#### Capítulo

Representa um capítulo formal da fonte.

```json
{
  "id": "barbetta-cap-04",
  "tipo": "capitulo",
  "numero_impresso": "4",
  "titulo": "Probabilidade",
  "pagina_pdf_inicio": 92,
  "pagina_pdf_fim": 116,
  "pagina_impressa_inicio": 91
}
```

#### Seção

Representa uma seção ou subseção.

```json
{
  "id": "barbetta-sec-04-03",
  "tipo": "secao",
  "numero_impresso": "4.3",
  "titulo": "Probabilidade condicional e independência",
  "pagina_pdf_inicio": 103,
  "pagina_pdf_fim": 110,
  "pertinencia_t199": "direta"
}
```

#### Item pedagógico

Representa uma questão, um exercício ou um exemplo individualizado.

```json
{
  "id": "banco-q-0442",
  "tipo": "item_pedagogico",
  "subtipo": "questao",
  "numero_impresso": "442",
  "pagina_pdf": 123,
  "pertinencia_t199": "direta"
}
```

Os enunciados completos não serão armazenados.

#### Tópico

Representa um assunto normalizado.

```json
{
  "id": "topico-probabilidade-condicional",
  "tipo": "topico",
  "nome": "Probabilidade condicional"
}
```

#### Conteúdo curricular

Representa os conteúdos oficiais `01.01` a `03.04` do projeto de ensino.

```json
{
  "id": "conteudo-02-01",
  "tipo": "conteudo_curricular",
  "codigo": "02.01",
  "unidade": "II",
  "nome": "Probabilidade"
}
```

### 6.4 Relações

A primeira versão terá quatro tipos de relação:

| Relação | Finalidade |
| --- | --- |
| `contem` | Registrar a hierarquia editorial |
| `aborda` | Ligar seção ou item a tópico estatístico |
| `corresponde_a` | Ligar seção ou item a conteúdo curricular |
| `precede` | Registrar a ordem entre capítulos, seções ou itens |

Exemplos:

```json
{
  "origem": "banco-q-0442",
  "tipo": "aborda",
  "destino": "topico-probabilidade-condicional"
}
```

```json
{
  "origem": "banco-q-0442",
  "tipo": "corresponde_a",
  "destino": "conteudo-02-01"
}
```

## 7. Pertinência à T199

Os valores permitidos serão:

| Valor | Interpretação |
| --- | --- |
| `direta` | Corresponde explicitamente ao projeto de ensino |
| `indireta` | Serve como pré-requisito, extensão ou contextualização |
| `fora_do_escopo` | Pertence ao corpus, mas não à disciplina |

Toda questão do banco será representada, inclusive quando classificada como
`fora_do_escopo`, ao final do mapeamento integral. Na primeira entrega, essa
regra se aplica somente às questões efetivamente examinadas, conforme a seção
2.2.

## 8. Campos excluídos

Não integrarão o esquema:

```text
dificuldade
observacao
```

Também não serão criados campos genéricos de texto livre para substituir
indiretamente essas duas chaves.

## 9. Conteúdo não armazenado

O grafo não armazenará:

- enunciados completos;
- trechos extensos dos livros;
- soluções ou gabaritos completos;
- imagens extraídas dos PDFs;
- resumos automáticos de cada página;
- ATs, APs, notebooks ou outros artefatos gerados;
- artefatos ainda não criados.

O grafo indicará onde o conteúdo está. A geração futura consultará as páginas
necessárias na fonte original.

## 10. Fluxo de construção

```text
Inventário dos PDFs
        ↓
Identificação e hash das fontes
        ↓
Extração de capítulos, seções e questões
        ↓
Normalização de títulos e páginas
        ↓
Criação dos tópicos
        ↓
Correspondência com 01.01–03.04
        ↓
Classificação de pertinência
        ↓
Validação estrutural e visual
        ↓
Geração do JSON canônico
        ↓
Geração automática do Markdown
```

Cada fase repetirá classificação, validação e geração sobre o mesmo grafo. A
primeira fase filtrará a curadoria por `01.01`–`01.04`; as fases seguintes
ampliarão a cobertura declarada.

## 11. Divergências e falhas de extração

O PDF será sempre a fonte canônica.

Quando o número impresso e a página física divergirem, ambos serão
registrados:

```json
{
  "pagina_pdf": 103,
  "pagina_impressa": 102
}
```

Quando a extração automática falhar:

- a estrutura será verificada visualmente;
- o sumário Markdown poderá auxiliar;
- relações incertas não serão inventadas;
- o nó estrutural continuará existindo mesmo sem correspondência curricular.

A numeração máxima observada no banco não será presumida como quantidade de
questões. A cobertura será reconciliada diretamente com a sequência existente
no PDF.

## 12. Validação

Toda entrega exigirá:

- todos os PDFs previstos registrados;
- IDs únicos e estáveis;
- todas as relações apontando para nós existentes;
- páginas e intervalos dentro dos limites de cada PDF;
- códigos curriculares restritos a `01.01`–`03.04`;
- valores de pertinência pertencentes ao vocabulário;
- ausência das chaves `dificuldade` e `observacao`;
- ausência de enunciados extensos;
- Markdown reproduzível integralmente a partir do JSON;
- verificação visual de amostras de cada fonte curada.

A primeira entrega exigirá adicionalmente:

- `cobertura.estado` igual a `parcial`;
- `conteudos_concluidos` contendo exatamente `01.01`–`01.04`;
- `conteudos_pendentes` contendo exatamente `02.01`–`03.04`;
- nove fontes inventariadas;
- somente relações curriculares com `01.01`–`01.04`;
- ausência de itens híbridos dependentes de conteúdos pendentes;
- aviso de cobertura parcial no início do Markdown.

A conclusão do mapeamento integral exigirá:

- todos os capítulos e seções dos livros representados;
- todas as questões do banco representadas;
- todas as questões e exercícios da apostila representados;
- `conteudos_concluidos` contendo `01.01`–`03.04`;
- `conteudos_pendentes` vazio;
- `cobertura.estado` igual a `completo`.

## 13. Consultas obrigatórias

A primeira entrega deverá permitir responder:

- quais referências abordam fundamentos estatísticos;
- quais páginas correspondem ao conteúdo `01.01`;
- quais fontes tratam de organização e representação de dados;
- quais seções tratam de análise univariada;
- quais itens tratam de análise bivariada;
- quais referências podem ser consultadas para produzir um notebook sobre
  `01.01`, `01.02`, `01.03` ou `01.04`;
- qual é a cobertura declarada e quais conteúdos permanecem pendentes.

O grafo integral deverá permitir responder também:

- quais referências abordam probabilidade condicional;
- quais páginas correspondem ao conteúdo `02.01`;
- quais questões do banco estão fora do escopo da T199;
- quais fontes tratam de regressão linear múltipla;
- quais seções tratam de estimação intervalar;
- quais itens combinam mais de um conteúdo curricular;
- quais referências podem ser consultadas para produzir um notebook sobre
  `03.04`.

## 14. Extensão futura

Uma versão posterior poderá acrescentar nós para notebooks, ATs, APs, listas
de exercícios e materiais de aula, com relações como:

```text
utiliza_referencia
derivado_de
avalia
produz_evidencia_de
```

Essa extensão reutilizará os IDs estáveis das referências. Ela não faz parte
da primeira versão e não deve ser antecipada no mapeamento inicial.

## 15. Limite da próxima etapa

Após a aprovação desta versão da especificação, o plano integral existente
será substituído por um plano prioritário da Unidade I. O novo plano deverá
detalhar infraestrutura definitiva, inventário das nove fontes, curadoria de
`01.01`–`01.04`, validação da cobertura parcial e geração dos três artefatos
previstos.

As Unidades II e III deverão receber planos posteriores que ampliem o mesmo
grafo e preservem os IDs publicados na primeira entrega.

A aprovação desta especificação não autoriza, por si só, a criação ou
alteração de ATs, APs, notebooks ou documentos do AVA.
