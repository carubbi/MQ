# Modelos textuais dos notebooks da AP integrada

Os modelos definem a ordem das seções. Células Markdown e de código deverão ser intercaladas em uma progressão didática; títulos vazios não constituem entrega.

Os modelos apresentam apenas os blocos acadêmicos essenciais e sua sequência geral. Cada grupo deverá decidir como selecionar, organizar e articular as evidências estatísticas necessárias dentro desses blocos, observando o enunciado e a rubrica de cada AP. Subtítulos adicionais poderão ser utilizados quando contribuírem para a clareza da investigação.

## Estrutura externa aos notebooks

Os três notebooks deverão permanecer no mesmo repositório, respectivamente em `notebooks/ap1.ipynb`, `notebooks/ap2.ipynb` e `notebooks/ap3.ipynb`. O projeto também deverá conter `README.md`, `requirements.txt`, `.gitignore`, `data/raw/` e `data/processed/`, conforme a especificação geral.

Cada notebook começará com duas células Markdown:

1. conteúdo integral de [cabeçalho institucional da Aula 1](../notebooks/u1_a01.ipynb);
2. título principal da AP.

Depois dessas células, cada seção deverá combinar:

1. contexto ou pergunta;
2. conceito ou justificativa;
3. célula curta de código;
4. saída individual;
5. interpretação da saída;
6. conclusão parcial e transição.

O notebook não deverá reunir em uma única célula extensa o carregamento, o pré-processamento, a análise e a visualização.

## Modelo da AP1

````markdown
# AP1 — Análise exploratória do preço de venda de imóveis residenciais

## 1. Identificação

## 2. Delimitação da investigação

### 2.1 Contexto
### 2.2 Pergunta de pesquisa
### 2.3 Objetivo da investigação

## 3. Carregamento dos dados

## 4. Análise exploratória

### 4.1 Análise univariada
### 4.2 Análise bivariada

## 5. Exportação dos dados

## 6. Conclusão e limitações

## 7. Contribuições dos integrantes
## 8. Declaração de uso de inteligência artificial
## 9. Referências
````

## Modelo da AP2

```markdown
# AP2 — Auditoria de modelos probabilísticos

## 1. Identificação

## 2. Delimitação da investigação

### 2.1 Contexto
### 2.2 Pergunta de pesquisa
### 2.3 Objetivo da investigação
### 2.4 Atribuição

## 3. Carregamento dos dados

## 4. Delimitação da variável aleatória

### 4.1 Unidade de análise e definição
### 4.2 Classificação e suporte

## 5. Compatibilidade conceitual inicial

## 6. Caracterização empírica

### 6.1 Observações válidas e ausentes
### 6.2 Medidas e distribuição de frequências
### 6.3 Representação gráfica

## 7. Modelo probabilístico candidato

### 7.1 Definição e parâmetros
### 7.2 Esperança e variância
### 7.3 Calibração empírica

## 8. Simulação

### 8.1 Configuração e reprodutibilidade
### 8.2 Comparação entre resultados observados, teóricos e simulados

## 9. Auditoria dos pressupostos
## 10. Parecer de adequação
## 11. Conclusão e limitações

## 12. Contribuições dos integrantes
## 13. Declaração de uso de inteligência artificial
## 14. Referências
```

## Modelo da AP3

```markdown
# AP3 — Modelagem estatística do preço de venda de imóveis residenciais

## 1. Identificação

## 2. Delimitação da investigação

### 2.1 Contexto
### 2.2 Pergunta de pesquisa
### 2.3 Objetivo da investigação

## 3. Carregamento dos dados

## 4. Modelagem estatística

### 4.1 Regressão linear simples
### 4.2 Regressão linear múltipla

## 5. Avaliação dos modelos

### 5.1 Inferência e qualidade do ajuste
### 5.2 Diagnóstico
### 5.3 Comparação

## 6. Conclusão e limitações

## 7. Contribuições dos integrantes
## 8. Declaração de uso de inteligência artificial
## 9. Referências
```

## Regras de execução

- Reiniciar o kernel e executar todas as células antes da entrega.
- Não depender de variáveis criadas fora do notebook.
- Usar caminhos relativos à raiz do repositório.
- Manter as dependências necessárias no `requirements.txt`.
- Manter células de código curtas e com finalidade analítica única.
- Apresentar saídas relevantes individualmente e interpretá-las em células Markdown subsequentes.
- Legendar tabelas e figuras científicas relevantes em sequência.
- Registrar sementes das simulações.
- Usar LaTeX para fórmulas e símbolos.
- Informar unidades em tabelas, eixos e interpretações.
- Comentar somente decisões não evidentes no código.
- Não ocultar avisos ou erros relevantes.
