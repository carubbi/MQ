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

> O que representa cada registro do Palmer Penguins e até onde as conclusões obtidas com esses dados podem ser generalizadas?

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

---

### Fonte, registro e unidade de análise

- **Fonte:** origem documentada dos dados.
- **Registro ou observação:** linha que reúne informações sobre uma unidade.
- **Unidade de análise:** entidade à qual as variáveis de um registro se referem.
- **Variável:** característica observada ou calculada para cada unidade.
- **Valor:** realização registrada de uma variável em determinada unidade.

Uma linha não é automaticamente uma pessoa, um dispositivo ou um evento. Seu significado depende do processo que gerou o conjunto.

---

### População, censo, amostra e amostragem

- **População:** conjunto de unidades sobre o qual se pretende responder à pergunta.
- **Censo:** observação de todas as unidades da população definida.
- **Amostra:** subconjunto efetivamente observado.
- **Amostragem:** processo de seleção das unidades.
- **Quadro amostral:** representação operacional das unidades que poderiam ser selecionadas.

A população precisa ser declarada. “Todos os pinguins” e “os pinguins adultos associados aos ninhos observados no Arquipélago Palmer” representam populações diferentes.

---

### Descrição e inferência

- **Estatística descritiva:** resume e representa os registros observados.
- **Estatística inferencial:** utiliza dados amostrais e um modelo para avaliar características de uma população ou processo.

Uma descrição correta da amostra não garante uma inferência válida para uma população mais ampla.

| Pergunta | Natureza |
| --- | --- |
| Qual foi a massa corporal mediana entre os registros disponíveis? | Descritiva |
| Qual é a massa corporal mediana de todos os pinguins da população-alvo? | Inferencial |
| Como as medidas variam entre as espécies registradas? | Descritiva |
| A diferença observada pode ser generalizada para outra região ou período? | Inferencial |

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

---

## Exemplo proposto

Considere este recorte dos seis primeiros registros do arquivo bruto:

| Identificador | Espécie | Ilha | Massa corporal (g) |
| --- | --- | --- | ---: |
| `N1A1` | Adelie | Torgersen | 3750 |
| `N1A2` | Adelie | Torgersen | 3800 |
| `N2A1` | Adelie | Torgersen | 3250 |
| `N2A2` | Adelie | Torgersen | ausente |
| `N3A1` | Adelie | Torgersen | 3450 |
| `N3A2` | Adelie | Torgersen | 3650 |

Antes da resolução, responda:

1. O que representa cada linha?
2. Quais colunas são qualitativas e quais são quantitativas?
3. Os seis registros formam a população?
4. Que conclusão seria descritiva?
5. Que conclusão exigiria inferência e justificativa amostral?

---

## Resolução do exemplo

### Unidade, registros e variáveis

- Cada linha descreve um pinguim adulto associado a um ninho incluído no processo de coleta.
- O identificador, a espécie e a ilha são variáveis qualitativas.
- A massa corporal é quantitativa, medida em gramas.
- A ausência da quarta massa corporal é informação sobre a qualidade e a completude dos dados; não deve ser transformada em zero.

Os seis registros são apenas um recorte da amostra disponível. O arquivo bruto completo contém 344 registros e 17 colunas.

---

### População e alcance

Uma conclusão descritiva válida seria:

> Entre os seis registros exibidos, as massas corporais observadas variam de 3250 g a 3800 g, com um valor ausente.

Uma afirmação sobre todos os pinguins exigiria:

- definição explícita da população-alvo;
- conhecimento do processo de seleção;
- avaliação da cobertura espacial e temporal;
- tratamento fundamentado dos valores ausentes;
- modelo inferencial compatível.

Os registros não constituem, apenas por existirem, uma amostra aleatória simples de todos os pinguins.

---

### Pergunta estatística possível

> Como a massa corporal observada varia entre as espécies registradas no conjunto Palmer Penguins?

Essa pergunta:

- identifica uma variável quantitativa;
- define os grupos de comparação;
- admite variabilidade entre registros;
- pode ser respondida descritivamente com os dados disponíveis;
- não implica, por si só, causalidade ou generalização para outras populações.

---

## Aplicação ou discussão em sala

### Transferência para um log sintético

| instante | servidor | latência (ms) | status |
| --- | --- | ---: | --- |
| 10:00 | A | 82 | sucesso |
| 10:01 | A | 91 | sucesso |
| 10:02 | B | 430 | falha |
| 10:03 | B | 105 | sucesso |

O exemplo é sintético. Em grupos, identifique:

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
- [Palmer Penguins — arquivo bruto](../data/raw/penguins_raw.csv).

### Exercícios indicados

- Barbetta et al., capítulo 1, exercício 2: população e amostra.
- Barbetta et al., capítulo 2, exercício 7: avaliação crítica de um plano amostral.

Ao resolver, identifique população, amostra, unidade de análise, variáveis e alcance da conclusão.

---

## Referências

- Apostila de Métodos Quantitativos, seções 1.1–1.3, páginas 8–10.
- BARBETTA et al. *Estatística para cursos de engenharia e informática*, capítulo 1, seções 1.1–1.6, páginas 12–23; capítulo 2, seções 2.1–2.2.1, páginas 24–31.
- PINHEIRO et al. *Estatística básica: a arte de trabalhar com dados*, capítulo 1, seções 1.1–1.2, páginas 20–23.
- GORMAN, K. B.; WILLIAMS, T. D.; FRASER, W. R. Ecological sexual dimorphism and environmental variability within a community of Antarctic penguins. *PLoS ONE*, v. 9, n. 3, e90081, 2014.
