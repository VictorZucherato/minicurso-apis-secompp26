# Prática 1 - A primeira requisição em Python
# Minicurso "Consumo de APIs e Análise de Dados na Prática" - SECOMPP26
#
# Versão completa da Prática 1. Se você se perdeu, copie este código
# para o seu arquivo e continue daqui.

import requests

# O CEP vai sem hífen: são 8 números. Este é o CEP da FCT/Unesp
url = "https://viacep.com.br/ws/19060900/json/"
resposta = requests.get(url)

# Sempre confira o status primeiro
if resposta.status_code == 200:
    dados = resposta.json()

    # Nem todo 200 é sucesso: um CEP que não existe (exemplo: 99999999)
    # também devolve 200, mas com {"erro": "true"} dentro
    if "erro" in dados:
        print("CEP não encontrado!")
    else:
        print("Rua:", dados["logradouro"])
        print("Bairro:", dados["bairro"])
        print("Cidade:", dados["localidade"])
else:
    # Um CEP com formato inválido (exemplo: 12345) devolve 400
    print("Deu erro! Status:", resposta.status_code)
