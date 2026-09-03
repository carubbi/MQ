# Notebook temporário sem `notebook.yaml`

## Objetivo

Simplificar a geração das aulas em notebook, eliminando o plano intermediário
`notebook.yaml`. O próprio notebook temporário passa a ser o rascunho submetido
à aprovação docente.

## Autoridades

- O cronograma define o encontro, o conteúdo formal e a duração.
- O projeto de ensino define os objetivos da unidade.
- O YAML de curadoria da aula define escopo, tópicos, referências e recursos
  aprovados.
- O notebook público é o material discente final.
- `notebooks/u1_a07.ipynb` é referência de forma e linguagem, não de conteúdo,
  número de seções ou distribuição de tempo.

## Artefatos

O fluxo não cria `notebook.yaml`, schema de notebook ou plano computacional
persistente. Durante a elaboração, usa um `.ipynb` em diretório temporário. O
único artefato público produzido é:

```text
notebooks/<aula-id>.ipynb
```

Não é criada versão em `notebooks/resolvidos/`.

## Fluxo de aprovação

### 1. Estrutura inicial

Gerar o notebook temporário com:

1. cabeçalho institucional canônico;
2. título da aula;
3. objetivos de aprendizagem;
4. agenda provisória.

Os objetivos devem preservar o resultado observável da aula, usar verbos
observáveis e permanecer alinhados aos objetivos conceitual, procedimental e
atitudinal da unidade. Não devem ser uma lista de operações de software.

A agenda propõe as seções substantivas e o tempo de cada uma. Os enunciados
ficam em negrito, a numeração é sequencial e a soma corresponde à duração do
encontro. Elementos de consulta não recebem tempo.

Apresentar objetivos e agenda ao docente e interromper até aprovação.

### 2. Estrutura e fundamentação

Após a primeira aprovação, criar as demais seções Markdown na ordem aprovada e
redigir sua fundamentação a partir das referências selecionadas. A agenda deve
ser atualizada se os títulos ou o escopo das seções mudarem.

Apresentar estrutura e fundamentação ao docente e interromper até nova
aprovação.

### 3. Aplicação computacional

Somente após a aprovação das seções e da fundamentação, incluir células de
código junto das explicações correspondentes. Cada bloco lógico começa por um
comentário curto, imediatamente seguido do código. Blocos distintos na mesma
célula são separados por uma linha vazia.

Código, gráfico, tabela ou resultado que será apenas apresentado pronto deve
ser declarado depois da agenda como não desenvolvido durante o encontro.

### 4. Execução e promoção

Executar todas as células em ordem e rejeitar outputs de erro. Revisar conteúdo,
fórmulas, citações, código, saídas, gráficos, legendas, objetivos e agenda.
Comparar o notebook temporário com a versão pública existente. Promover somente
após aprovação explícita final; qualquer falha preserva a versão anterior.

## Alterações nas skills

### `curar-aula-formal`

Manter o YAML como contrato curricular, sem planejamento de células, código ou
saídas. Encaminhar objetivos, duração, tópicos e referências aprovados para a
geração do notebook.

### `gerar-aula-formal`

Manter apenas o modo `markdown_com_notebook`. No modo `notebook_integral`, não
criar Markdown e encaminhar diretamente à geração do notebook.

### `gerar-notebooks-aula`

- remover toda exigência de `notebook.yaml`;
- remover seu schema, carregador, gerador orientado ao plano e testes associados;
- criar e revisar diretamente o notebook temporário em quatro etapas;
- manter um validador independente de plano para estrutura institucional,
  objetivos, agenda, execução e artefatos incompatíveis;
- exigir validação canônica prévia do YAML de curadoria.

## Validação automatizável

O validador recebe o YAML de curadoria, a raiz do repositório, o cabeçalho
canônico e o notebook. Ele verifica:

- estado aprovado, ID, semestre e duração da aula;
- cabeçalho e título;
- presença de objetivos com ao menos um enunciado;
- presença da agenda, formato dos itens, numeração e soma dos tempos;
- ausência de outputs de erro e execução sequencial das células de código;
- ausência de `aulas/<aula-id>.md` e de cópia resolvida no modo integral.

Alinhamento semântico, suficiência da fundamentação, correspondência entre
agenda e seções, qualidade do código e interpretação dos resultados permanecem
revisões humanas obrigatórias.

## Migração

Arquivos `notebook.yaml` existentes não serão convertidos nem apagados
automaticamente. Quando encontrados, devem ser tratados como legados e sua
remoção exige decisão explícita. A mudança não altera o schema do YAML de
curadoria.

## Critérios de aceite

- nenhuma instrução ativa exige ou gera `notebook.yaml`;
- nenhum código é incluído antes da aprovação da estrutura e fundamentação;
- o notebook temporário contém inicialmente apenas os quatro elementos fixos;
- a agenda fecha a duração canônica sem tempos fixos reutilizados entre aulas;
- a publicação produz um único notebook executado e validado;
- falhas ou ausência de aprovação preservam o notebook público anterior.
