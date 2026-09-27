# Prática 3 - Do JSON para a tabela com o pandas
# Minicurso "Consumo de APIs e Análise de Dados na Prática" - SECOMPP26
#
# Versão completa da Prática 3. Ela lê o jogador.json que vocês salvaram
# na segunda. Quem faltou: baixe o dados_offline/jogador_exemplo.json do
# repositório e salve na sua pasta com o nome jogador.json.

import json
import os

import matplotlib.pyplot as plt
import pandas as pd

# 1. Do JSON para a tabela
caminho = "jogador.json"
if not os.path.isfile(caminho):
    # Rodando de dentro do repositório: usa o jogador de exemplo
    pasta_do_script = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta_do_script, "..", "dados_offline", "jogador_exemplo.json")

with open(caminho, encoding="utf-8") as arquivo:
    jogador = json.load(arquivo)

df = pd.DataFrame(jogador["brawlers"])
print(df.head())

# 2. Primeiro olhar
print(df.shape)  # (linhas, colunas)
df.info()
print(df["trophies"].describe())

# 3. Escolhendo colunas e ordenando
colunas = ["name", "power", "trophies", "highestTrophies"]
tabela = df[colunas]

top10 = tabela.sort_values("trophies", ascending=False).head(10)
print(top10)

# 4. Filtrando linhas
fortes = tabela[tabela["trophies"] >= 1100]
print(len(fortes), "brawlers com 1100 troféus ou mais")
print(fortes)

# 5. Coluna nova: quanto cada brawler está abaixo do próprio recorde
df["perdidos"] = df["highestTrophies"] - df["trophies"]

longe = df.sort_values("perdidos", ascending=False)
print(longe[["name", "trophies", "perdidos"]].head())

# 6. Contando e agrupando
print(df["power"].value_counts())

media = df.groupby("power")["trophies"].mean()
print(media)

# 7. Salvando para abrir no Excel ou no LibreOffice
tabela.to_csv("brawlers.csv", index=False,
              sep=";", encoding="utf-8-sig")
print("brawlers.csv salvo!")

# 8. O gráfico da demo
grafico = top10.iloc[::-1]  # o maior fica em cima
plt.barh(grafico["name"], grafico["trophies"])
plt.title("Top 10 brawlers por troféus")
plt.xlabel("Troféus")
plt.tight_layout()
plt.show()
