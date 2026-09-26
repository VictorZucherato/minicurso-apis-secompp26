"""
gerar_dados_offline.py - ferramenta dos instrutores
Minicurso "Consumo de APIs e Análise de Dados na Prática" - SECOMPP26

1. Baixa respostas reais das APIs para a pasta dados_offline/ (o plano C da aula)
2. Testa de uma vez todas as APIs da aula e da lista do desafio livre
3. Mostra os campos que cada resposta tem, para planejar a análise do dia 2

A chave do Brawl Stars fica em token.txt (nesta pasta) ou na variável BRAWL_TOKEN,
e precisa estar cadastrada para o IP de onde este script roda.
Rode com: python gerar_dados_offline.py
"""

import json
import os
import time

import requests

TAG = "#RGVU2J"
PASTA = os.path.dirname(os.path.abspath(__file__))
PASTA_SAIDA = os.path.join(PASTA, "dados_offline")
BASE_BRAWL = "https://api.brawlstars.com/v1"

APIS_PUBLICAS = [
    ("viacep_fct.json", "ViaCEP",
     "https://viacep.com.br/ws/19060900/json/"),
    ("pokeapi_pikachu.json", "PokeAPI",
     "https://pokeapi.co/api/v2/pokemon/pikachu"),
    ("rickandmorty_personagens.json", "Rick and Morty API",
     "https://rickandmortyapi.com/api/character"),
    ("brasilapi_feriados_2026.json", "Brasil API (feriados)",
     "https://brasilapi.com.br/api/feriados/v1/2026"),
    ("brasilapi_ddd_18.json", "Brasil API (DDD 18)",
     "https://brasilapi.com.br/api/ddd/v1/18"),
    ("openmeteo_prudente.json", "Open-Meteo",
     "https://api.open-meteo.com/v1/forecast?latitude=-22.12&longitude=-51.39"
     "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America%2FSao_Paulo"),
    ("coingecko_top10.json", "CoinGecko",
     "https://api.coingecko.com/api/v3/coins/markets?vs_currency=brl&order=market_cap_desc&per_page=10&page=1"),
    ("dogapi_racas.json", "Dog API",
     "https://dog.ceo/api/breeds/list/all"),
    ("hpapi_personagens.json", "Harry Potter API",
     "https://hp-api.onrender.com/api/characters"),
]


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


def carregar(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def baixar(nome_arquivo, url, cabecalhos=None):
    """Baixa uma URL e salva o JSON em dados_offline/. Retorna (deu_certo, detalhe)."""
    try:
        resposta = requests.get(url, headers=cabecalhos, timeout=30)
    except requests.RequestException as erro:
        return False, f"sem conexão ({type(erro).__name__})"

    if resposta.status_code != 200:
        try:
            corpo = resposta.json()
            motivo = f"{corpo.get('reason', '')} {corpo.get('message', '')}".strip()
        except ValueError:
            motivo = ""
        return False, f"status {resposta.status_code} {motivo[:150]}".strip()

    try:
        dados = resposta.json()
    except ValueError:
        return False, "a resposta não é JSON"

    with open(os.path.join(PASTA_SAIDA, nome_arquivo), "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    return True, f"{nome_arquivo} ({len(resposta.content) / 1024:.0f} KB)"


def baixar_brawl_stars(token):
    cabecalhos = {"Authorization": f"Bearer {token}"}
    tag_url = TAG.replace("#", "%23")
    resultados = []

    for nome_arquivo, rotulo, caminho in [
        ("jogador_exemplo.json", "Brawl Stars: jogador", f"/players/{tag_url}"),
        ("battlelog_exemplo.json", "Brawl Stars: battlelog", f"/players/{tag_url}/battlelog"),
        ("brawlers.json", "Brawl Stars: brawlers", "/brawlers"),
    ]:
        deu_certo, detalhe = baixar(nome_arquivo, BASE_BRAWL + caminho, cabecalhos)
        resultados.append((rotulo, deu_certo, detalhe))
        time.sleep(0.3)

    # Os slides usam "br" minúsculo no ranking: se não funcionar, testa "BR"
    for codigo in ("br", "BR"):
        url = f"{BASE_BRAWL}/rankings/{codigo}/players?limit=10"
        deu_certo, detalhe = baixar("ranking_br_exemplo.json", url, cabecalhos)
        resultados.append((f"Brawl Stars: ranking ({codigo})", deu_certo, detalhe))
        if deu_certo:
            break
        time.sleep(0.3)

    return resultados


def mostrar_campos():
    print("\nCAMPOS DISPONÍVEIS (para planejar o dia 2)")
    print("-" * 72)

    caminho = os.path.join(PASTA_SAIDA, "jogador_exemplo.json")
    if os.path.isfile(caminho):
        jogador = carregar(caminho)
        print("Jogador:", ", ".join(jogador.keys()))
        if jogador.get("brawlers"):
            print("Cada brawler do jogador:", ", ".join(jogador["brawlers"][0].keys()))
            print("Brawlers desbloqueados pelo jogador:", len(jogador["brawlers"]))

    caminho = os.path.join(PASTA_SAIDA, "brawlers.json")
    if os.path.isfile(caminho):
        itens = carregar(caminho).get("items", [])
        if itens:
            print("Cada item de /brawlers:", ", ".join(itens[0].keys()))
            print("Brawlers no jogo:", len(itens))

    caminho = os.path.join(PASTA_SAIDA, "battlelog_exemplo.json")
    if os.path.isfile(caminho):
        batalhas = carregar(caminho).get("items", [])
        if batalhas:
            print("Cada batalha (campo battle):", ", ".join(batalhas[0].get("battle", {}).keys()))
            print("Batalhas no battlelog:", len(batalhas))


def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    resultados = []

    token = ler_token()
    if token:
        resultados += baixar_brawl_stars(token)
    else:
        resultados.append(("Brawl Stars", False, "sem chave (defina BRAWL_TOKEN ou crie o token.txt)"))

    for nome_arquivo, rotulo, url in APIS_PUBLICAS:
        deu_certo, detalhe = baixar(nome_arquivo, url)
        resultados.append((rotulo, deu_certo, detalhe))
        time.sleep(0.3)

    print("\nRESULTADO")
    print("-" * 72)
    for rotulo, deu_certo, detalhe in resultados:
        marca = "OK    " if deu_certo else "FALHOU"
        print(f"[{marca}] {rotulo:<28} {detalhe}")

    mostrar_campos()


if __name__ == "__main__":
    main()
