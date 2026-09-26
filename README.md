# Consumo de APIs e Análise de Dados na Prática

Minicurso da SECOMPP26 (FCT/Unesp), com Felipe Giovaneli e Victor Zucherato.

## Como pegar o código

- Para copiar um arquivo: clique nele, depois no botão de copiar (canto superior direito do código)
- Para baixar tudo: botão verde **Code** > **Download ZIP** e extraia a pasta

## O que tem aqui

| Arquivo | Para que serve |
|---|---|
| `verificar_ambiente.py` | Confere se o computador está pronto para o minicurso |
| `demo.py` | A demonstração da abertura: API, tabela, perguntas e gráfico |
| `dia1/01_primeira_requisicao.py` | Prática 1 completa (ViaCEP) |
| `dia1/desafios_pratica1.py` | Respostas dos desafios da Prática 1 |
| `dia1/02_brawlstars.py` | Prática 2 completa (Brawl Stars com chave) |
| `dia1/desafios_pratica2.py` | Respostas dos desafios da Prática 2 |
| `dia1/plano_c_offline.py` | A Prática 2 sem internet, lendo o `jogador_exemplo.json` |
| `dados_offline/` | Respostas reais das APIs, salvas para usar sem internet |
| `gerar_dados_offline.py` | Ferramenta dos instrutores: atualiza a pasta `dados_offline/` |

## Como rodar

- **No VS Code:** abra o arquivo e clique no ▶ no canto superior direito
- **No terminal:** `python nome_do_arquivo.py` (no Windows, também funciona `py`; no Mac, use `python3`)

## Para usar no seu notebook

Instale as bibliotecas uma vez:

```
pip install -r requirements.txt
```

## Sobre a chave do Brawl Stars

- A chave usada em aula só funciona no laboratório e será apagada ao fim do minicurso
- Para continuar em casa, crie a sua em [developer.brawlstars.com](https://developer.brawlstars.com), cadastrando o IP da sua casa
- Nunca publique a sua chave no GitHub. Os scripts dos instrutores leem a chave de um arquivo `token.txt` ou da variável `BRAWL_TOKEN`, e o `token.txt` está no `.gitignore`
