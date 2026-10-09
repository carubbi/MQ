# CSV sintético da Aula 11

O arquivo [u1_a11_cds.csv](u1_a11_cds.csv) contém 1.000 linhas artificiais para a prática de probabilidade. Ele reproduz exatamente as contagens agregadas do exercício 19 do capítulo 4 de Barbetta, Reis e Bornia (2010): 700 CDs com resistência alta e trilhas aprovadas, 140 com resistência alta e trilhas reprovadas, 100 com resistência baixa e trilhas aprovadas e 60 com resistência baixa e trilhas reprovadas.

As linhas foram embaralhadas com semente 2026. A ordem e os registros individuais não provêm do livro. A simulação posterior no notebook produz novas seleções e não altera este arquivo.

Referência: BARBETTA, Pedro Alberto; REIS, Marcelo Menezes; BORNIA, Antonio Cezar. *Estatística para cursos de engenharia e informática*. 3. ed. São Paulo: Atlas, 2010, capítulo 4, exercício 19, p. 115.


## CSV sintético da Aula 1 da Unidade II

Os nomes dos arquivos conservam os identificadores anteriores à renumeração das aulas.

O arquivo [u1_a12_psicologos.csv](u1_a12_psicologos.csv) contém 1.000 registros artificiais derivados dos percentuais do exercício 3.8_P de Pinheiro et al. (2009, p. 94). Não são observações individuais coletadas nem registros publicados no livro.

| Área | Usa computador | Não usa computador | Total |
| --- | ---: | ---: | ---: |
| Clínica | 60 | 540 | 600 |
| Empresarial | 140 | 60 | 200 |
| Outras | 80 | 120 | 200 |
| Total | 280 | 720 | 1.000 |

As colunas são `area` (Clínica, Empresarial ou Outras) e `usa_pc` (`True` para usa computador e `False` para não usa). Cada registro pertence a uma única área. O CSV está codificado em UTF-8, separado por vírgulas e já embaralhado com semente 2026, usando `DataFrame.sample(frac=1, random_state=2026)`. O embaralhamento altera somente a ordem das linhas e preserva as contagens exatas.

Os dados reproduzem P(não usa) = 720/1.000 = 0,72 e P(clínica | não usa) = 540/720 = 0,75.

Referência: PINHEIRO, João Ismael D. et al. *Estatística básica: a arte de trabalhar com dados*. Rio de Janeiro: Elsevier, 2009, exercício 3.8_P, p. 94.


## CSV sintético da Aula 1 da Unidade II — teste de gravidez

O arquivo [u1_a12_teste_gravidez.csv](u1_a12_teste_gravidez.csv) contém 1.000 registros artificiais derivados das probabilidades do exercício 3.9_P de Pinheiro et al. (2009, p. 94). Representa o cenário hipotético de probabilidade inicial de gravidez igual a 0,20, sensibilidade igual a 0,98 e especificidade igual a 0,95. Não contém dados clínicos reais; a proporção de gravidez reproduz a premissa do exercício, não uma prevalência populacional estimada.

| Condição | Teste positivo | Teste negativo | Total |
| --- | ---: | ---: | ---: |
| Gravidez | 196 | 4 | 200 |
| Não gravidez | 40 | 760 | 800 |
| Total | 236 | 764 | 1.000 |

As colunas são `grav` (`True` para gravidez e `False` para não gravidez) e `pos` (`True` para teste positivo e `False` para teste negativo). O CSV está codificado em UTF-8, separado por vírgulas e já embaralhado com semente 2026, usando `DataFrame.sample(frac=1, random_state=2026)`. O embaralhamento preserva as contagens exatas.

Os dados reproduzem P(gravidez | positivo) = 196/236 ≈ 0,8305 e P(não gravidez | negativo) = 760/764 ≈ 0,9948.

Referência: PINHEIRO, João Ismael D. et al. *Estatística básica: a arte de trabalhar com dados*. Rio de Janeiro: Elsevier, 2009, exercício 3.9_P, p. 94.


## CSVs sintéticos da Semana 3 da Unidade II — distribuições discretas

Os arquivos abaixo apoiam a comparação entre **probabilidades teóricas** e **frequências simuladas** dos exercícios de Barbetta. Não são dados coletados nem tabelas fornecidas pela obra. Os parâmetros dos enunciados determinam as respostas teóricas; as frequências dos CSVs variam por acaso e não foram ajustadas para reproduzi-las exatamente.

- [u2_s03_binomial_ex07.csv](u2_s03_binomial_ex07.csv): 5.000 lotes independentes de 20 itens. Cada item foi simulado como indicador de defeito com probabilidade 0,05. As colunas são `lote`, `defeituosos` e `bons`, com `defeituosos + bons = 20` em cada linha. Apoia o exercício 7 do capítulo 5, p. 131 impressa.
- [u2_s03_poisson_ex11.csv](u2_s03_poisson_ex11.csv): 5.000 minutos independentes, divididos em duas janelas de 30 segundos. Cada meia janela foi simulada por Poisson com média 2,5, correspondente à taxa de cinco chegadas por minuto. As colunas são `minuto`, `chegadas_0_30s`, `chegadas_30_60s` e `chegadas_1min`. A última é a soma das duas meias janelas. Apoia o exercício 11 do capítulo 5, p. 136 impressa.

Os arquivos são UTF-8, separados por vírgulas, com cabeçalho e sem valores ausentes. Foram gerados com `numpy.random.default_rng(2026)` pelo script [gerar_u2_s03.py](gerar_u2_s03.py). A mesma semente é inicializada separadamente para cada exercício. Para executar os notebooks no Colab, os CSVs devem ser lidos por URL do repositório publicada em um commit, como nos notebooks anteriores.

Referência: BARBETTA, Pedro Alberto; REIS, Marcelo Menezes; BORNIA, Antonio Cezar. *Estatística para cursos de engenharia e informática*. 3. ed. São Paulo: Atlas, 2010, capítulo 5, exercícios 7 e 11.
