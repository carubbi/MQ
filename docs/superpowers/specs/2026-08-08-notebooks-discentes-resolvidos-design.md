# Publicação dos notebooks finalizados

## Objetivo

Manter três papéis distintos para os notebooks:

- `prof/notebooks/`: fonte canônica e permanente do professor;
- `mat/notebooks/`: notebooks discentes ainda em elaboração;
- `mat/notebooks/resolvidos/`: cópias finalizadas para consulta dos estudantes.

Um notebook docente nunca será movido nem apagado durante a publicação. O
processo apenas copiará versões finalizadas para a pasta discente.

## Convenção de finalização

Um arquivo localizado diretamente em `prof/notebooks/` será considerado
finalizado quando seu nome corresponder integralmente à expressão regular:

```text
^u[1-9][0-9]*_.+\.ipynb$
```

Na prática, o nome deve começar por `u`, seguido do número positivo da unidade
e de `_`. Nomear um notebook segundo esse padrão equivale a autorizar sua
publicação para os estudantes.

Arquivos sem esse prefixo são auxiliares ou permanecem restritos à área do
professor. Atualmente, `examples.ipynb` pertence a essa categoria e não será
publicado.

## Publicação

O script `scripts/publicar_notebooks_resolvidos.py` examinará apenas os arquivos
`.ipynb` diretamente contidos em `prof/notebooks/`. Para cada nome finalizado,
copiará o arquivo para `mat/notebooks/resolvidos/`, preservando o mesmo nome e o
mesmo conteúdo.

A publicação será determinística e idempotente. Uma nova execução sem mudanças
nas fontes não deverá produzir diferenças no Git. O script criará a pasta de
destino quando necessário e nunca excluirá automaticamente arquivos já
publicados.

O processo falhará antes de copiar qualquer arquivo quando:

- um notebook selecionado não contiver JSON válido;
- o nome de destino escapar de `mat/notebooks/resolvidos/`;
- uma referência local `assets/imgs/` estiver presente;
- dois arquivos resultarem no mesmo destino.

## Imagens e portabilidade

Os notebooks docentes finalizados deverão usar URLs absolutas sob:

```text
https://raw.githubusercontent.com/carubbi/MQ/main/mat/notebooks/assets/imgs/
```

Antes da primeira publicação, as referências relativas existentes nas Aulas 1
e 2 serão corrigidas em `prof/notebooks/`. Como a publicação será uma cópia
literal, as versões em `mat/notebooks/resolvidos/` conservarão as mesmas URLs e
funcionarão tanto no Jupyter quanto no Colab, desde que haja acesso à internet.

## Escopo inicial

Os seguintes notebooks satisfazem a convenção e serão publicados inicialmente:

- `u1_s01_fundamentos_estatisticos_aula01.ipynb`;
- `u1_s01_fundamentos_estatisticos_aula02.ipynb`.

`prof/notebooks/examples.ipynb` não satisfaz a convenção e permanecerá apenas
na área docente. Os notebooks existentes diretamente em `mat/notebooks/` não
serão removidos nem sobrescritos pelo processo, pois representam materiais em
elaboração.

## Links públicos

As referências aos dois notebooks finalizados no README principal e nos
cronogramas docente e discente passarão a apontar para
`mat/notebooks/resolvidos/`. Referências a notebooks em elaboração continuarão
apontando para `mat/notebooks/`.

`mat/notebooks/README.md` documentará a diferença entre as pastas, a convenção
de nomes e o comando de publicação.

## Validação

Testes automatizados deverão comprovar:

- seleção de nomes como `u1_...ipynb` e `u12_...ipynb`;
- rejeição de `examples.ipynb`, `unidade1.ipynb`, `u0_teste.ipynb` e arquivos
  fora de `prof/notebooks/`;
- validação JSON antes de qualquer cópia;
- rejeição de referências locais de imagem;
- criação da pasta de destino;
- cópia literal dos notebooks selecionados;
- preservação de arquivos discentes em elaboração;
- idempotência da publicação;
- ausência de `examples.ipynb` em `mat/notebooks/resolvidos/`.

A migração estará concluída quando as Aulas 1 e 2 docentes tiverem URLs
absolutas, suas cópias literais estiverem em `mat/notebooks/resolvidos/`, os
links públicos apontarem para elas e todas as validações passarem.
