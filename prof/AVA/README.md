# Estrutura do AVA/Moodle — T199 — 2026.2

## Finalidade

Esta pasta mantém os fragmentos HTML usados nos contêineres do AVA/Moodle de
T199 — Métodos Quantitativos. Os blocos são preparados e validados localmente
antes da cópia manual para o ambiente institucional.

## Fontes

O conteúdo é derivado, nesta ordem, de:

1. cronograma docente canônico;
2. projeto de ensino de 2026;
3. cronograma discente T199-64/65;
4. catálogo de plataformas de exercícios;
5. decisões pedagógicas formalizadas para o AVA.

Datas, conteúdos, avaliações e entregas não devem ser alterados diretamente
nos HTMLs sem atualização prévia da respectiva fonte canônica.

## Inventário

### Blocos comuns

- `apres.html`;
- `bibliografia.html`;
- `contrato.html`;
- `fraude.html`;
- `mat_apoio.html`;
- `metodo.html`;
- `mini_cv.html`;
- `motivacao.html`;
- `plan_ensino.html`;
- `pre-req.html`;
- `recursos.html`;
- `refs.html`;
- `saiba_mais.html`;
- `visao_geral.html`.

### Bloco de avaliação

- `aval_T199-64-65.html`.

Cada contêiner receberá os 14 blocos comuns e o bloco de avaliação da turma.
Não deve existir um `aval.html` genérico.

### Ativo

- `imgs/MQ_bkg.jpg`: imagem de fundo da identidade de Métodos Quantitativos.

## Mapa de publicação

O conjunto atual destina-se às turmas integradas T199-64/65:

- turma 64: `T6CD`, sexta-feira, das 15h30 às 17h10, sala D18;
- turma 65: `T6EF`, sexta-feira, das 17h20 às 19h, sala D18;
- bloco de avaliação: `aval_T199-64-65.html`.

Os códigos das turmas permanecem restritos ao nome interno do bloco de
avaliação, a este mapa e às informações de horário.

## Conteúdo dos blocos

### Identidade e organização

- `apres.html`: boas-vindas e abordagem geral;
- `visao_geral.html`: carga horária, unidades e resultado de aprendizagem;
- `plan_ensino.html`: identificação, ementa, objetivos e conteúdos;
- `pre-req.html`: pré-requisito e conhecimentos recomendados;
- `motivacao.html`: decisões com dados, variabilidade, incerteza e modelagem;
- `mini_cv.html`: identificação acadêmica do professor.

### Regras e avaliações

- `metodo.html`: ciclo didático, ATs, APs, composição e aprovação;
- `contrato.html`: comunicação, frequência, participação e prazos;
- `fraude.html`: integridade acadêmica e uso declarado de IA;
- `aval_T199-64-65.html`: agenda, escopos, entregas e segundas chamadas.

### Materiais e referências

- `bibliografia.html`: bibliografia oficial e periódicos;
- `mat_apoio.html`: materiais semanais, notebooks, apostila, banco de questões
  e dados;
- `recursos.html`: plataformas de exercícios e recursos interativos;
- `refs.html`: referências adicionais;
- `saiba_mais.html`: aprofundamento opcional e não avaliativo.

## Metodologia

O ciclo didático integrado articula:

1. problema e contexto;
2. fundamentação científica;
3. caso reduzido e resolução manual, quando pertinentes;
4. aplicação computacional;
5. comparação, diagnóstico e interpretação.

As APs são desenvolvidas em Python com Jupyter Notebook e utilizam o mesmo
repositório GitHub ao longo das três unidades.

## Avaliação

### Avaliação teórica

- Cada AT vale 10 pontos.
- Cada AT contém dez questões objetivas de mesmo peso, valendo 1 ponto cada.
- A AT1 contém oito questões de análise descritiva e duas de probabilidade.
- As aplicações ocorrem sem consulta no AVA/Moodle com Safe Exam Browser.
- A tolerância para entrada é de 15 minutos após o início.

### Avaliação prática

Cada AP vale 10 pontos:

| Dimensão | Pontos |
| --- | ---: |
| Processo e acompanhamentos | 4 |
| Produto técnico | 4 |
| Interpretação e domínio | 2 |

Os acompanhamentos são formativos e não geram notas isoladas. O conjunto das
evidências subsidia a dimensão processual atribuída no fechamento da AP.

### Composição

`AV = (0,70 × AT) + (0,30 × AP)`.

As APs não possuem segunda chamada.

## Agenda de avaliações e entregas

| Item | Data |
| --- | --- |
| AP1 — acompanhamentos | 28/08 e 04/09 |
| AP1 — acompanhamento final e entrega | 11/09 até 23h59 |
| AT1 — primeira chamada | 18/09 |
| AT1 — segunda chamada | 25/09, `N6CD`, 21h–22h40 |
| AP2 — acompanhamentos | 02/10 e 09/10 |
| AP2 — acompanhamento final | 16/10 |
| AP2 — entrega | 23/10 até 23h59 |
| AT2 — primeira chamada | 23/10 |
| AT2 — segunda chamada | 13/11, `N6CD`, 21h–22h40 |
| AP3 — acompanhamentos | 13/11 e 27/11 |
| AP3 — acompanhamento final e entrega | 04/12 até 23h59 |
| AT3 — primeira chamada | 04/12 |
| AT3 — segunda chamada | 09/12, `N4AB`, 19h–20h40 |

## Materiais públicos

O bloco `mat_apoio.html` publica:

- 16 materiais de aula: um finalizado e 15 em construção;
- 14 notebooks: dois finalizados e 12 em construção;
- três recursos finalizados e 27 recursos em construção no total;
- apostila;
- banco de questões e provas de 2026.2;
- conjuntos de dados didáticos;
- cronograma discente.

## Padrão técnico

- Fragmentos HTML sem `html`, `head` ou `body`;
- hierarquia de títulos iniciada em `h3`;
- ausência de scripts e folhas de estilo;
- estilos inline restritos ao layout do minicurrículo;
- links externos absolutos em HTTPS;
- links externos com `target="_blank"` e
  `rel="noopener noreferrer"`;
- ausência de caminhos locais e de links para materiais internos do professor.

## Fluxo de atualização

1. Atualizar primeiro as fontes canônicas, quando necessário.
2. Adaptar os fragmentos locais.
3. Executar as validações de inventário, conteúdo e links.
4. Conferir a agenda e os escopos das avaliações.
5. Copiar manualmente cada fragmento para o AVA/Moodle.
6. Conferir visualmente o resultado no contêiner publicado.

## Checklist anterior à publicação

- confirmar o semestre 2026.2;
- confirmar T199 — Métodos Quantitativos;
- confirmar turma T199-64/65, horários e sala D18;
- confirmar `AT = 70%` e `AP = 30%`;
- confirmar ATs de 10 pontos, com dez questões de 1 ponto;
- confirmar a rubrica da AP em `4 + 4 + 2`;
- confirmar SEB e tolerância de 15 minutos;
- conferir ATs, APs, acompanhamentos, entregas e segundas chamadas;
- confirmar que as APs não possuem segunda chamada;
- conferir os 16 materiais e 14 notebooks;
- testar todos os links;
- confirmar que todos os links externos usam os atributos de segurança;
- procurar referências a outras disciplinas, conteúdos ou datas legadas;
- confirmar que o minicurrículo e o ativo `MQ_bkg.jpg` permanecem corretos.
