# Fundamentos estatísticos e investigação com dados

- **Disciplina:** T199 — Métodos Quantitativos
- **Unidade:** I
- **Semana:** 1
- **Data:** 07/08/2026
- **Conteúdos formais:** `01.01`
- **Tópicos:** Investigação estatística; Estatística descritiva; Estatística inferencial; População; Amostra; Amostragem; Representatividade; Unidade de análise; Tipos de variáveis
- **Resultado de aprendizagem:** identificar a estrutura de um conjunto de dados, formular uma pergunta estatística e delimitar o alcance das conclusões a partir da origem dos registros.

---

## Pergunta orientadora

> O que representa cada registro de um conjunto de dados e até onde as conclusões obtidas podem ser generalizadas?

Responder exige mais do que executar código. É necessário relacionar:

- a pergunta formulada;
- a origem dos registros;
- a unidade de análise;
- as variáveis disponíveis;
- a população de interesse;
- o processo que produziu a amostra.

---

## Conceitos e definições

### Estatística e investigação

A Estatística organiza métodos para formular perguntas, obter dados, representar a variabilidade, analisar evidências e comunicar conclusões com suas limitações.

Uma investigação estatística pode ser organizada em seis movimentos:

1. delimitar o problema;
2. formular uma pergunta respondível;
3. definir população, unidade de análise e variáveis;
4. obter ou reconhecer a origem dos dados;
5. analisar a variabilidade e os padrões;
6. comunicar a conclusão e seu alcance.

> **Material da disciplina:** [Banco de questões, questões 1, 4 e 5, pp. 7–8](../apostila/banco_questoes_provas_2026_2.pdf#page=7)

---

### Fonte, registro e unidade de análise

- **Fonte:** origem documentada dos dados.
- **Registro ou observação:** linha que reúne informações sobre uma unidade.
- **Unidade de análise:** entidade à qual as variáveis de um registro se referem.
- **Variável:** característica observada ou calculada para cada unidade.
- **Valor:** realização registrada de uma variável em determinada unidade.

Uma linha não é automaticamente uma pessoa, um dispositivo ou um evento. Seu significado depende do processo que gerou o conjunto.

> **Fonte pública:** [Portal Brasileiro de Dados Abertos — conjuntos de dados e metadados](https://dados.gov.br/)
>
> **Material da disciplina:** [Apostila, conceitos fundamentais, pp. 9–10](../apostila/apostila_mq.pdf#page=9)

---

### População, censo, amostra e amostragem

- **População:** conjunto de unidades sobre o qual se pretende responder à pergunta.
- **Censo:** observação de todas as unidades da população definida.
- **Amostra:** subconjunto efetivamente observado.
- **Amostragem:** processo de seleção das unidades.
- **Quadro amostral:** representação operacional das unidades que poderiam ser selecionadas.

A população precisa ser declarada. “Todos os atendimentos” e “os atendimentos registrados por determinado serviço durante um período definido” representam populações diferentes.

> **Fonte pública:** [IBGE — Censo Demográfico 2022: população-alvo e metodologia](https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html)
>
> **Material da disciplina:** [Apostila, população e amostra, pp. 8–9](../apostila/apostila_mq.pdf#page=8)

---

### Descrição e inferência

- **Estatística descritiva:** resume e representa os registros observados.
- **Estatística inferencial:** utiliza dados amostrais e um modelo para avaliar características de uma população ou processo.

Uma descrição correta da amostra não garante uma inferência válida para uma população mais ampla.

| Pergunta | Natureza |
| --- | --- |
| Qual foi o tempo mediano entre os registros disponíveis? | Descritiva |
| Qual é o tempo mediano de todos os atendimentos da população-alvo? | Inferencial |
| Como os tempos variam entre os grupos registrados? | Descritiva |
| A diferença observada pode ser generalizada para outro serviço ou período? | Inferencial |

> **Fonte pública:** [SIDRA/IBGE — tabela pública de população residente](https://sidra.ibge.gov.br/Tabela/202)
>
> **Material da disciplina:** [Banco de questões, questões 2 e 6, pp. 7–8](../apostila/banco_questoes_provas_2026_2.pdf#page=7)

---

### Variabilidade e vieses

A variabilidade pode resultar de:

- diferenças reais entre unidades;
- mudanças temporais ou espaciais;
- erro de medição;
- condições de coleta;
- seleção das unidades;
- valores ausentes;
- preparação e codificação dos dados.

Dois riscos importantes:

- **viés de seleção:** algumas unidades têm probabilidades diferentes ou desconhecidas de integrar os dados;
- **viés de medição:** o procedimento de observação produz diferenças sistemáticas entre o valor registrado e a característica de interesse.

> **Fonte pública:** [IBGE — Pesquisa de Pós-Enumeração do Censo 2022](https://www.ibge.gov.br/estatisticas/sociais/populacao/40418-pesquisa-de-pos-enumeracao-do-censo-demografico-2022.html)
>
> **Material da disciplina:** [Banco de questões, atividade de medição, p. 10](../apostila/banco_questoes_provas_2026_2.pdf#page=10)

---

## Notação e formulação matemática

Considere:

- $N$: número de unidades da população definida;
- $n$: número de unidades observadas na amostra;
- $\theta$: parâmetro populacional, como uma média ou proporção;
- $\widehat{\theta}$: estatística amostral usada para descrever os dados ou estimar $\theta$.

Em uma amostra:

$$
\widehat{\theta}=g(X_1,X_2,\ldots,X_n),
$$

em que $X_i$ representa a informação observada na unidade $i$ e $g$ é a regra de cálculo.

O valor de $\widehat{\theta}$ pode ser calculado corretamente e ainda assim não representar bem $\theta$ quando a amostra não sustenta a generalização pretendida.

---

### Representatividade não é apenas tamanho

Uma amostra grande pode continuar inadequada quando:

- exclui sistematicamente parte da população;
- depende de participação voluntária;
- utiliza um quadro amostral incompleto;
- mistura períodos ou condições incompatíveis;
- contém medições produzidas por procedimentos diferentes.

O tamanho $n$ influencia a variabilidade amostral, mas não corrige automaticamente vieses de seleção ou de medição.

> **Fonte pública:** [IBGE — PNAD Contínua: amostra e representatividade](https://painel.ibge.gov.br/saibamais/)
>
> **Material da disciplina:** [Apostila, amostragem, p. 9](../apostila/apostila_mq.pdf#page=9)

---

## Exemplo proposto

Considere o conjunto sintético a seguir, formado por seis registros de
atendimentos:

| Identificador | Canal | Período | Tempo (min) |
| --- | --- | --- | ---: |
| `A01` | presencial | manhã | 18 |
| `A02` | remoto | manhã | 24 |
| `A03` | presencial | tarde | 15 |
| `A04` | remoto | tarde | ausente |
| `A05` | presencial | tarde | 21 |
| `A06` | remoto | noite | 30 |

Antes da resolução, responda:

1. O que representa cada linha?
2. Quais colunas são qualitativas e quais são quantitativas?
3. Os seis registros formam a população?
4. Que conclusão seria descritiva?
5. Que conclusão exigiria inferência e justificativa amostral?

---

## Resolução do exemplo

### Unidade, registros e variáveis

- Cada linha descreve um atendimento incluído no processo de registro.
- O identificador, o canal e o período são variáveis qualitativas.
- O tempo é quantitativo, medido em minutos.
- A ausência do quarto tempo é informação sobre a qualidade e a completude dos dados; não deve ser transformada em zero.

Os seis registros podem constituir toda a base disponível sem constituir toda a
população de interesse. A relação entre base, amostra e população depende de
como e quando os atendimentos foram registrados.

---

### População e alcance

Uma conclusão descritiva válida seria:

> Entre os seis registros exibidos, os tempos observados variam de 15 min a
> 30 min, com um valor ausente.

Uma afirmação sobre todos os atendimentos exigiria:

- definição explícita da população-alvo;
- conhecimento do processo de seleção;
- avaliação da cobertura espacial e temporal;
- tratamento fundamentado dos valores ausentes;
- modelo inferencial compatível.

Os registros não constituem, apenas por existirem, uma amostra aleatória
simples de todos os atendimentos.

---

### Pergunta estatística possível

> Como o tempo observado varia entre os canais de atendimento registrados?

Essa pergunta:

- identifica uma variável quantitativa e sua unidade;
- define os grupos de comparação;
- admite variabilidade entre registros;
- pode ser respondida descritivamente com os dados disponíveis;
- não implica, por si só, causalidade ou generalização para outras populações.

---

## Aplicação ou discussão em sala

### Transferência para outro contexto

| instante | servidor | latência (ms) | status |
| --- | --- | ---: | --- |
| 10:00 | A | 82 | sucesso |
| 10:01 | A | 91 | sucesso |
| 10:02 | B | 430 | falha |
| 10:03 | B | 105 | sucesso |

O exemplo também é sintético. Em grupos, identifique:

1. a unidade de análise;
2. as variáveis e seus tipos;
3. uma população de interesse possível;
4. uma pergunta estatística;
5. um mecanismo de seleção capaz de produzir viés.

Encaminhamento: se cada linha representa uma requisição, “servidor” e “status” são qualitativas, enquanto “latência” é quantitativa em milissegundos. Uma coleta limitada a quatro minutos não sustenta automaticamente conclusões sobre todo o funcionamento mensal.

---

## Erros comuns e cuidados interpretativos

- Confundir linha do arquivo com unidade de análise sem verificar a documentação.
- Tratar a amostra disponível como se fosse toda a população de interesse.
- Afirmar representatividade apenas porque $n$ é grande.
- Interpretar ausência como zero.
- Confundir associação observada com efeito causal.
- Formular perguntas que os dados não conseguem responder.
- Omitir período, local, unidade e processo de coleta ao comunicar resultados.

---

## Síntese

- A pergunta estatística antecede o procedimento computacional.
- Registros, variáveis e unidades precisam ser interpretados no contexto da fonte.
- Estatística descritiva resume o observado; inferência amplia a conclusão mediante pressupostos.
- Representatividade depende do processo de seleção, não apenas do tamanho da amostra.
- Toda conclusão deve declarar população, dados, variabilidade, limitações e alcance.

---

## Estudo e exercícios

### Materiais públicos

- [Apostila de Métodos Quantitativos](../apostila/apostila_mq.pdf): seções 1.1–1.3, páginas 8–10.
- [Banco de questões e provas 2026.2](../apostila/banco_questoes_provas_2026_2.pdf): questões relacionadas aos fundamentos estatísticos.

### Exercícios indicados

- Barbetta et al., capítulo 1, exercício 2: população e amostra.
- Barbetta et al., capítulo 2, exercício 7: avaliação crítica de um plano amostral.

Ao resolver, identifique população, amostra, unidade de análise, variáveis e alcance da conclusão.

---

## Referências

- Apostila de Métodos Quantitativos, seções 1.1–1.3, páginas 8–10.
- BARBETTA et al. *Estatística para cursos de engenharia e informática*, capítulo 1, seções 1.1–1.6, páginas 12–23; capítulo 2, seções 2.1–2.2.1, páginas 24–31.
- PINHEIRO et al. *Estatística básica: a arte de trabalhar com dados*, capítulo 1, seções 1.1–1.2, páginas 20–23.
