# Plano C - a Prática 2 sem internet (ou sem chave)
# Minicurso "Consumo de APIs e Análise de Dados na Prática" - SECOMPP26
#
# Use quando a API do Brawl Stars não estiver respondendo:
# 1. No repositório, abra dados_offline/jogador_exemplo.json e baixe o arquivo
# 2. Salve na sua pasta, a mesma deste script
# 3. Rode: daqui para baixo, é igual à Prática 2

import json
import os


def carregar_offline(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


caminho = "jogador_exemplo.json"
if not os.path.isfile(caminho):
    # Rodando de dentro do repositório: o arquivo está na pasta dados_offline
    pasta_do_script = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta_do_script, "..", "dados_offline", "jogador_exemplo.json")

jogador = carregar_offline(caminho)

print("Nome:", jogador["name"])
print("Troféus:", jogador["trophies"])
print("Recorde:", jogador["highestTrophies"])
print("Clube:", jogador.get("club", {}).get("name", "Sem clube"))
print("Brawlers:", len(jogador["brawlers"]))

for brawler in jogador["brawlers"]:
    print(brawler["name"], "-", brawler["trophies"], "troféus")

# Salva o jogador.json do mesmo jeito que a Prática 2, para usar na quarta
with open("jogador.json", "w", encoding="utf-8") as arquivo:
    json.dump(jogador, arquivo, ensure_ascii=False, indent=2)

print("Arquivo salvo!")
