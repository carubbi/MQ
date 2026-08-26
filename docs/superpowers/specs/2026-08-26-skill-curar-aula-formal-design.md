# Skill `curar-aula-formal` — desenho

**Data:** 26 de agosto de 2026

**Estado:** desenho aprovado; aguardando revisão da especificação escrita

## 1. Objetivo

Criar uma skill privada para orientar e tornar reproduzível a curadoria de cada
aula estatística formal, desde a delimitação do encontro até a aprovação do
manifesto de seleção. A skill deverá reduzir trabalho repetitivo sem transferir
para automação as decisões curriculares e bibliográficas do docente.

A skill será instalada em:

```text
~/.codex/skills/curar-aula-formal/
```

Ela operará sobre os artefatos privados de cada aula:

```text
.interno/prof/aulas/<semestre>/<aula-id>/
├── selecao.yaml
└── dossie.md
```

O manifesto YAML continuará sendo a fonte canônica. O dossiê continuará sendo
uma representação derivada e regenerável, apresentada por listas, sem tabelas.

## 2. Escopo

A skill compreenderá duas fases internas do mesmo fluxo:

1. **Preparação da curadoria:** identificar a aula no cronograma docente,
   delimitar seu escopo, consultar o grafo, ler as páginas originais, criar ou
   atualizar o manifesto e renderizar o dossiê.
2. **Apoio à decisão:** recomendar estados de tópicos e referências, seus
   papéis, compatibilizações e a partição da aula em ciclos conceituais; depois
   registrar somente as decisões aprovadas pelo docente.

A skill não gerará a aula pública. Essa responsabilidade pertencerá, em etapa
posterior, a uma skill separada, `gerar-aula-formal`, que aceitará apenas um
manifesto aprovado.

Também ficam fora do escopo:

- selecionar tópicos ou referências sem confirmação docente;
- alterar o grafo silenciosamente para acomodar uma aula;
- inferir conteúdo teórico apenas dos metadados do grafo;
- criar ou modificar notebooks;
- gerar código, pseudocódigo ou instruções computacionais para a aula;
- publicar arquivos sob `.interno/` ou incluí-los no Git;
- impor quantidade fixa de ciclos a encontros de 100 minutos.

## 3. Decisões arquiteturais

Será criada uma única skill de curadoria, e não uma skill para o dossiê e outra
para os ciclos. As duas atividades compartilham as mesmas autoridades, estados
e decisões e precisam ser avaliadas em conjunto. A separação ocorrerá por
fases e pontos de parada internos, evitando duplicação de regras.

A skill será uma camada de orquestração e julgamento assistido. Os scripts do
repositório continuarão responsáveis pelas operações determinísticas:

- validar o contrato e a semântica de `selecao.yaml`;
- conferir IDs, relações e páginas contra o grafo;
- renderizar `dossie.md` sem modificar o manifesto;
- rejeitar um manifesto inconsistente ou prematuramente aprovado.

A skill poderá recomendar e editar o manifesto durante a colaboração, mas não
substituirá o docente como autoridade da seleção. Toda passagem para o estado
geral `aprovado` exigirá confirmação explícita.

## 4. Autoridades e precedência

A skill consultará as autoridades nesta ordem funcional:

1. projeto de ensino e cronograma docente, para conteúdo, resultado de
   aprendizagem, data, duração e limites do encontro;
2. planejamentos da unidade, para progressão, pré-requisitos e conteúdos
   reservados;
3. grafo de referências, para localizar fontes candidatas;
4. páginas originais, para comprovar cobertura, notação, divergências, exemplos
   e exercícios;
5. convenção matemática global, para harmonizar a exposição;
6. manifesto da aula, para conservar candidatos, evidências e decisões.

O cronograma delimita a aula; o grafo não amplia seu escopo. O grafo localiza
fontes; as páginas originais sustentam a análise. O manifesto aprovado encerra
a curadoria daquela versão e limita a futura geração da aula.

## 5. Política de referências

A recomendação avaliará primeiro a adequação da cobertura, não apenas o idioma
ou a existência de uma menção. Entre obras com cobertura suficiente, livros em
português terão preferência para `fundamentacao`.

A apostila será usada como referência de conteúdo somente quando os livros não
cobrirem adequadamente o assunto. Ela não substituirá automaticamente uma
fundamentação teórica mais completa.

Quando não houver livro em português com cobertura suficiente, um livro em
inglês poderá cumprir o papel de `fundamentacao`. Nesse caso, a skill deverá:

- consultar diretamente o original;
- propor tradução técnica em português;
- harmonizar terminologia e notação com a disciplina;
- preservar fonte, edição e páginas originais;
- registrar as decisões em `compatibilizacao.observacao`;
- não apresentar a formulação resultante como tradução oficial.

Livros em inglês também poderão ser complementares a uma fundamentação em
português quando acrescentarem precisão, distinções conceituais, contrapontos
ou exemplos pertinentes.

## 6. Estados e decisões

### 6.1 Tópicos

A skill recomendará:

- `selecionado` quando o tópico for necessário ao resultado de aprendizagem e
  couber na profundidade e no tempo do encontro;
- `adiado` quando for pertinente, mas pertencer melhor a aula ou unidade
  posterior;
- `rejeitado` quando for irrelevante, redundante ou inadequado ao escopo;
- `pendente` somente quando faltar uma decisão ou evidência verificável.

`pendente` é um estado transitório e nunca será aceito em um manifesto
`aprovado`.

### 6.2 Referências

Cada referência candidata será `selecionada`, `rejeitada` ou `pendente`. Uma
referência selecionada receberá um ou mais papéis permitidos pelo contrato. Um
tópico selecionado exigirá ao menos uma referência de `fundamentacao`.

A recomendação deverá justificar rejeições relevantes, sobretudo quando uma
fonte for apenas indireta, excessivamente avançada, terminologicamente
incompatível ou insuficiente para fundamentar o conceito.

### 6.3 Manifesto

O manifesto permanecerá `em_selecao` enquanto houver tópico ou referência
pendente, enquanto os ciclos não estiverem definidos ou enquanto faltar uma
`aplicacao_notebook`. Não haverá estado próprio em cada ciclo.

Somente após validação estrutural, curricular, bibliográfica e temporal, e
após confirmação docente, o estado geral passará para `aprovado`.

## 7. Definição dos ciclos

Cada ciclo será um bloco conceitual coerente e preservará o campo
`ciclos[].topicos`. Um ID de tópico ou de referência não equivale a um ciclo.
Vários tópicos poderão integrar o mesmo ciclo quando responderem à mesma
questão conceitual e puderem compartilhar formalização, exemplo, interpretação
e evidência de aprendizagem.

Um novo ciclo será recomendado quando ocorrer ao menos uma mudança relevante
de:

- objeto conceitual;
- resultado parcial de aprendizagem;
- notação, condições ou pressupostos;
- exemplo estruturante;
- interpretação ou limitação;
- evidência esperada na aplicação do notebook.

A skill deverá evitar tanto a fragmentação artificial quanto a concentração de
conceitos incompatíveis em um único bloco.

## 8. Complexidade e viabilidade temporal

Não haverá quantidade padrão nem limite fixo de ciclos para 100 minutos. A
quantidade decorrerá da menor partição conceitual coerente que caiba no tempo
disponível.

Para cada ciclo candidato $j$, a skill estimará uma duração mínima
$t_j^{\min}$ a partir da novidade conceitual, formalização, pressupostos,
exemplo, interpretação e aplicação. A partição será viável somente quando:

$$
\sum_{j=1}^{k} t_j^{\min}
\leq
T_{\text{aula}}-T_{\text{abertura}}-T_{\text{fechamento}}.
$$

As faixas seguintes serão usadas apenas como calibração, nunca como regra de
contagem:

- baixa complexidade: aproximadamente 12 a 15 minutos;
- complexidade moderada: aproximadamente 18 a 25 minutos;
- alta complexidade: aproximadamente 25 a 35 minutos.

Um ciclo que ultrapasse a faixa de alta complexidade deverá ser dividido ou
ter parte de seu conteúdo adiada. Se a soma não couber na aula, a skill deverá
recomendar redução de profundidade, adiamento ou redistribuição, e não a mera
compressão do tempo.

Para tornar essa análise auditável, a implementação atualizará o contrato do
manifesto de `1.0` para `1.1`. O novo objeto de nível superior
`planejamento_tempo` registrará `abertura_minutos` e `fechamento_minutos`. Cada
ciclo acrescentará `complexidade`, `duracao_minima_minutos` e
`justificativa_particao`, preservando `ciclos[].topicos` e sem introduzir estado
por ciclo.

O validador calculará o tempo disponível a partir de `aula.duracao_minutos` e
rejeitará o manifesto quando a soma das durações mínimas dos ciclos o exceder.
A migração do manifesto da Aula 2 conservará todos os tópicos, referências e
decisões existentes; acrescentará somente os novos campos temporais.

## 9. Referência de calibração: Aula 2

A Aula 2 confirma a metodologia, mas não define um molde para outras aulas.
Considerando 5 minutos de abertura e 10 de fechamento, permanecem 85 minutos
para os ciclos:

1. investigação estatística e variabilidade — complexidade moderada, 20
   minutos;
2. estatística descritiva e inferencial — complexidade baixa, 15
   minutos;
3. população, amostra, unidade de análise e unidade de observação —
   complexidade alta, 25 minutos;
4. amostragem, representatividade, vieses e generalização — complexidade alta,
   25 minutos.

A soma das durações mínimas é 85 minutos. Quatro ciclos são viáveis porque o
escopo exclui técnicas detalhadas de amostragem, tamanho amostral, margem de
erro, distribuições amostrais e inferência probabilística formal. Três ciclos
concentrariam conceitos demais; cinco somente seriam justificados por maior
profundidade ou por uma aplicação independente.

## 10. Aplicação no notebook

Cada ciclo deverá conter exatamente uma `aplicacao_notebook`, com o mesmo ID do
ciclo correspondente no notebook. A skill recomendará somente objetivo,
pergunta, contraste, evidência e vínculo.

Não serão incluídos código, pseudocódigo, bibliotecas, funções, comandos,
células, sequências de implementação ou resultados inventados. A subseção da
aula será intitulada `Aplicação no notebook`.

## 11. Fluxo operacional

### 11.1 Preparação

Ao receber semestre e ID da aula, a skill deverá:

1. localizar o encontro no cronograma docente canônico;
2. declarar conteúdo, resultado, duração, escopo e reservas;
3. consultar o grafo pelos conteúdos e tópicos pertinentes;
4. ler as páginas originais das referências candidatas;
5. registrar cobertura, páginas, notação e divergências no manifesto;
6. validar o manifesto em estado `em_selecao`;
7. renderizar o dossiê exclusivamente a partir do YAML;
8. parar e apresentar ao docente as decisões pendentes.

### 11.2 Apoio à decisão

Depois de receber escolhas ou um pedido de recomendação, a skill deverá:

1. classificar tópicos e referências segundo as regras aprovadas;
2. recomendar papéis e compatibilizações;
3. propor a partição conceitual mínima;
4. estimar e testar a viabilidade temporal;
5. recomendar uma aplicação de notebook para cada ciclo;
6. explicar riscos, adiamentos e alternativas relevantes;
7. registrar somente decisões confirmadas;
8. regenerar o dossiê e validar novamente o manifesto;
9. solicitar confirmação separada antes de marcar `aprovado`.

O docente poderá escolher livremente uma ou mais referências compatíveis. A
skill deverá aceitar essa decisão quando o contrato continuar válido e deverá
alertar, de forma direta, quando a escolha causar lacuna de fundamentação,
incompatibilidade ou excesso de escopo.

## 12. Falhas e segurança

Qualquer uma das condições seguintes interromperá o avanço do estado, sem
apagar nem substituir o manifesto:

- aula ausente ou ambígua no cronograma;
- fonte ou página original indisponível;
- ID sem correspondência no grafo;
- referência que não aborde o tópico ou o conteúdo curricular;
- tópico selecionado sem fundamentação;
- tradução ou notação não compatibilizada;
- tópico ou referência pendente;
- ausência de ciclos ou de aplicação correspondente;
- partição conceitual incompatível com o tempo disponível;
- tentativa de aprovar sem confirmação docente.

Mensagens de erro deverão indicar aula, campo ou ciclo afetado e uma ação
corretiva. A skill não restaurará arquivos removidos nem incluirá alterações
alheias do worktree em seus commits.

## 13. Componentes da skill

O pacote privado conterá apenas os recursos necessários:

```text
~/.codex/skills/curar-aula-formal/
├── SKILL.md
└── references/
    ├── criterios-estados.md
    ├── politica-referencias.md
    └── ciclos-e-tempo.md
```

`SKILL.md` descreverá gatilhos, sequência operacional, pontos de parada,
comandos do repositório e invariantes. Os arquivos de referência concentrarão
critérios que precisem ser consultados durante a respectiva fase. Não serão
duplicados schemas, scripts, PDFs ou dados do grafo dentro da skill.

## 14. Verificação

A implementação deverá ser verificada com cenários representativos:

- nova aula com candidatos inicialmente pendentes;
- seleção com múltiplas referências compatíveis;
- preferência por livro em português com cobertura suficiente;
- fundamentação inglesa traduzida quando a cobertura em português for
  insuficiente;
- apostila usada apenas como referência de conteúdo;
- tópico selecionado sem fundamentação, que deve bloquear a aprovação;
- três partições alternativas, das quais apenas uma é conceitualmente coerente
  e temporalmente viável;
- aula cuja complexidade exija mais de quatro ciclos;
- aula cujo escopo precise ser reduzido para caber em 100 minutos;
- regeneração do dossiê sem alteração do YAML;
- tentativa de aprovar sem todas as aplicações de notebook;
- preservação de arquivos privados fora do rastreamento do Git.

Os testes determinísticos permanecerão no repositório. A própria skill será
avaliada por cenários de uso e pela qualidade de suas decisões, sem transformar
o julgamento pedagógico em uma regra textual rígida.

## 15. Critérios de aceite

A skill estará pronta quando:

- reproduzir o fluxo da Aula 2 em uma nova aula sem copiar decisões específicas
  dela;
- consultar cronograma, grafo e páginas originais nas funções corretas;
- manter o YAML como fonte canônica e o dossiê como derivação legível;
- recomendar estados com justificativas acionáveis;
- respeitar a política linguística e de compatibilização;
- definir ciclos por coerência e complexidade, não por contagem fixa;
- demonstrar a viabilidade temporal antes da aprovação;
- preservar `ciclos[].topicos` e a correspondência com o notebook;
- interromper-se nos pontos de decisão docente;
- não gerar a aula pública nem conteúdo computacional;
- não rastrear nenhum artefato sob `.interno/`.
