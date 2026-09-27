# Prática 3 - respostas dos desafios
# Minicurso "Consumo de APIs e Análise de Dados na Prática" - SECOMPP26

import json
import os

import pandas as pd


def carregar(nome):
    """Abre o arquivo da sua pasta. Se ele não estiver lá, usa o do repositório."""
    caminho = nome
    if not os.path.isfile(caminho):
        pasta_do_script = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.join(pasta_do_script, "..", "dados_offline", nome)
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


if os.path.isfile("jogador.json"):
    jogador = carregar("jogador.json")
else:
    jogador = carregar("jogador_exemplo.json")
df = pd.DataFrame(jogador["brawlers"])

# Desafio 1: brawlers com menos de 1000 troféus e a média deles
fracos = df[df["trophies"] < 1000]
print(len(fracos), "brawlers com menos de 1000 troféus")
if len(fracos) > 0:
    print("Média de troféus deles:", round(fracos["trophies"].mean()))

# Desafio 2: a maior sequência de vitórias
melhor = df.sort_values("maxWinStreak", ascending=False).iloc[0]
print("\nMaior sequência de vitórias:", melhor["name"], "-", melhor["maxWinStreak"], "vitórias seguidas")

# Desafio 3: só o top 10 num CSV
top10 = df.sort_values("trophies", ascending=False).head(10)
top10[["name", "trophies"]].to_csv("top10.csv", index=False, sep=";", encoding="utf-8-sig")
print("\ntop10.csv salvo!")

# Desafio 4 (difícil): em qual modo de jogo o jogador mais ganha?
# O battlelog_exemplo.json está na pasta dados_offline do repositório
batalhas = carregar("battlelog_exemplo.json")

# O json_normalize "achata" o JSON aninhado: battle -> mode vira a coluna battle.mode
partidas = pd.json_normalize(batalhas["items"])

# Alguns modos, como o Combate, usam posição em vez de vitória: ficam de fora
com_resultado = partidas[partidas["battle.result"].notna()]

placar = pd.crosstab(com_resultado["battle.mode"], com_resultado["battle.result"])
print("\nVitórias e derrotas por modo:")
print(placar.sort_values("victory", ascending=False))
print("\nModo com mais vitórias:", placar["victory"].idxmax())
