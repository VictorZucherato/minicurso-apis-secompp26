"""
verificar_ambiente.py
Minicurso "Consumo de APIs e Análise de Dados na Prática" - SECOMPP26

Rode com:  python verificar_ambiente.py
           (no Windows também funciona "py verificar_ambiente.py"; no Mac, "python3")
Não precisa de nenhuma biblioteca externa para rodar.
Rode logado com o MESMO usuário que o participante vai usar.
"""

import importlib
import json
import os
import platform
import sys
import urllib.error
import urllib.request

# IPs cadastrados na chave do minicurso (se criar uma chave nova, atualize aqui)
IPS_DA_CHAVE = ["200.145.184.170"]

OK = "[ OK ]"
FALHA = "[FALHOU]"
AVISO = "[AVISO]"

problemas = []
avisos = []


def registrar(lista, mensagem):
    if mensagem not in lista:
        lista.append(mensagem)


def titulo(texto):
    print("\n" + "=" * 60)
    print(texto)
    print("=" * 60)


def requisitar(url, cabecalhos=None, timeout=10):
    """Faz um GET com requests (se estiver instalada) ou com urllib. Retorna (status, corpo)."""
    cabecalhos = cabecalhos or {}
    try:
        import requests
    except ImportError:
        requests = None

    if requests is not None:
        resposta = requests.get(url, headers=cabecalhos, timeout=timeout)
        return resposta.status_code, resposta.text

    pedido = urllib.request.Request(url, headers=cabecalhos)
    try:
        with urllib.request.urlopen(pedido, timeout=timeout) as resposta:
            return resposta.status, resposta.read().decode("utf-8")
    except urllib.error.HTTPError as erro:
        return erro.code, erro.read().decode("utf-8", errors="ignore")


def erro_de_certificado(erro):
    return "CERTIFICATE_VERIFY_FAILED" in str(erro) or "SSL" in type(erro).__name__


def ler_token():
    """Lê a chave de BRAWL_TOKEN ou do token.txt (aceita só a chave ou a linha TOKEN = "...")."""
    texto = os.getenv("BRAWL_TOKEN", "")
    pasta_do_script = os.path.dirname(os.path.abspath(__file__))
    for caminho in ("token.txt", os.path.join(pasta_do_script, "token.txt")):
        if not texto.strip() and os.path.isfile(caminho):
            with open(caminho, "r", encoding="utf-8") as arquivo:
                texto = arquivo.read()
    texto = texto.strip()
    if texto.upper().startswith("TOKEN") and "=" in texto:
        texto = texto.split("=", 1)[1]
    return texto.strip().strip('"').strip("'")


# ------------------------------------------------------------------
titulo("1. SISTEMA E PYTHON")
print(f"Sistema operacional: {platform.system()} {platform.release()}")
print(f"Usuário logado:      {os.getenv('USER') or os.getenv('USERNAME')}")
print(f"Pasta do usuário:    {os.path.expanduser('~')}")
print(f"Executável Python:   {sys.executable}")

versao = sys.version_info
if versao >= (3, 10):
    print(f"{OK} Python {versao.major}.{versao.minor}.{versao.micro}")
else:
    print(f"{FALHA} Python {versao.major}.{versao.minor} (precisa ser 3.10 ou superior)")
    registrar(problemas, "Python abaixo da versão 3.10")

# ------------------------------------------------------------------
titulo("2. BIBLIOTECAS")
bibliotecas = {
    "requests": True,     # obrigatória
    "pandas": True,       # obrigatória
    "matplotlib": False,  # opcional (gráfico do dia 2)
}

for nome, obrigatoria in bibliotecas.items():
    try:
        modulo = importlib.import_module(nome)
        print(f"{OK} {nome} {getattr(modulo, '__version__', '')}")
    except ImportError:
        if obrigatoria:
            print(f"{FALHA} {nome} NÃO instalada")
            registrar(problemas, f"Biblioteca {nome} não instalada para este usuário")
        else:
            print(f"{AVISO} {nome} não instalada (opcional)")
            registrar(avisos, f"Biblioteca {nome} não instalada (opcional)")

# ------------------------------------------------------------------
titulo("3. INTERNET E APIs")
testes = {
    "ViaCEP": "https://viacep.com.br/ws/19060900/json/",
    "PokeAPI": "https://pokeapi.co/api/v2/pokemon/pikachu",
    "Brawl Stars": "https://api.brawlstars.com/v1/brawlers",
}

for nome, url in testes.items():
    try:
        status, _ = requisitar(url)
        if nome == "Brawl Stars" and status == 403:
            # Sem chave, 403 é o esperado: significa que o servidor foi alcançado
            print(f"{OK} {nome} alcançável (403 sem chave é o esperado)")
        elif status == 200:
            print(f"{OK} {nome} respondeu {status}")
        else:
            print(f"{AVISO} {nome} respondeu {status}")
            registrar(avisos, f"API {nome} respondeu com status {status}")
    except Exception as erro:
        if erro_de_certificado(erro):
            print(f"{FALHA} {nome}: erro de certificado SSL")
            registrar(problemas, "Erro de certificado SSL (no Mac: rodar 'Install Certificates.command' na pasta do Python, em Aplicativos)")
        else:
            print(f"{FALHA} {nome}: {erro}")
            registrar(problemas, f"Sem acesso à API {nome} (internet, proxy ou firewall)")

# ------------------------------------------------------------------
titulo("4. IP PÚBLICO (a chave do Brawl Stars depende dele)")
try:
    status, corpo = requisitar("https://api.ipify.org?format=json")
    ip_publico = json.loads(corpo)["ip"]
    print(f"{OK} IP público desta máquina: {ip_publico}")
    if ip_publico in IPS_DA_CHAVE:
        print(f"{OK} Este IP está cadastrado na chave do minicurso")
    else:
        print(f"{AVISO} Este IP NÃO está na chave do minicurso ({', '.join(IPS_DA_CHAVE)})")
        print("      Avise um instrutor: a API do Brawl Stars vai responder 403 nesta máquina")
        registrar(avisos, f"IP {ip_publico} fora da chave do minicurso (avisar um instrutor)")
except Exception as erro:
    print(f"{FALHA} Não foi possível descobrir o IP público: {erro}")
    registrar(avisos, "IP público não identificado (abrir api.ipify.org no navegador)")

# ------------------------------------------------------------------
titulo("5. PERMISSÃO DE ESCRITA NA PASTA ATUAL")
arquivo_teste = "teste_escrita_minicurso.json"
try:
    with open(arquivo_teste, "w", encoding="utf-8") as arquivo:
        json.dump({"teste": True}, arquivo)
    os.remove(arquivo_teste)
    print(f"{OK} É possível salvar arquivos em: {os.getcwd()}")
except Exception as erro:
    print(f"{FALHA} Não é possível salvar arquivos aqui: {erro}")
    registrar(problemas, "Sem permissão de escrita na pasta atual")

# ------------------------------------------------------------------
titulo("6. EXTENSÃO PYTHON DO VS CODE (neste usuário)")
pasta_extensoes = os.path.join(os.path.expanduser("~"), ".vscode", "extensions")
if os.path.isdir(pasta_extensoes):
    extensoes_python = [
        nome for nome in os.listdir(pasta_extensoes)
        if nome.lower().startswith("ms-python.python")
    ]
    if extensoes_python:
        print(f"{OK} Extensão Python encontrada: {extensoes_python[0]}")
    else:
        print(f"{AVISO} VS Code existe neste usuário, mas SEM a extensão Python")
        print("      Instalar: abrir o VS Code > Extensões (Ctrl+Shift+X) > buscar 'Python' (Microsoft)")
        registrar(avisos, "Extensão Python do VS Code não instalada neste usuário")
else:
    print(f"{AVISO} O VS Code nunca foi aberto por este usuário (ou não está instalado)")
    print("      Abrir o VS Code uma vez e instalar a extensão 'Python' da Microsoft")
    print("      Se você usa outra IDE (como o Antigravity), pode ignorar este aviso")
    registrar(avisos, "VS Code sem extensões neste usuário (abrir e instalar a extensão Python)")

# ------------------------------------------------------------------
titulo("7. CHAVE DO BRAWL STARS (só para os instrutores)")
token = ler_token()
if not token:
    print("      Nenhum token.txt encontrado: teste pulado (participantes não precisam disso)")
else:
    try:
        status, corpo = requisitar(
            "https://api.brawlstars.com/v1/rankings/br/players?limit=1",
            {"Authorization": f"Bearer {token}"},
        )
        if status == 200:
            print(f"{OK} A chave funciona nesta máquina")
        else:
            try:
                detalhe = json.loads(corpo)
                motivo = f"{detalhe.get('reason')}: {detalhe.get('message')}"
            except ValueError:
                motivo = corpo[:200]
            print(f"{FALHA} A API respondeu {status} ({motivo})")
            registrar(problemas, f"Chave do Brawl Stars recusada nesta máquina: {motivo}")
    except Exception as erro:
        print(f"{FALHA} Não foi possível testar a chave: {erro}")
        registrar(problemas, "Não foi possível testar a chave do Brawl Stars")

# ------------------------------------------------------------------
titulo("RESULTADO")
if problemas:
    print("Problemas que IMPEDEM o minicurso nesta máquina:")
    for problema in problemas:
        print(f"  - {problema}")
if avisos:
    print("\nAvisos (dá para resolver na hora, sem administrador):")
    for aviso in avisos:
        print(f"  - {aviso}")
if not problemas and not avisos:
    print("Tudo certo! Esta máquina está pronta para o minicurso.")
elif not problemas:
    print("\nNenhum problema grave. Esta máquina pode ser usada no minicurso.")
print()
