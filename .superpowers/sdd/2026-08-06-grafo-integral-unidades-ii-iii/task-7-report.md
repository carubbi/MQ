# Task 7 — Consultas e Markdown para cobertura integral

## Escopo

Atualizados somente o renderer e seus testes de consulta/renderização. As
curadorias e os artefatos publicados não foram alterados.

## RED

O novo teste do renderer para o grafo completo falhou porque a saída ainda
começava pelo aviso `Cobertura parcial` e a seção de pendências ficava vazia.
O teste de consulta `03.04` ficou verde imediatamente: `query_by_content`
já inferia corretamente o estado a partir da lista integral de concluídos.

## GREEN

- A saída de cobertura `completo` inicia apenas com o título do grafo.
- A seção de pendências exibe `nenhum conteúdo pendente` quando não há códigos
  pendentes.
- A mensagem sobre itens fora do escopo não descreve a cobertura como parcial
  no grafo completo.
- Fixtures parciais preservam o aviso e o comportamento de pendência.

## Verificação

```bash
.venv/bin/python -m unittest \
  tests.grafo_refs.test_query_graph \
  tests.grafo_refs.test_render_markdown -v
```

Resultado: `Ran 15 tests ... OK`.

Verificação complementar de schema, validador e gates das Unidades II e III:
`Ran 43 tests ... OK`.
