# Prática 1 - respostas dos desafios
# Minicurso "Consumo de APIs e Análise de Dados na Prática" - SECOMPP26

import requests

# Desafio 1: o CEP da sua casa (troque abaixo: 8 números, sem hífen)
cep = "19060900"
resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/")

if resposta.status_code == 200:
    endereco = resposta.json()
    if "erro" in endereco:
        print("CEP não encontrado!")
    else:
        print(endereco["logradouro"], "-", endereco["bairro"])
        print(endereco["localidade"], "/", endereco["uf"])
else:
    print("CEP inválido. Status:", resposta.status_code)

# Desafios 2 e 3: um pokémon na PokeAPI (o nome vai em minúsculas)
nome = "pikachu"
resposta = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nome}")

if resposta.status_code == 200:
    pokemon = resposta.json()

    # A PokeAPI mede a altura em decímetros e o peso em hectogramas.
    # Dividindo por 10, viram metros e quilos: o pikachu tem 0.4 m e 6.0 kg
    print("Nome:", pokemon["name"])
    print("Altura:", pokemon["height"] / 10, "m")
    print("Peso:", pokemon["weight"] / 10, "kg")
else:
    print("Pokémon não encontrado. Status:", resposta.status_code)
