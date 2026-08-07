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

## Contexto recorrente

Um serviço computacional registrou cinco requisições durante cinco minutos.

| Requisição | Instante | Servidor | Latência (ms) | Status |
| --- | --- | --- | ---: | --- |
| `R01` | 10:00 | A | 82 | sucesso |
| `R02` | 10:01 | A | 91 | sucesso |
| `R03` | 10:02 | B | 430 | falha |
| `R04` | 10:03 | B | 105 | sucesso |
| `R05` | 10:04 | A | ausente | falha |

**Tabela 1 - Registros sintéticos de requisições.** Os cinco registros reúnem instante, servidor, latência e status; quatro latências são numéricas e uma está ausente. Fonte: adaptado de Barbetta, Bornia e Reis (2010, seção 1.4).

> O que representa cada linha e o que foi registrado sobre ela?

O conjunto será retomado progressivamente. A tabela, sozinha, não informa se
os registros representam todo o funcionamento do serviço.

---

## Conceitos e definições

### Estatística e investigação

> Que perguntas sobre o serviço podem ser respondidas com esses registros?

A Estatística organiza métodos para formular perguntas, obter dados, representar a variabilidade, analisar evidências e comunicar conclusões com suas limitações.

Uma investigação estatística pode ser organizada em seis movimentos:

1. delimitar o problema;
2. formular uma pergunta respondível;
3. definir população, unidade de análise e variáveis;
4. obter ou reconhecer a origem dos dados;
5. analisar a variabilidade e os padrões;
6. comunicar a conclusão e seu alcance.

**Exemplo - Investigação do tempo de resposta de um serviço.** Uma equipe
recebe relatos de lentidão e organiza a investigação:

1. **Problema:** há relatos de demora no processamento de requisições.
2. **Pergunta:** como a latência varia ao longo da semana e entre os servidores?
3. **População, unidade e variáveis:** a população reúne as requisições da
   semana; cada requisição é uma unidade; instante, servidor, latência e status
   são as variáveis.
4. **Obtenção dos dados:** definir períodos de observação, registrar o processo
   de seleção e documentar falhas ou valores ausentes.
5. **Análise:** descrever as latências observadas e verificar diferenças entre
   períodos e servidores, sem atribuir causalidade automaticamente.
6. **Conclusão:** responder à pergunta somente para o alcance sustentado pelos
   registros e declarar as limitações da coleta.

Fonte: adaptado de Barbetta, Bornia e Reis (2010, seções 1.1–1.4).

---

### Fonte, registro e unidade de análise

> `R01` e `R02` são dois servidores ou duas requisições?

- **Fonte:** origem documentada dos dados.
- **Registro ou observação:** linha que reúne informações sobre uma unidade.
- **Unidade de análise:** entidade à qual as variáveis de um registro se referem.
- **Variável:** característica observada ou calculada para cada unidade.
- **Valor:** realização registrada de uma variável em determinada unidade.

Na tabela, cada linha é uma observação e a unidade de análise é uma requisição,
não um servidor. `Servidor` e `status` são variáveis qualitativas, `latência` é
quantitativa em milissegundos e `instante` registra a posição temporal.

Uma linha não é automaticamente uma pessoa, um dispositivo ou um evento. Seu
significado depende da documentação e do processo que gerou o conjunto.

> **Fonte pública:** [Portal Brasileiro de Dados Abertos — conjuntos de dados e metadados](https://dados.gov.br/)

---

### Variabilidade e qualidade dos dados

As latências numericamente observadas foram:

$$
82,\quad 91,\quad 430,\quad 105\text{ ms}.
$$

> Por que os valores não são todos iguais? O valor $430$ deve ser declarado
> erro apenas por ser o maior?

**Variabilidade** é a presença de diferenças entre os valores observados nas
unidades de análise. Ela pode resultar de:

- diferenças reais entre requisições;
- mudanças temporais nas condições do serviço;
- servidor responsável pelo processamento;
- erro de medição ou de registro;
- condições de coleta e preparação dos dados.

A latência ausente de `R05` não equivale a zero. A falha da requisição e a
ausência da medição também são informações diferentes. Por sua vez, $430$ ms é
um valor incomum neste conjunto reduzido, mas sua validade precisa ser
investigada antes de qualquer exclusão.

> **Fonte pública:** [IBGE — Pesquisa de Pós-Enumeração do Censo 2022](https://www.ibge.gov.br/estatisticas/sociais/populacao/40418-pesquisa-de-pos-enumeracao-do-censo-demografico-2022.html)

---

### População, censo, amostra e amostragem

> Se os cinco registros cobrem apenas o intervalo de 10:00 a 10:04, sobre que
> conjunto de requisições se pretende concluir?

- **População:** conjunto de unidades sobre o qual se pretende responder à pergunta.
- **Censo:** observação de todas as unidades da população definida.
- **Amostra:** subconjunto efetivamente observado.
- **Amostragem:** processo de seleção das unidades.
- **Quadro amostral:** representação operacional das unidades que poderiam ser selecionadas.

As cinco linhas são todos os registros exibidos, mas podem ser apenas uma
amostra das requisições do serviço. “Todas as requisições entre 10:00 e 10:04”
e “todas as requisições processadas durante uma semana” representam
populações diferentes. Se o registro capturou todas as requisições do primeiro
intervalo, ele constitui um censo dessa população restrita e, ao mesmo tempo,
pode funcionar como uma amostra inadequada da população semanal.

> **Fonte pública:** [IBGE — Censo Demográfico 2022: população-alvo e metodologia](https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html)

---

### Descrição e inferência

Considere duas afirmações:

> Entre as quatro latências numericamente registradas, os valores variaram de
> $82$ a $430$ ms.

> O serviço normalmente apresenta latência inferior a $150$ ms.

- **Estatística descritiva:** resume e representa os registros observados.
- **Estatística inferencial:** utiliza dados amostrais e um modelo para avaliar características de uma população ou processo.

A primeira afirmação descreve os dados disponíveis. A segunda amplia a
conclusão para o comportamento usual do serviço e exigiria uma população
definida, um processo de seleção justificável e um modelo compatível.

| Pergunta | Natureza |
| --- | --- |
| Como as latências variam entre as requisições registradas? | Descritiva |
| Qual é a latência típica de todas as requisições da semana? | Inferencial |
| Quantos dos cinco registros têm status de sucesso? | Descritiva |
| A taxa usual de sucesso do serviço é superior a 90%? | Inferencial |

**Tabela 2 - Perguntas descritivas e inferenciais.** Perguntas restritas aos
registros observados são descritivas, enquanto generalizações sobre o
funcionamento do serviço exigem inferência.

> **Fonte pública:** [SIDRA/IBGE — tabela pública de população residente](https://sidra.ibge.gov.br/Tabela/202)

---

### Vieses

Dois riscos importantes:

- **viés de seleção:** algumas unidades têm probabilidades diferentes ou desconhecidas de integrar os dados;
- **viés de medição:** o procedimento de observação produz diferenças sistemáticas entre o valor registrado e a característica de interesse.

Registrar somente os primeiros cinco minutos do dia pode produzir viés temporal
se o serviço se comportar de maneira diferente em outros horários. Usar apenas
as requisições que chegaram ao servidor A também excluiria sistematicamente
parte da população definida.

---

## Notação e formulação matemática

Para uma população definida de requisições, considere:

- $N$: número de unidades da população definida;
- $n$: número de unidades observadas na amostra;
- $\theta$: parâmetro populacional, como uma média ou proporção;
- $\widehat{\theta}$: estatística amostral usada para descrever os dados ou estimar $\theta$.

Em uma amostra:

$$
\widehat{\theta}=g(X_1,X_2,\ldots,X_n),
$$

em que $X_i$ representa a informação observada na unidade $i$ e $g$ é a regra de cálculo.

A amostra contém $n=5$ requisições, mas a variável latência possui somente
$n_{\mathrm{lat}}=4$ valores numéricos válidos. Qualquer resumo da latência deve
informar esse número efetivo de observações. Uma estatística pode ser calculada
corretamente e ainda assim não representar bem $\theta$ quando a amostra não
sustenta a generalização pretendida.

---

### Representatividade não é apenas tamanho

> Uma tabela maior, mas restrita ao mesmo intervalo de cinco minutos,
> resolveria o problema de representatividade?

Uma amostra grande pode continuar inadequada quando:

- exclui sistematicamente parte da população;
- depende de participação voluntária;
- utiliza um quadro amostral incompleto;
- mistura períodos ou condições incompatíveis;
- contém medições produzidas por procedimentos diferentes.

O tamanho $n$ influencia a variabilidade amostral, mas não corrige automaticamente vieses de seleção ou de medição.

> **Fonte pública:** [IBGE — PNAD Contínua: amostra e representatividade](https://painel.ibge.gov.br/saibamais/)

---

## Exemplo proposto

Retome o conjunto sintético de requisições e avalie a afirmação:

> O serviço normalmente apresenta latência inferior a $150$ ms.

Antes da resolução:

1. O que representa cada linha?
2. Quais colunas são qualitativas e quais são quantitativas?
3. Quantas latências podem ser analisadas numericamente?
4. Qual população está implícita na afirmação?
5. Os cinco registros sustentam essa generalização?
6. Que conclusão descritiva pode ser mantida?

---

## Resolução do exemplo

### Unidade, registros e variáveis

- Cada linha descreve uma requisição incluída no processo de registro.
- `Requisição` é um identificador, e não uma medida.
- `Servidor` e `status` são qualitativas.
- `Latência` é quantitativa, medida em milissegundos.
- `Instante` registra a posição temporal da requisição.
- Há cinco registros, mas somente quatro latências numéricas.

O valor ausente não deve ser transformado em zero. O valor $430$ ms não deve
ser excluído apenas por ser o maior: primeiro é necessário investigar sua
origem.

---

### População e alcance

Uma conclusão descritiva válida seria:

> Entre as quatro latências numericamente registradas, os valores variaram de
> $82$ a $430$ ms; uma das cinco requisições não possui latência registrada.

Uma afirmação sobre o funcionamento usual do serviço exigiria:

- definição explícita da população-alvo;
- conhecimento do processo de seleção;
- avaliação da cobertura temporal e dos servidores;
- tratamento fundamentado dos valores ausentes;
- modelo inferencial compatível.

Os cinco registros não constituem, apenas por existirem, uma amostra aleatória
simples de todas as requisições da semana. A afirmação proposta deve ser
recusada com os dados disponíveis.

---

### Pergunta estatística possível

> Como a latência varia entre as requisições registradas no intervalo de 10:00
> a 10:04?

Essa pergunta:

- identifica uma variável quantitativa e sua unidade;
- delimita os registros e o intervalo observado;
- admite variabilidade entre registros;
- pode ser respondida descritivamente com os dados disponíveis;
- não implica, por si só, causalidade ou generalização para outras populações.

---

## Aplicação ou discussão em sala

### Decisão sobre a coleta

Considere dois planos para estudar todas as requisições processadas durante uma
semana:

- **Plano A:** registrar todas as requisições dos primeiros cinco minutos da
  segunda-feira;
- **Plano B:** a cada hora da semana, sortear uma requisição entre aquelas
  processadas naquele intervalo.

Em grupos:

1. aprove ou recuse cada plano como estratégia para representar a população;
2. identifique um possível viés;
3. indique qual plano oferece melhor cobertura temporal;
4. declare que informação ainda seria necessária para avaliar a seleção.

Encaminhamento: o Plano B distribui a coleta no tempo e tende a oferecer melhor
cobertura, mas não garante representatividade por si só. É necessário conhecer
o quadro amostral, os períodos sem requisições e a execução efetiva do sorteio.

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

### Materiais didáticos

- [Apostila de Métodos Quantitativos](../apostila/apostila_mq.pdf): seções 1.1–1.3, páginas 8–10.
- [Banco de questões e provas 2026.2](../apostila/banco_questoes_provas_2026_2.pdf): seção 1.1, páginas 7–13.

### Exercícios indicados

- Banco de questões, questão 6: descrição e inferência.
- Banco de questões, questão 13: variabilidade e viés de medição.
- Barbetta et al., capítulo 1, exercício 2: população e amostra.
- Barbetta et al., capítulo 2, exercício 7: avaliação crítica de um plano amostral.

Ao resolver, identifique população, amostra, unidade de análise, variáveis e alcance da conclusão.

---

## Referências

- Apostila de Métodos Quantitativos, seções 1.1–1.3, páginas 8–10.
- BARBETTA, Pedro Alberto; BORNIA, Antonio Cezar; REIS, Marcelo Menezes. *Estatística para cursos de engenharia e informática*. 3. ed. São Paulo: Atlas, 2010.
- NAVIDI. *Statistics for Engineers and Scientists*, capítulo 1, introdução e seção 1.1, páginas 23–30.
- PINHEIRO et al. *Estatística básica: a arte de trabalhar com dados*, capítulo 1, seções 1.1–1.2, páginas 20–23.
