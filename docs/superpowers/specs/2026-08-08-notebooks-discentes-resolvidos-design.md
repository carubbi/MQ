# Organização dos notebooks finalizados

## Objetivo

Separar os notebooks por estágio e manter apenas uma cópia de cada arquivo:

- `prof/notebooks/`: notebooks auxiliares ou docentes ainda não promovidos;
- `mat/notebooks/`: notebooks discentes ainda em elaboração;
- `mat/notebooks/resolvidos/`: localização canônica dos notebooks finalizados.

Quando um notebook docente for finalizado, ele será movido de
`prof/notebooks/` para `mat/notebooks/resolvidos/`. Não será mantida uma cópia
adicional em `prof/notebooks/`.

## Convenção de finalização

Somente arquivos localizados diretamente em `prof/notebooks/` e cujo nome
corresponda integralmente à expressão regular abaixo serão movidos:

```text
^u[1-9][0-9]*_.+\.ipynb$
```

Na prática, o nome deve começar por `u`, seguido do número positivo da unidade
e de `_`. Arquivos sem esse prefixo não serão movidos.

Atualmente, os arquivos selecionados são:

- `u1_s01_fundamentos_estatisticos_aula01.ipynb`;
- `u1_s01_fundamentos_estatisticos_aula02.ipynb`.

`prof/notebooks/examples.ipynb` não satisfaz a convenção e permanecerá em sua
localização atual.

## Movimentação

Os dois notebooks selecionados serão movidos com preservação do histórico do
Git para `mat/notebooks/resolvidos/`, conservando os nomes originais. A pasta de
destino será criada durante a mudança.

Nenhum notebook localizado diretamente em `mat/notebooks/` será removido,
movido ou sobrescrito. Esses arquivos continuarão representando materiais em
elaboração, mesmo quando houver um notebook homônimo em `resolvidos/`.

Não será criado script de sincronização ou publicação. Para futuros notebooks,
a promoção para finalizado será uma movimentação explícita, revisada no Git.

## Imagens e portabilidade

Antes da movimentação, as referências relativas das Aulas 1 e 2 serão
substituídas por URLs absolutas sob:

```text
https://raw.githubusercontent.com/carubbi/MQ/main/mat/notebooks/assets/imgs/
```

Assim, os notebooks finalizados funcionarão no Jupyter e no Colab sem depender
da localização do diretório de execução, desde que haja acesso à internet.

## Links públicos

As referências às Aulas 1 e 2 no README principal e nos cronogramas docente e
discente serão atualizadas para `mat/notebooks/resolvidos/`. Referências a
notebooks ainda em elaboração continuarão apontando para `mat/notebooks/`.

`mat/notebooks/README.md` documentará a diferença entre a raiz e
`resolvidos/`, bem como a convenção usada para promover notebooks docentes.

## Validação

A mudança será validada pelas seguintes condições:

- os dois notebooks selecionados contêm JSON válido;
- os dois arquivos existem em `mat/notebooks/resolvidos/`;
- eles não existem mais em `prof/notebooks/`;
- `prof/notebooks/examples.ipynb` permanece inalterado;
- nenhum outro notebook de `prof/notebooks/` é movido;
- os notebooks em elaboração de `mat/notebooks/` permanecem inalterados;
- não restam referências locais `assets/imgs/` nos notebooks resolvidos;
- os links públicos apontam para arquivos existentes;
- `git diff --check` não apresenta erros.
