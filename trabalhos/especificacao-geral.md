# Avaliação prática integrada — Ames Housing

## Finalidade

As avaliações práticas das três unidades constituem etapas distintas de uma investigação estatística com o Ames Housing:

- AP1: organizar e explorar os dados;
- AP2: auditar a adequação de um modelo probabilístico;
- AP3: ajustar, interpretar, comparar e diagnosticar modelos de regressão.

Cada etapa será entregue e avaliada separadamente. Os notebooks guiados das aulas servem como referências de método e comunicação, mas não deverão ser copiados ou concatenados para formar as APs.

## Organização dos grupos

- O trabalho será realizado em duplas.
- Será admitido um trio somente quando a quantidade de estudantes impedir a formação exclusiva de duplas.
- Recomenda-se a continuidade dos integrantes nas três unidades.
- Mudanças de composição poderão ocorrer com autorização do professor em caso de incompatibilidade, desistência, alteração de matrícula ou outra situação justificada.
- As decisões e os produtos já desenvolvidos permanecerão vinculados ao projeto, mesmo quando houver mudança na composição do grupo.
- Cada grupo receberá uma característica qualitativa $B$ diferente.
- No início da AP2, cada grupo receberá uma variável ou um evento e um modelo candidato entre Binomial, Poisson e Normal.
- Na AP3, cada grupo reutilizará a característica $B$ preparada na AP1 e definirá sua categoria de referência antes da modelagem.
- Todos os integrantes deverão compreender e conseguir explicar as decisões estatísticas e computacionais.

## Base de dados obrigatória

O professor fornecerá o arquivo bruto original do Ames Housing. Não será fornecida uma versão previamente limpa, com nomes de colunas padronizados ou com tratamentos definidos.

O artigo de referência e o dicionário dos dados deverão ser consultados durante a investigação:

- artigo: <https://jse.amstat.org/v19n3/decock.pdf>.

Somente o arquivo fornecido pelo professor poderá ser utilizado. Qualquer substituição dependerá de autorização prévia.

O grupo deverá registrar:

- identificação e procedência do arquivo fornecido;
- procedimento de importação;
- nomes originais das colunas utilizadas;
- eventual normalização dos nomes e respectivo mapeamento;
- decisões de conversão e tratamento;
- consulta ao artigo e ao dicionário oficial.

## Continuidade entre as APs

Ao final da AP1, serão congelados:

- código de importação;
- mapeamento dos nomes;
- tratamento dos valores ausentes;
- agrupamento da característica $B$;
- rótulos finais;
- estrutura organizada dos dados.

No início da AP3, o grupo indicará a categoria de referência de $B$ com base em significado e interpretabilidade, antes do exame dos resultados da regressão. As AP2 e AP3 não deverão repetir a análise exploratória completa. Qualquer alteração das decisões da AP1 dependerá de autorização e justificativa do professor.

Se uma etapa anterior estiver incompleta, o professor poderá fornecer somente os parâmetros mínimos que evitem o bloqueio da etapa seguinte. Esse procedimento não modificará a nota anterior nem fornecerá respostas da AP atual.

## Repositório e produtos

Cada grupo manterá um único repositório GitHub para as três APs, com a seguinte estrutura mínima:

```text
README.md
requirements.txt
.gitignore
data/
  raw/
  processed/
notebooks/
  ap1.ipynb
  ap2.ipynb
  ap3.ipynb
```

O `README.md` deverá identificar o projeto e os integrantes, explicar sua estrutura, indicar como preparar o ambiente e descrever como executar os notebooks. O repositório deverá utilizar caminhos relativos, registrar as dependências necessárias, excluir arquivos temporários e credenciais por meio do `.gitignore` e manter um histórico de commits coerente com o desenvolvimento do trabalho.

Os dados brutos deverão ser preservados em `data/raw/`. Dados gerados pelo grupo poderão ser armazenados em `data/processed/`, desde que seu processo de obtenção seja reproduzível.

Os notebooks serão salvos diretamente em `notebooks/`, nos caminhos `notebooks/ap1.ipynb`, `notebooks/ap2.ipynb` e `notebooks/ap3.ipynb`.

Cada notebook começará com:

1. uma célula Markdown com o conteúdo institucional de [cabeçalho institucional da Aula 1](../notebooks/u1_a01.ipynb);
2. uma célula Markdown com o título principal da AP.

O desenvolvimento será organizado por seções e por células curtas. Cada célula de código terá uma finalidade analítica identificável e, quando produzir uma evidência relevante, será seguida por uma célula Markdown com interpretação. Carregamento, preparação, análise, visualização e modelagem não deverão ser reunidos em uma única célula com aparência de script.

Tabelas e figuras científicas relevantes deverão receber legendas e interpretações específicas no padrão:

- `**Tabela X - Descrição.** Interpretação da evidência apresentada.`
- `**Figura X - Descrição.** Interpretação da evidência apresentada.`

Cada notebook deverá:

- executar integralmente, do início ao fim, sem estado oculto;
- utilizar caminhos de dados reproduzíveis;
- apresentar previsões ou justificativas antes dos resultados computacionais;
- apresentar de forma rastreável os resultados computacionais solicitados;
- interpretar tabelas, gráficos e saídas no contexto;
- explicitar unidades, pressupostos e limitações;
- identificar os integrantes e suas contribuições;
- declarar o uso de inteligência artificial.

## Entrega

O grupo entregará pelo AVA somente o link do repositório GitHub até 23h59, no horário de Fortaleza, nas datas do [cronograma da turma](../ensino/cronograma_2026_2_t199_64_65.md): AP1 em 11/09/2026, AP2 em 23/10/2026 e AP3 em 04/12/2026. A versão avaliada será a correspondente ao último commit realizado até esse horário.

As APs são atividades práticas desenvolvidas com acompanhamento processual ao longo de cada unidade e não terão segunda chamada. A versão entregue no prazo definido será a versão avaliada.

O repositório poderá ser público ou privado, mas o professor deverá ter acesso antes do encerramento do prazo. O mesmo link será utilizado nas três unidades. O acompanhamento formativo não substitui a submissão final.

## Uso de inteligência artificial

O notebook deverá conter:

```markdown
## Declaração de uso de inteligência artificial
```

Quando houver uso, o grupo informará a ferramenta ou o modelo, a finalidade, as etapas afetadas e como verificou o conteúdo. Quando não houver, deverá declarar essa condição. Os estudantes permanecem integralmente responsáveis por código, análise, referências e conclusões.

## Princípios de avaliação

- Correção estatística e interpretação terão prioridade sobre sofisticação do código.
- Código executado sem justificativa ou interpretação não constituirá evidência suficiente.
- Decisões orientadas apenas à obtenção de significância ou melhor ajuste serão penalizadas.
- Resultados inesperados não serão penalizados quando o método e a análise forem corretos.
- A atribuição de causalidade não será aceita em uma análise observacional.
