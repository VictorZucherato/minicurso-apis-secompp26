# Prática 2 - Entrando no Brawl Stars
# Minicurso "Consumo de APIs e Análise de Dados na Prática" - SECOMPP26
#
# Versão completa da Prática 2. Se você se perdeu, copie este código
# para o seu arquivo, troque a linha do TOKEN e continue daqui.

import json

import requests

# Troque esta linha pela linha que está no documento da chave
TOKEN = "COLE_A_CHAVE_AQUI"
cabecalhos = {"Authorization": f"Bearer {TOKEN}"}

# 1. Mandando o crachá junto com o pedido: o top 5 do Brasil
url = "https://api.brawlstars.com/v1/rankings/br/players?limit=5"
resposta = requests.get(url, headers=cabecalhos)

print(resposta.status_code)
print(resposta.json())

# 2. O problema da #: na URL, a # vira %23
tag = "#RGVU2J"
tag_url = tag.replace("#", "%23")
url = f"https://api.brawlstars.com/v1/players/{tag_url}"

# 3. Buscando um jogador
resposta = requests.get(url, headers=cabecalhos)

if resposta.status_code == 200:
    jogador = resposta.json()

    # 4. Navegando no JSON do jogador
    print("Nome:", jogador["name"])
    print("Troféus:", jogador["trophies"])
    print("Recorde:", jogador["highestTrophies"])
    print("Clube:", jogador.get("club", {}).get("name", "Sem clube"))
    print("Brawlers:", len(jogador["brawlers"]))

    for brawler in jogador["brawlers"]:
        print(brawler["name"], "-", brawler["trophies"], "troféus")

    # 5. Guardando os dados para quarta
    with open("jogador.json", "w", encoding="utf-8") as arquivo:
        json.dump(jogador, arquivo, ensure_ascii=False, indent=2)

    print("Arquivo salvo!")
else:
    # Quando dá erro, a API do Brawl Stars explica o motivo no próprio JSON
    print("Erro:", resposta.status_code)
    print(resposta.json())
