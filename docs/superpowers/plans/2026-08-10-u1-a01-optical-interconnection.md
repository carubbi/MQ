# Optical Interconnection Network na Aula 1 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adaptar somente a Aula 1 da Unidade I para apresentar e inspecionar o arquivo bruto do Optical Interconnection Network.

**Architecture:** O Markdown manterá os três ciclos didáticos existentes, mas substituirá o contexto, os casos reduzidos, o código e as interpretações do Internet Firewall Data pelo Optical Interconnection Network. O arquivo oficial será lido sem limpeza: as 15 colunas carregadas, as dez variáveis documentadas e os problemas estruturais permanecerão visíveis para retomada na aula de pré-processamento.

**Tech Stack:** Markdown, Python, pandas, CSV compactado do UCI Machine Learning Repository.

## Global Constraints

- Modificar somente `aulas/u1_a01_ambientacao_dados.md`.
- Não modificar notebook, Aula 2, cronograma ou outros materiais.
- Preservar duração, resultado de aprendizagem, três ciclos didáticos e ausência de exercício adicional.
- Carregar o arquivo oficial com `sep=";"`, `decimal=","` e `compression="zip"`.
- Não selecionar, excluir, renomear, converter ou corrigir colunas e valores nesta aula.
- Usar somente linhas do arquivo oficial nos casos reduzidos; apenas `ID*` poderá ser acrescentado para localização.
- Usar `*`, nunca `†`, para marcar conteúdo acrescentado ou inferido.
- Distinguir dez variáveis documentadas das 15 colunas efetivamente carregadas.
- Identificar unidades inferidas como inferências justificadas.
- Não interpretar `Channel Utilization > 1` como proporção válida.
- Não criar commit da Aula 1 antes da aprovação específica do usuário sobre o arquivo adaptado.

---

### Task 1: Substituir o contexto e o ciclo de reconhecimento dos dados

**Files:**
- Modify: `aulas/u1_a01_ambientacao_dados.md:30-149`

**Interfaces:**
- Consumes: especificação `docs/superpowers/specs/2026-08-10-u1-a01-optical-interconnection-design.md` e arquivo oficial UCI 449.
- Produces: contexto, dicionário, leitura dos valores, caso reduzido, carregamento bruto e interpretação estrutural usados pelo Ciclo 3.

- [ ] **Step 1: Substituir o contexto recorrente e o carregamento**

Remover toda a apresentação de firewall, portas e NAT. Apresentar 640 medições
de desempenho de configurações simuladas de uma rede óptica multiprocessada e
usar exatamente este carregamento:

```python
import pandas as pd

url_rede = (
    "https://archive.ics.uci.edu/static/public/449/"
    "optical%2Binterconnection%2Bnetwork.zip"
)
rede = pd.read_csv(
    url_rede,
    compression="zip",
    sep=";",
    decimal=",",
)
```

Explicar que cada linha representa uma medição de desempenho de uma
configuração simulada, não um nó, pacote ou thread individual.

- [ ] **Step 2: Inserir o dicionário com unidade na segunda coluna**

Usar a ordem `Variável no arquivo | Unidade | Descrição documentada` e incluir,
sem omissões:

```text
Node Number | nós | número de nós: 16 para 4×4 e 64 para 8×8
Thread Number | threads por nó | número inicial de threads em cada nó
Spatial Distribution | não se aplica | modelo espacial do tráfego
Temporal Distribution | não se aplica | modelo temporal de geração dos pacotes
T/R | adimensional | razão entre tempo de transferência T e execução R
Processor Utilization[espaço final] | proporção 0–1** | tempo com threads em execução
Channel Waiting Time | ciclos de relógio* | espera média na fila do canal de saída
Input Waiting Time | ciclos de relógio* | espera média até atendimento pelo processador
Network Response Time | ciclos de relógio* | tempo médio entre requisição e resposta
Channel Utilization | proporção 0–1** | tempo com o canal ocupado
```

Definir `UN`, `HR`, `BR`, `PS`, `Client-Server` e `Asynchronous`. Manter as duas
notas: `*` para a inferência dos ciclos e `**` para a leitura das utilizações
como proporções, embora a documentação use a palavra percentual.

- [ ] **Step 3: Inserir a leitura de valores e a interpretação conjunta**

Criar `### Como interpretar os valores` com a tabela aprovada na especificação,
incluindo exemplos para as dez variáveis. Criar em seguida
`### Como interpretar as métricas conjuntamente` e relacionar:

```text
Processor Utilization ↔ Input Waiting Time
Channel Utilization ↔ Channel Waiting Time
esperas e utilizações ↔ Network Response Time
```

Explicar que utilização elevada com espera elevada pode indicar saturação e que
utilização baixa com espera baixa pode representar baixa demanda. Registrar que
as métricas são médias da simulação e que utilizações acima de 1 não receberão
interpretação proporcional.

- [ ] **Step 4: Substituir o caso reduzido por quatro linhas do arquivo**

Usar as quatro primeiras linhas e uma projeção com estas colunas e valores:

```text
ID* | Node Number | Thread Number | Spatial Distribution | Temporal Distribution | T/R | Network Response Time
1   | 64          | 4             | UN                   | Client-Server         | 0,1 | 700,514102
2   | 64          | 4             | UN                   | Client-Server         | 0,2 | 864,599227
3   | 64          | 4             | UN                   | Client-Server         | 0,3 | 839,372851
4   | 64          | 4             | UN                   | Client-Server         | 0,4 | 1256,053108
```

Declarar que `ID*` não pertence ao dataset e que quatro linhas exibidas não
representam toda a distribuição.

- [ ] **Step 5: Atualizar a aplicação, comparação e diagnóstico do Ciclo 2**

Usar:

```python
dimensoes = rede.shape
nomes_colunas = rede.columns.tolist()

print("Linhas e colunas:", dimensoes)
print("Colunas:", nomes_colunas)
```

Registrar o resultado `(640, 15)`, explicar que apenas dez colunas são
documentadas e que cinco colunas vazias decorrem da estrutura bruta do CSV.
Comparar afirmações equivalentes a:

```text
“Há 640 nós.” → não sustentada
“Há 640 medições de desempenho.” → compatível
“Cada linha representa um pacote.” → não sustentada
“O arquivo carregado contém 15 colunas.” → compatível com o CSV bruto
“A documentação descreve dez variáveis.” → compatível com a fonte
```

- [ ] **Step 6: Verificar o primeiro bloco**

Run:

```bash
sed -n '/## Contexto recorrente/,/### Ciclo didático 3/p' aulas/u1_a01_ambientacao_dados.md | rg -n "Firewall|firewall|NAT|Source Port|Destination Port|Bytes Sent|pkts_sent"
```

Expected: nenhuma ocorrência.

Run:

```bash
rg -n "Optical Interconnection|640, 15|Node Number|Thread Number|Spatial Distribution|Temporal Distribution|T/R|Processor Utilization|Channel Waiting Time|Input Waiting Time|Network Response Time|Channel Utilization" aulas/u1_a01_ambientacao_dados.md
```

Expected: todas as variáveis e as dimensões brutas aparecem no arquivo.

---

### Task 2: Adaptar a inspeção computacional, os cuidados e as referências

**Files:**
- Modify: `aulas/u1_a01_ambientacao_dados.md:151-257`

**Interfaces:**
- Consumes: objeto `rede` e definições produzidos pela Task 1.
- Produces: inspeção computacional coerente, limitações, materiais e referência final da Aula 1.

- [ ] **Step 1: Substituir o caso reduzido de tipos computacionais**

Usar uma tabela com as previsões:

```text
Node Number | 64, 16 | inteiro
Spatial Distribution | UN, HR, BR, PS | texto
T/R | 0,1; 0,2; 0,3 | ponto flutuante
Network Response Time | 700,514102; 864,599227 | ponto flutuante
```

Explicar que tipo computacional não determina sozinho o tipo estatístico nem a
unidade da variável.

- [ ] **Step 2: Atualizar o código e a leitura das inspeções**

Usar operações separadas:

```python
primeiros_registros = rede.head()
tipos_computacionais = rede.dtypes
valores_distintos = rede.nunique()

print(primeiros_registros)
print(tipos_computacionais)
print(valores_distintos)
```

Registrar como resultados esperados:

```text
Node Number: 2 valores distintos
Thread Number: 4
Spatial Distribution: 4
Temporal Distribution: 2
T/R: 10
Processor Utilization : 624
Channel Waiting Time: 640
Input Waiting Time: 640
Network Response Time: 640
Channel Utilization: 627
cinco colunas vazias: 0 valores não ausentes distintos
```

Mencionar que os nomes das cinco colunas vazias são atribuídos pelo pandas no
padrão `Unnamed: ...` e que `Processor Utilization ` preserva o espaço final.

- [ ] **Step 3: Atualizar diagnóstico e erros comuns**

Preservar o quadro que distingue `shape`, `columns`, `head()`, `dtypes` e
`nunique()`. Substituir os cuidados do firewall por:

```text
confundir medição com nó, pacote ou thread;
ignorar separador de campos e separador decimal;
tratar as 15 colunas carregadas como 15 variáveis documentadas;
remover colunas vazias ou corrigir nomes silenciosamente;
interpretar utilização acima de 1 como proporção válida;
concluir qualidade ou representatividade apenas por head() e dtypes.
```

Manter explícito que a correção ocorrerá somente na aula de qualidade e
pré-processamento.

- [ ] **Step 4: Atualizar materiais e referência**

Substituir o link do firewall por:

```markdown
[Optical Interconnection Network — UCI](https://archive.ics.uci.edu/dataset/449/optical%2Binterconnection%2Bnetwork)
```

Substituir a referência final por:

```markdown
- UCI MACHINE LEARNING REPOSITORY. *Optical Interconnection Network*. 2015.
  DOI: [10.24432/C5J60X](https://doi.org/10.24432/C5J60X).
```

Não alterar as demais referências, o vínculo com a apostila, o banco de
questões ou a declaração de ausência de exercício adicional.

- [ ] **Step 5: Validar o arquivo contra a especificação e o CSV**

Run:

```bash
rg -n '[[:blank:]]+$' aulas/u1_a01_ambientacao_dados.md
```

Expected: nenhuma saída.

Run:

```bash
rg -n "Internet Firewall|C5131M|NAT|Source Port|Action|Bytes|Packets" aulas/u1_a01_ambientacao_dados.md
```

Expected: nenhuma ocorrência.

Run:

```bash
rg -n "C5J60X|640, 15|cinco colunas|Como interpretar os valores|Como interpretar as métricas conjuntamente|ciclos de relógio|proporção" aulas/u1_a01_ambientacao_dados.md
```

Expected: todos os elementos obrigatórios aparecem.

Run:

```bash
unzip -p /tmp/optical_network.zip optical_interconnection_network.csv | sed -n '1,5p'
```

Expected: cabeçalho oficial e as quatro linhas usadas no caso reduzido.

- [ ] **Step 6: Apresentar a Aula 1 para aprovação**

Mostrar o arquivo alterado, o resumo das verificações e `git status --short`.
Não modificar o notebook nem iniciar a Aula 2. Não adicionar ou criar commit da
Aula 1 antes da aprovação específica do usuário.
