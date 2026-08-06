# Grafo de referências da T199 — desenho

**Data:** 6 de agosto de 2026

**Disciplina:** T199 — Métodos Quantitativos

**Estado:** desenho aprovado para formalização

## 1. Objetivo

Construir um grafo canônico das referências disponíveis em `prof/refs/`
para localizar conteúdos destinados à futura geração de notebooks de aula,
APs, ATs, exercícios e outros materiais didáticos.

Esses artefatos serão consumidores do grafo. Eles não serão indexados na
primeira versão.

O grafo funcionará como índice de localização e relacionamento. Ele não
substituirá a consulta às páginas originais nem armazenará transcrições
extensas das fontes.

## 2. Corpus

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

## 3. Granularidade

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

## 4. Arquitetura

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

## 5. Modelo de dados

O documento canônico terá quatro coleções de nível superior:

```json
{
  "metadados": {},
  "vocabularios": {},
  "nos": [],
  "relacoes": []
}
```

### 5.1 Metadados

`metadados` registrará a versão do esquema, a data de geração, o semestre de
referência e a cobertura do corpus. A versão permitirá ampliar o grafo
posteriormente sem alterar silenciosamente o significado dos campos atuais.

### 5.2 Vocabulários

`vocabularios` registrará os valores permitidos para tipos de nós, subtipos,
relações e pertinência à T199. Os valores efetivamente permitidos também
serão validados pelo JSON Schema.

### 5.3 Nós

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

### 5.4 Relações

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

## 6. Pertinência à T199

Os valores permitidos serão:

| Valor | Interpretação |
| --- | --- |
| `direta` | Corresponde explicitamente ao projeto de ensino |
| `indireta` | Serve como pré-requisito, extensão ou contextualização |
| `fora_do_escopo` | Pertence ao corpus, mas não à disciplina |

Toda questão do banco será representada, inclusive quando classificada como
`fora_do_escopo`.

## 7. Campos excluídos

Não integrarão o esquema:

```text
dificuldade
observacao
```

Também não serão criados campos genéricos de texto livre para substituir
indiretamente essas duas chaves.

## 8. Conteúdo não armazenado

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

## 9. Fluxo de construção

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

## 10. Divergências e falhas de extração

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

## 11. Validação

A conclusão do mapeamento exigirá:

- todos os PDFs previstos registrados;
- IDs únicos e estáveis;
- todas as relações apontando para nós existentes;
- páginas e intervalos dentro dos limites de cada PDF;
- todos os capítulos e seções dos livros representados;
- todas as questões do banco representadas;
- todas as questões e exercícios da apostila representados;
- códigos curriculares restritos a `01.01`–`03.04`;
- valores de pertinência pertencentes ao vocabulário;
- ausência das chaves `dificuldade` e `observacao`;
- ausência de enunciados extensos;
- Markdown reproduzível integralmente a partir do JSON;
- verificação visual de amostras de cada fonte.

## 12. Consultas obrigatórias

O desenho deverá permitir responder:

- quais referências abordam probabilidade condicional;
- quais páginas correspondem ao conteúdo `02.01`;
- quais questões do banco estão fora do escopo da T199;
- quais fontes tratam de regressão linear múltipla;
- quais seções tratam de estimação intervalar;
- quais itens combinam mais de um conteúdo curricular;
- quais referências podem ser consultadas para produzir um notebook sobre
  `03.04`.

## 13. Extensão futura

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

## 14. Limite da próxima etapa

Após a aprovação desta especificação será produzido um plano de
implementação. O plano deverá detalhar extração, normalização, classificação,
validação e geração dos três artefatos previstos.

A aprovação desta especificação não autoriza, por si só, a criação ou
alteração de ATs, APs, notebooks ou documentos do AVA.
