import json
import tempfile
import unittest
from pathlib import Path

from scripts.grafo_refs.validate_teaching_resources import validate_resource


ROOT = Path(__file__).resolve().parents[2]
GRAPH = json.loads(
    (ROOT / "prof/refs/mapas/grafo_referencias.json").read_text(encoding="utf-8")
)

VALID_AULA = """# Fundamentos estatísticos

- **Conteúdos formais:** `01.01`
- **Tópicos:** Investigação estatística; População; Amostra

---

## Pergunta orientadora
Pergunta.

## Conceitos e definições
Conceitos.

## Notação e formulação matemática
$n$ é o tamanho da amostra.

## Exemplo proposto
Problema.

## Resolução do exemplo
Resolução e interpretação.

## Aplicação ou discussão em sala
Discussão.

## Erros comuns e cuidados interpretativos
Cuidados.

## Síntese
Síntese.

## Estudo e exercícios
Estudo.

## Referências
Apostila de Métodos Quantitativos, seção 1.1.
"""

VALID_ROTEIRO = """# Roteiro do notebook guiado — Fundamentos estatísticos

> Estado: roteiro estrutural em Markdown; não executável.

## 1. Identificação
- **Conteúdos formais:** `01.01`
- **Tópicos:** Investigação estatística; População; Amostra

## 2. Resultado de aprendizagem
Resultado observável.

## 3. Contexto e pergunta-problema
Pergunta substantiva.

## 4. Preparação conceitual
Conceitos.

## 5. Dados, entradas e dependências
Dados.

## 6. Antecipação conceitual antes do cálculo ou da execução
Antecipação justificada.

## 8. Sequência funcional do futuro notebook
Blocos funcionais.

## 9. Verificação e contraste
Contraste.

## 10. Evidência de aprendizagem
Resultado e justificativa.

## 11. Síntese e limitações
Perguntas de fechamento.

## 12. Estudo, exercícios e referências
Referências.

## 13. Critérios para implementação futura
Critérios específicos.
"""


class TeachingResourceValidatorTests(unittest.TestCase):
    def test_accepts_valid_aula(self):
        self.assertEqual(
            [],
            validate_resource(
                Path("aula.md"),
                "aula",
                GRAPH,
                VALID_AULA,
            ),
        )

    def test_accepts_valid_roteiro_without_conditional_section_seven(self):
        self.assertEqual(
            [],
            validate_resource(
                Path("roteiro.md"),
                "roteiro",
                GRAPH,
                VALID_ROTEIRO,
            ),
        )

    def test_rejects_forbidden_latex_and_marp(self):
        invalid = VALID_AULA + "\nmarp: true\n\\(x\\)\n"
        findings = validate_resource(
            Path("aula.md"),
            "aula",
            GRAPH,
            invalid,
        )
        self.assertIn("diretiva Marp proibida", findings)
        self.assertIn("delimitador LaTeX proibido", findings)

    def test_rejects_unknown_content_and_topic(self):
        invalid = VALID_AULA.replace("`01.01`", "`99.99`").replace(
            "Investigação estatística",
            "Tópico inexistente",
        )
        findings = validate_resource(
            Path("aula.md"),
            "aula",
            GRAPH,
            invalid,
        )
        self.assertIn(
            "conteúdo curricular desconhecido: 99.99",
            findings,
        )
        self.assertIn(
            "tópico desconhecido: Tópico inexistente",
            findings,
        )

    def test_rejects_incomplete_sections(self):
        invalid = VALID_ROTEIRO.replace(
            "## 10. Evidência de aprendizagem",
            "## Evidência",
        )
        findings = validate_resource(
            Path("roteiro.md"),
            "roteiro",
            GRAPH,
            invalid,
        )
        self.assertIn(
            "seção ausente: ## 10. Evidência de aprendizagem",
            findings,
        )

    def test_rejects_escovedo_and_missing_slide_separator(self):
        invalid = VALID_AULA.replace("\n---\n", "\n").replace(
            "Apostila de Métodos Quantitativos",
            "Escovedo",
        )
        findings = validate_resource(
            Path("aula.md"),
            "aula",
            GRAPH,
            invalid,
        )
        self.assertIn("referência Escovedo proibida", findings)
        self.assertIn("separador editorial ausente", findings)

    def test_rejects_course_dataset_in_theoretical_slides(self):
        invalid = VALID_AULA + "\nAplicação com Palmer Penguins.\n"
        findings = validate_resource(
            Path("aula.md"),
            "aula",
            GRAPH,
            invalid,
        )
        self.assertIn(
            "conjunto didático específico em slides teóricos: Palmer Penguins",
            findings,
        )

        roteiro = VALID_ROTEIRO + "\nDados: Palmer Penguins.\n"
        self.assertEqual(
            [],
            validate_resource(
                Path("roteiro.md"),
                "roteiro",
                GRAPH,
                roteiro,
            ),
        )

    def test_rejects_broken_local_link(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "aula.md"
            text = VALID_AULA + "\n[arquivo](arquivo-ausente.csv)\n"
            path.write_text(text, encoding="utf-8")
            findings = validate_resource(path, "aula", GRAPH)
        self.assertIn(
            "link local quebrado: arquivo-ausente.csv",
            findings,
        )


if __name__ == "__main__":
    unittest.main()
