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
Atualmente, isso inclui `u1_s01_fundamentos_estatisticos_aula01.ipynb`. A Aula 2
possui células de resposta vazias, e os notebooks posteriores possuem apenas o
cabeçalho; por isso, eles permanecerão apenas na raiz até receberem conteúdo
resolvido.

Não serão criadas cópias vazias dentro de `resolvidos/`, pois isso comunicaria
incorretamente que existe um gabarito disponível.

## Marcação das respostas

As células que contêm respostas receberão a tag de metadados `solution` na
versão canônica.

Durante a geração da versão discente:

- células de código com a tag `solution` terão `source`, `outputs` e
  `execution_count` limpos, mas a célula vazia será preservada como espaço de
  trabalho;
- células Markdown com a tag `solution` serão removidas integralmente;
- células sem a tag serão copiadas sem alteração;
- a tag `solution` será retirada das células geradas para não expor detalhes
  editoriais desnecessários aos estudantes.

Enunciados e orientações devem permanecer em células sem a tag. Uma célula não
deve misturar enunciado e resposta.

## Gerador

O script `scripts/gerar_notebooks_discentes.py` receberá um notebook resolvido
ou processará todos os arquivos em `mat/notebooks/resolvidos/`. Para cada fonte,
gravará a versão discente de mesmo nome diretamente em `mat/notebooks/`.

O script falhará sem sobrescrever o destino quando:

- o arquivo não for um notebook JSON válido;
- o notebook resolvido não contiver nenhuma célula `solution`;
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

Os arquivos existentes em `prof/notebooks/` serão usados apenas como evidência
de comparação durante a migração inicial. Eles não serão apagados nesta etapa,
pois o diretório também contém materiais que não são duplicatas diretas. Uma
limpeza posterior deverá ser decidida separadamente.

## Validação

Testes automatizados deverão cobrir, no mínimo:

- limpeza de código, outputs e contador de execução em células `solution`;
- remoção de respostas Markdown;
- preservação de células sem resposta, IDs e metadados relevantes;
- rejeição de notebook sem tag `solution`;
- geração determinística;
- validação JSON dos notebooks de origem e destino;
- ausência de referências locais `assets/imgs/` nas versões geradas.

A migração será considerada concluída quando a Aula 1 resolvida estiver na nova
pasta, sua versão discente for reproduzível pelo script e as validações acima
passarem.
