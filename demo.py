"""
demo.py - "Até quarta, vocês vão escrever isto"
Minicurso "Consumo de APIs e Análise de Dados na Prática" - SECOMPP26

Busca um jogador na API do Brawl Stars, transforma a lista de brawlers
numa tabela (pandas), responde algumas perguntas e desenha um gráfico.

A chave é lida do arquivo token.txt (nesta mesma pasta) ou da variável BRAWL_TOKEN.
Se a API não responder, a demo usa dados_offline/jogador_exemplo.json sozinha.
"""

import json
import os

import pandas as pd
import requests

TAG = "#2002JY88"
PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_OFFLINE = os.path.join(PASTA, "dados_offline", "jogador_exemplo.json")


def ler_token():
    """Lê a chave de BRAWL_TOKEN ou do token.txt (aceita só a chave ou a linha TOKEN = "...")."""
    texto = os.getenv("BRAWL_TOKEN", "")
    caminho = os.path.join(PASTA, "token.txt")
    if not texto.strip() and os.path.isfile(caminho):
        with open(caminho, "r", encoding="utf-8") as arquivo:
            texto = arquivo.read()
    texto = texto.strip()
    if texto.upper().startswith("TOKEN") and "=" in texto:
        texto = texto.split("=", 1)[1]
    return texto.strip().strip('"').strip("'")


def buscar_jogador(tag):
    """Tenta a API ao vivo. Se não der certo, usa os dados salvos."""
    token = ler_token()
    if token:
        url = "https://api.brawlstars.com/v1/players/" + tag.replace("#", "%23")
        cabecalhos = {"Authorization": f"Bearer {token}"}
        try:
            resposta = requests.get(url, headers=cabecalhos, timeout=10)
            if resposta.status_code == 200:
                return resposta.json(), "API ao vivo"
            print(f"(a API respondeu {resposta.status_code}: usando os dados salvos)")
        except requests.RequestException:
            print("(sem conexão com a API: usando os dados salvos)")
    with open(ARQUIVO_OFFLINE, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo), "dados salvos"


# 1. COLETAR
jogador, origem = buscar_jogador(TAG)

print("=" * 55)
print(f"{jogador['name']} ({jogador['tag']})  |  fonte: {origem}")
print(f"Troféus: {jogador['trophies']}  |  Recorde: {jogador['highestTrophies']}")
print(f"Clube: {jogador.get('club', {}).get('name', 'Sem clube')}")
print("=" * 55)

# 2. ORGANIZAR: a lista de brawlers vira uma tabela
tabela = pd.DataFrame(jogador["brawlers"])
tabela = tabela[["name", "power", "trophies", "highestTrophies"]]
tabela.columns = ["Brawler", "Power", "Troféus", "Recorde"]
tabela["Brawler"] = tabela["Brawler"].str.title()

# 3. PERGUNTAR E RESPONDER
print(f"\nBrawlers desbloqueados: {len(tabela)}")
print(f"Média de troféus por brawler: {tabela['Troféus'].mean():.0f}")
print(f"Brawlers no power 11 (o máximo): {(tabela['Power'] == 11).sum()}")

top10 = tabela.sort_values("Troféus", ascending=False).head(10)
print("\nTop 10 brawlers por troféus:")
print(top10.to_string(index=False))

total = tabela["Troféus"].sum()
if total > 0:
    fatia = top10["Troféus"].sum() / total * 100
    print(f"\nOs 10 melhores somam {fatia:.0f}% dos troféus de todos os brawlers")

# 4. VISUALIZAR
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("\n(matplotlib não está instalado: o gráfico fica para quarta)")
else:
    grafico = top10.iloc[::-1]  # inverte para o maior ficar em cima
    nome = jogador["name"].replace("$", r"\$")

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.barh(grafico["Brawler"], grafico["Troféus"], height=0.6, color="#009688")
    ax.set_title(f"Top 10 brawlers de {nome} por troféus", loc="left",
                 fontsize=14, color="#1f1f1f", pad=12)
    ax.set_xlabel("Troféus", color="#5f5f5f")
    ax.tick_params(axis="x", colors="#5f5f5f", length=0)
    ax.tick_params(axis="y", colors="#1f1f1f", length=0, labelsize=11)
    ax.grid(axis="x", color="#e6e6e6", linewidth=1)
    ax.set_axisbelow(True)
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_color("#d0d0d0")

    # Só o maior valor ganha rótulo; os outros estão na tabela acima
    maior = top10.iloc[0]
    ax.text(maior["Troféus"], len(grafico) - 1, f"  {maior['Troféus']}",
            va="center", color="#1f1f1f", fontsize=11, fontweight="bold")
    ax.margins(x=0.1)

    fig.tight_layout()
    fig.savefig(os.path.join(PASTA, "grafico_demo.png"), dpi=150)
    plt.show()
