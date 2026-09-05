# Acompanhamentos formativos da AP integrada

## Regras comuns

- Cada unidade terá três acompanhamentos.
- Os acompanhamentos seguirão o [cronograma da turma](../ensino/cronograma_2026_2_t199_64_65.md).
- Na Unidade I, ocorrerão nas Aulas 8, 10 e 12; o acompanhamento final será em 11/09, das 18h30 às 19h.
- Na Unidade II, ocorrerão nos 30 minutos finais das Aulas 6, 8 e 10.
- Na Unidade III, ocorrerão nos 30 minutos finais das Aulas 6, 10 e 11; a Aula 11 também conterá a revisão teórica.
- Os acompanhamentos não gerarão notas isoladas.
- O grupo apresentará o notebook em desenvolvimento, não apenas um relato oral.
- Ao final, registrará ajustes, responsável e prazo interno.

## Unidade I

### Primeiro acompanhamento

Evidências:

- repositório criado, estrutura mínima organizada e acesso concedido ao professor;
- identificação correta do arquivo bruto fornecido;
- `notebooks/ap1.ipynb` com cabeçalho institucional, título principal e seção de carregamento;
- célula própria para carregar `data/raw/AmesHousing.txt`;
- código de importação;
- dimensões e unidade de análise;
- nomes originais e eventual mapeamento;
- tipos, conversões e ausências a investigar.
- inspeção inicial de `Fireplaces`, `Mas Vnr Area`, `Year Remod/Add` e `Year Built`.

### Segundo acompanhamento

Evidências:

- análise univariada inicial;
- tabela de medidas, histogramas e gráfico de barras de $B$;
- cercas de Tukey;
- uso de `IQR`;
- tabela dos limites e boxplots;
- investigação dos casos sinalizados;
- decisão preliminar sobre manutenção, correção ou exclusão.

### Acompanhamento final

Evidências:

- frequências e agrupamento final de $B$;
- rótulos finais das categorias de $B$;
- tabela anual e gráfico de linha da mediana do preço de venda (`SalePrice`) por ano da venda (`Yr Sold`);
- diagrama de dispersão e correlação entre preço de venda (`SalePrice`) e área construída (`Gr Liv Area`);
- tabela de medidas e boxplots do preço de venda (`SalePrice`) por categoria de $B$;
- interpretação das limitações temporais;
- registro das decisões congeladas.
- `README.md` com identificação, estrutura e instruções iniciais de execução.
- produção reproduzível de `data/processed/AmesHousing.csv`.

## Unidade II

### Primeiro acompanhamento

Evidências:

- `notebooks/ap2.ipynb` com cabeçalho institucional, título principal e carregamento de `data/processed/AmesHousing.csv`;
- registro da variável ou do evento e do modelo candidato atribuídos;
- pergunta de pesquisa específica;
- unidade de análise e definição da variável aleatória;
- classificação, valores possíveis e suporte;
- compatibilidade inicial do modelo atribuído;
- descrição empírica inicial.

### Segundo acompanhamento

Evidências:

- definição e calibração empírica dos parâmetros;
- esperança e variância teóricas;
- tabela ou gráfico observado coerente com o tipo da variável;
- para a trilha Normal, previsão do histograma e do Q–Q plot;
- plano de simulação com 10.000 realizações e semente definida;
- critérios previstos para comparar dados observados, modelo teórico e simulação.

### Acompanhamento final

Evidências:

- simulação reproduzível;
- células curtas, saídas individuais e interpretações subsequentes;
- comparação entre resultados observados, teóricos e simulados;
- para a trilha Normal, histograma e Q–Q plot interpretados conjuntamente;
- auditoria dos pressupostos específicos da trilha;
- parecer adequado, parcialmente adequado ou inadequado;
- conclusão e limitações;
- repositório atualizado, notebook executável e acesso docente confirmado.

## Unidade III

### Primeiro acompanhamento

Evidências:

- `notebooks/ap3.ipynb` com cabeçalho institucional, título principal e carregamento de `data/processed/AmesHousing.csv`;
- pergunta de pesquisa e objetivo da investigação;
- população conceitual e limitações de representatividade;
- preço de venda (`SalePrice`) como resposta;
- registro, anterior ao ajuste, das variáveis quantitativas candidatas, da escolha de $X$ e de sua justificativa substantiva e quanto à qualidade dos dados;
- $X$ e característica $B$ como preditores;
- categorias preservadas e categoria de referência de $B$;
- diagrama de dispersão;
- ajuste inicial da regressão simples;
- interpretação inicial do `OLS Regression Results`, incluindo $R^2$ e $R^2_{\mathrm{ajustado}}$.

### Segundo acompanhamento

Evidências:

- inferência sobre a inclinação da regressão simples;
- diagnóstico do modelo simples;
- parecer explícito de aprovação ou recusa de $X$, justificado pelo valor-p da inclinação, por $R^2$, por $R^2_{\mathrm{ajustado}}$ e pelos resíduos;
- registro de cada candidata recusada e da repetição do procedimento até a aprovação de $X$;
- regressão múltipla com `C(B)`;
- categoria de referência;
- interpretação dos coeficientes indicadores;
- inferência inicial sobre os coeficientes;
- comparação inicial entre os modelos por $R^2$, $R^2_{\mathrm{ajustado}}$ e interpretação substantiva.

### Acompanhamento final

Evidências:

- interpretação dos principais resultados do `OLS Regression Results`;
- gráficos de diagnóstico dos modelos;
- comparação entre regressão simples e múltipla por $R^2$, $R^2_{\mathrm{ajustado}}$, diagnóstico e interpretação;
- inferência sobre a inclinação e os indicadores de $B$;
- células curtas, saídas individuais e interpretações subsequentes;
- conclusão sobre associação bruta e ajustada;
- pressupostos e limitações;
- contribuições dos integrantes;
- declaração de uso de IA.
- `README.md` final, dependências atualizadas, notebooks executáveis e acesso docente confirmado.
