# Prática 2 - respostas dos desafios
# Minicurso "Consumo de APIs e Análise de Dados na Prática" - SECOMPP26

import requests

# Troque esta linha pela linha que está no documento da chave
TOKEN = "COLE_A_CHAVE_AQUI"
cabecalhos = {"Authorization": f"Bearer {TOKEN}"}
BASE = "https://api.brawlstars.com/v1"


def buscar(url):
    """Faz o GET com a chave e devolve o JSON (ou None, se der erro)."""
    resposta = requests.get(url, headers=cabecalhos)
    if resposta.status_code == 200:
        return resposta.json()
    print("Erro:", resposta.status_code, resposta.json())
    return None


# Desafio 1: troque pela sua tag (no jogo, ela aparece no seu perfil)
tag = "#2002JY88"
tag_url = tag.replace("#", "%23")

# Desafio 2: o brawler com mais troféus
jogador = buscar(f"{BASE}/players/{tag_url}")
if jogador:
    melhor = jogador["brawlers"][0]
    for brawler in jogador["brawlers"]:
        if brawler["trophies"] > melhor["trophies"]:
            melhor = brawler
    print("Brawler com mais troféus:", melhor["name"], "-", melhor["trophies"], "troféus")

# Desafio 3: o top 10 do Brasil
ranking = buscar(f"{BASE}/rankings/br/players?limit=10")
if ranking:
    print("\nTop 10 do Brasil:")
    posicao = 1
    for item in ranking["items"]:
        print(f"{posicao}. {item['name']} - {item['trophies']} troféus")
        posicao += 1

# Desafio 4 (difícil): vitórias e derrotas nas últimas partidas
batalhas = buscar(f"{BASE}/players/{tag_url}/battlelog")
if batalhas:
    vitorias = 0
    derrotas = 0
    outras = 0  # empates e modos que usam posição em vez de vitória, como o Combate
    for item in batalhas["items"]:
        resultado = item.get("battle", {}).get("result")
        if resultado == "victory":
            vitorias += 1
        elif resultado == "defeat":
            derrotas += 1
        else:
            outras += 1
    print(f"\nÚltimas {len(batalhas['items'])} partidas:")
    print(f"{vitorias} vitórias, {derrotas} derrotas e {outras} outras")
