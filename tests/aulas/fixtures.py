"""Fixtures pequenos e completos para os testes de curadoria."""

import copy


GRAPH = {
    "metadados": {},
    "nos": [
        {
            "id": "fonte-a",
            "tipo": "fonte",
            "titulo": "Fonte A",
        },
        {
            "id": "capitulo-fundamentos",
            "tipo": "capitulo",
            "numero_impresso": "1",
            "titulo": "Fundamentos",
            "pagina_pdf_inicio": 10,
            "pagina_pdf_fim": 13,
        },
        {
            "id": "secao-populacao",
            "tipo": "secao",
            "numero_impresso": "1.1",
            "titulo": "População e amostra",
            "pagina_pdf_inicio": 10,
            "pagina_pdf_fim": 12,
            "pertinencia_t199": "direta",
        },
        {
            "id": "questao-populacao",
            "tipo": "questao",
            "numero_impresso": "1",
            "pagina_pdf": 13,
            "pertinencia_t199": "direta",
        },
        {
            "id": "conteudo-01-01",
            "tipo": "conteudo_curricular",
            "codigo": "01.01",
            "unidade": "I",
            "nome": "Fundamentos estatísticos",
        },
        {
            "id": "topico-populacao",
            "tipo": "topico",
            "nome": "População",
        },
    ],
    "relacoes": [
        {
            "origem": "fonte-a",
            "tipo": "contem",
            "destino": "capitulo-fundamentos",
        },
        {
            "origem": "capitulo-fundamentos",
            "tipo": "contem",
            "destino": "secao-populacao",
        },
        {
            "origem": "capitulo-fundamentos",
            "tipo": "contem",
            "destino": "questao-populacao",
        },
        {
            "origem": "secao-populacao",
            "tipo": "corresponde_a",
            "destino": "conteudo-01-01",
        },
        {
            "origem": "secao-populacao",
            "tipo": "aborda",
            "destino": "topico-populacao",
        },
        {
            "origem": "questao-populacao",
            "tipo": "corresponde_a",
            "destino": "conteudo-01-01",
        },
        {
            "origem": "questao-populacao",
            "tipo": "aborda",
            "destino": "topico-populacao",
        },
    ],
}


VALID_MANIFEST = {
    "versao_contrato": "2.0",
    "estado": "em_selecao",
    "aula": {
        "id": "u1_a02",
        "semestre": "2026-2",
        "unidade": "I",
        "numero": 2,
        "data": "2026-08-07",
        "duracao_minutos": 100,
        "titulo": "Fundamentos da Estatística e processo de investigação",
        "conteudos_formais": ["01.01"],
        "resultado_aprendizagem": (
            "Distinguir descrição e inferência e avaliar representatividade."
        ),
    },
    "notacao": {
        "convencao": "global",
        "caminho": ".interno/docs/modelos/notacao-estatistica.md",
    },
    "escopo": {
        "incluidos": ["População e amostra"],
        "excluidos": ["Técnicas detalhadas de amostragem"],
        "reservados": ["Distribuições amostrais"],
    },
    "planejamento_tempo": {
        "abertura_minutos": 5,
        "fechamento_minutos": 10,
    },
    "recursos_discentes": {
        "materiais_didaticos": [{"id": "capitulo-fundamentos"}],
        "exercicios_indicados": [{"id": "questao-populacao"}],
    },
    "topicos": [
        {
            "id": "topico-populacao",
            "nome": "População",
            "classificacao": "central",
            "subassuntos": [],
            "estado": "pendente",
            "divergencias": [],
            "compatibilizacao": {
                "convencao": "notacao_global",
                "observacao": "Normalizar os símbolos pela convenção global.",
            },
            "profundidade": "formal_aplicada",
            "referencias": [
                {
                    "id": "secao-populacao",
                    "fonte_id": "fonte-a",
                    "estado": "pendente",
                    "papeis": [],
                    "paginas_pdf": {"inicio": 10, "fim": 12},
                    "cobertura": "Definição de população e amostra.",
                    "notacao": "N para população e n para amostra.",
                }
            ],
        }
    ],
}


def approved_manifest() -> dict:
    manifest = copy.deepcopy(VALID_MANIFEST)
    manifest["estado"] = "aprovado"
    topic = manifest["topicos"][0]
    topic["estado"] = "selecionado"
    reference = topic["referencias"][0]
    reference["estado"] = "selecionada"
    reference["papeis"] = ["fundamentacao"]
    return manifest
