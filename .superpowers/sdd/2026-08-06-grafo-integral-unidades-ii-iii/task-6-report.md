# Task 6 — Promoção da cobertura integral

## Escopo

Promovida a cobertura canônica do grafo para os doze conteúdos de `01.01` a
`03.04`. Nenhuma curadoria, consulta ou renderizador foi alterado.

## RED

Após atualizar os gates de teste para o estado integral, o comando
`.venv/bin/python -m unittest tests.grafo_refs.test_build_graph -v` falhou em
`test_builds_the_declared_complete_coverage_deterministically`: o construtor
ainda declarava `estado == "parcial"`.

## GREEN

- `build_graph.py` declara `completo`, os doze códigos concluídos e nenhum pendente.
- O schema fixa essa declaração de cobertura.
- `validate_graph.py` rejeita cobertura divergente e todo código concluído sem
  uma relação `corresponde_a`.
- O teste da Unidade II agora protege a cobertura integral; o teste semântico
  remove todas as referências de `03.04` de um grafo válido e confirma a rejeição.

## Verificação

```bash
.venv/bin/python -m unittest \
  tests.grafo_refs.test_schema \
  tests.grafo_refs.test_validate_graph \
  tests.grafo_refs.test_unidade_ii_complete \
  tests.grafo_refs.test_unidade_iii_complete -v
```

Resultado: `Ran 42 tests ... OK`.

O grafo canônico também foi construído em memória; a validação semântica
retornou `validation_errors= []`.
