"""Gera amostras sintéticas para os exercícios 5.7 e 5.11 de Barbetta."""

import csv
from pathlib import Path

import numpy as np


DESTINO = Path(__file__).resolve().parent
REPETICOES = 5_000
SEMENTE = 2026


def gerar_binomial() -> None:
    """Simula lotes de 20 itens com probabilidade de defeito de 0,05."""
    gerador = np.random.default_rng(SEMENTE)
    defeitos_por_item = gerador.binomial(1, 0.05, size=(REPETICOES, 20))
    defeituosos_por_lote = defeitos_por_item.sum(axis=1)

    caminho = DESTINO / "u2_s03_binomial_ex07.csv"
    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        tabela = csv.writer(arquivo, lineterminator="\n")
        tabela.writerow(("lote", "defeituosos", "bons"))
        for lote, defeituosos in enumerate(defeituosos_por_lote, start=1):
            quantidade = int(defeituosos)
            tabela.writerow((lote, quantidade, 20 - quantidade))


def gerar_poisson() -> None:
    """Simula dois intervalos independentes de 30 s por minuto."""
    gerador = np.random.default_rng(SEMENTE)
    chegadas_30s = gerador.poisson(2.5, size=(REPETICOES, 2))

    caminho = DESTINO / "u2_s03_poisson_ex11.csv"
    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        tabela = csv.writer(arquivo, lineterminator="\n")
        tabela.writerow(("minuto", "chegadas_0_30s", "chegadas_30_60s", "chegadas_1min"))
        for minuto, (primeira_metade, segunda_metade) in enumerate(chegadas_30s, start=1):
            primeira = int(primeira_metade)
            segunda = int(segunda_metade)
            tabela.writerow((minuto, primeira, segunda, primeira + segunda))


if __name__ == "__main__":
    gerar_binomial()
    gerar_poisson()
