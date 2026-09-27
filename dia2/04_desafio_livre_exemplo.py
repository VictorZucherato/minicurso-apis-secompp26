# Desafio livre - um exemplo completo
# Minicurso "Consumo de APIs e Análise de Dados na Prática" - SECOMPP26
#
# Pergunta: quantos personagens de Harry Potter são de cada casa?
# API: Harry Potter API, sem chave (hp-api.onrender.com)

import json
import os

import pandas as pd
import requests

url = "https://hp-api.onrender.com/api/characters"

try:
    # Essa API às vezes demora para "acordar": por isso o timeout maior
    resposta = requests.get(url, timeout=30)
    resposta.raise_for_status()
    dados = resposta.json()
    print("Fonte: API ao vivo")
except requests.RequestException:
    # Sem internet: usa a resposta salva no repositório
    pasta_do_script = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta_do_script, "..", "dados_offline", "hpapi_personagens.json")
    with open(caminho, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    print("Fonte: dados salvos")

personagens = pd.DataFrame(dados)
print(len(personagens), "personagens")

# Quem não tem casa vem com "" no campo house
com_casa = personagens[personagens["house"] != ""]
print(com_casa["house"].value_counts())

# Bônus: quantos estudantes de Hogwarts há em cada casa?
estudantes = com_casa.groupby("house")["hogwartsStudent"].sum()
print(estudantes.sort_values(ascending=False))
