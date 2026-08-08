# Versões discentes e resolvidas dos notebooks

## Objetivo

Manter duas apresentações de cada notebook didático:

- `mat/notebooks/<nome>.ipynb`: versão discente, com espaços de resposta vazios;
- `mat/notebooks/resolvidos/<nome>.ipynb`: versão canônica, com respostas e códigos preenchidos.

A versão resolvida será a única editada manualmente. A versão discente será
gerada por script para impedir divergências de enunciados, imagens, metadados e
correções.

## Escopo inicial

A migração inicial abrangerá somente notebooks que já tenham respostas reais.
Atualmente, isso inclui `u1_s01_fundamentos_estatisticos_aula01.ipynb`: sua
versão discente está em `mat/notebooks/` e sua versão completa está em
`prof/notebooks/`. Ambas possuem 62 células com IDs correspondentes. A Aula 2
possui células de resposta vazias, e os notebooks posteriores possuem apenas o
cabeçalho; por isso, eles permanecerão apenas na raiz até receberem conteúdo
resolvido.

Não serão criadas cópias vazias dentro de `resolvidos/`, pois isso comunicaria
incorretamente que existe um gabarito disponível.

## Marcação das respostas

As células que contêm respostas receberão a tag de metadados `solution` na
versão canônica. Cada uma também armazenará sua apresentação discente em
`metadata.mq.student_source`. Esse campo será uma lista de linhas, no mesmo
formato de `source`, e poderá ser vazio quando a resposta discente deva ser uma
célula completamente vazia.

Durante a geração da versão discente:

- células com a tag `solution` terão `source` substituído pelo conteúdo de
  `metadata.mq.student_source`;
- em células de código `solution`, `outputs` serão esvaziados e
  `execution_count` será definido como `null`;
- células sem a tag serão copiadas sem alteração;
- a tag `solution` e o campo `metadata.mq` serão retirados das células geradas
  para não expor respostas ou detalhes editoriais aos estudantes.

Enunciados em células próprias devem permanecer sem a tag. Quando uma célula de
código combinar comentário-guia e resposta, o comentário será preservado em
`student_source` e apenas a implementação será omitida da versão discente.

## Gerador

O script `scripts/gerar_notebooks_discentes.py` receberá um notebook resolvido
ou processará todos os arquivos em `mat/notebooks/resolvidos/`. Para cada fonte,
gravará a versão discente de mesmo nome diretamente em `mat/notebooks/`.

O script falhará sem sobrescrever o destino quando:

- o arquivo não for um notebook JSON válido;
- o notebook resolvido não contiver nenhuma célula `solution`;
- uma célula `solution` não possuir `metadata.mq.student_source` válido;
- o destino calculado escapar de `mat/notebooks/`;
- houver colisão de nomes durante uma execução em lote.

A geração será determinística: executar novamente sem alterar a fonte não deve
produzir diferenças no Git.

## Imagens e portabilidade

As duas versões conservarão as URLs absolutas em
`raw.githubusercontent.com/carubbi/MQ/main/mat/notebooks/assets/imgs/`. O
gerador não copiará imagens nem reintroduzirá caminhos relativos, de modo que os
notebooks continuem utilizáveis no Jupyter e no Colab.

## Documentação

`mat/notebooks/README.md` explicará:

- qual pasta contém cada versão;
- que `resolvidos/` é a fonte canônica;
- como marcar células de resposta;
- como executar o gerador;
- que arquivos resolvidos no mesmo repositório são publicamente acessíveis.

As referências discentes existentes no README principal e no cronograma
continuarão apontando para `mat/notebooks/<nome>.ipynb`.

## Relação com `prof/notebooks`

A versão completa da Aula 1 em `prof/notebooks/` fornecerá as respostas para a
migração inicial. A versão discente atual em `mat/notebooks/` fornecerá os
`student_source`, os textos atualizados e as URLs externas. A associação será
feita pelo `id` de cada célula, e a migração falhará se a sequência de IDs ou os
tipos das células não forem compatíveis.

Os arquivos em `prof/notebooks/` não serão apagados nesta etapa, pois o
diretório também contém materiais que não são duplicatas diretas. Uma limpeza
posterior deverá ser decidida separadamente.

## Validação

Testes automatizados deverão cobrir, no mínimo:

- substituição da resposta pelo `student_source`;
- limpeza de outputs e contador de execução em células de código `solution`;
- remoção dos metadados privados `solution` e `metadata.mq`;
- preservação de células sem resposta, IDs e metadados relevantes;
- rejeição de notebook sem tag `solution`;
- rejeição de célula `solution` sem `student_source` válido;
- geração determinística;
- validação JSON dos notebooks de origem e destino;
- ausência de referências locais `assets/imgs/` nas versões geradas.

A migração será considerada concluída quando a Aula 1 resolvida estiver na nova
pasta, sua versão discente for reproduzível pelo script e as validações acima
passarem.
