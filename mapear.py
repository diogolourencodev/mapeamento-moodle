import requests
from bs4 import BeautifulSoup
import random
import json
import os
import sys
from datetime import datetime

# NAO ESQUECA DE CRIAR UM ARQUIVO 'alunos.json'
# CREDENCIAIS DO SITE MOODLE
LOGIN = "LOGIN"
PASSWORD = "PASSWORD"

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:117.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.131 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.105 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.136 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.128 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.70 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36"
]

print(f'\n[*] Iniciando sessão...')
session = requests.Session()

moodle_login_url = "https://moodle.univassouras.edu.br/login/index.php"

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.131 Mobile Safari/537.36'
}

print(f'[*] Adquirindo logintoken...')

res = session.get(moodle_login_url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
token_tag = soup.find("input", {"name": "logintoken"})

logintoken = token_tag["value"]

print(f'[*] Login Token Moodle: {logintoken}')

login_data = {
    "username": LOGIN,
    "password": PASSWORD,
    "logintoken": logintoken
}

print(f'[*] Adquirindo Cookies...')

login_response = session.post(moodle_login_url, data=login_data, headers=headers)

moodle_url = 'https://moodle.univassouras.edu.br/user/profile.php?id='
headers = {
    'User-Agent': random.choice(user_agents)
}

for cookie in session.cookies:
    cookies = f"{cookie.name}={cookie.value}"

print(f'[*] Sessão iniciada em {cookies}. \n\n[*] Iniciando mapeamento...\n')

json_file = 'usuarios.json'

if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
    with open(json_file, 'r', encoding='utf-8') as f:
        alunos = json.load(f)
else:
    alunos = {}

id_i = 0000000

ids_invalidos = set()
if os.path.exists('invalidos.txt'):
    with open('invalidos.txt', 'r', encoding='utf-8') as invfile:
        for linha in invfile:
            linha_limpa = linha.strip()
            if linha_limpa:
                ids_invalidos.add(linha_limpa)

def formatar_status(tipo, id_num, adicional=""):
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if tipo == "INVALIDO":
        return f"[{timestamp}] | SKIP | ID {id_num:<8} | Status: Usuário inválido"
    elif tipo == "COLETADO":
        return f"[{timestamp}] | SKIP | ID {id_num:<8} | Status: Já coletado anteriormente"
    elif tipo == "ENCONTRADO":
        return f"[{timestamp}] | SAVE | ID {id_num:<8} | Aluno: {adicional}"
    elif tipo == "ERRO":
        return f"[{timestamp}] | ERR  | ID {id_num:<8} | Erro: {adicional}"
    elif tipo == "NAO_ENCONTRADO":
        return f"[{timestamp}] | FAIL | ID {id_num:<8} | Elemento não encontrado: {adicional}"

def limpar_e_imprimir(mensagem, limpar_linha=False):
    if limpar_linha:
        print(' ' * 100, end='\r')
    print(mensagem, end='\r' if limpar_linha else '\n')

while True:
    if str(id_i) == "0":
        id_i += 1
        continue

    if str(id_i) in ids_invalidos:
        mensagem = formatar_status("INVALIDO", id_i)
        limpar_e_imprimir(mensagem, limpar_linha=True)
        id_i += 1
        continue

    if str(id_i) in alunos:
        mensagem = formatar_status("COLETADO", id_i)
        limpar_e_imprimir(mensagem, limpar_linha=True)
        id_i += 1
        continue

    flink = f"{moodle_url}{id_i}"
    
    try:
        response = session.get(flink, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        section = soup.find('section', id='region-main')
        div = soup.find('div', class_='card card-body card-profile')

        if section:
            if "Usuário inválido" in section.get_text():
                mensagem = formatar_status("INVALIDO", id_i)
                limpar_e_imprimir(mensagem, limpar_linha=True)
                ids_invalidos.add(str(id_i))
                with open('invalidos.txt', 'a', encoding='utf-8') as invfile:
                    invfile.write(str(id_i) + '\n')
                id_i += 1
            else:
                if div:
                    h3 = div.find('h3')
                    if h3:
                        nome = h3.get_text().strip()
                        print(formatar_status("ENCONTRADO", id_i, nome))

                        alunos[str(id_i)] = nome

                        with open(json_file, 'w', encoding='utf-8') as f:
                            json.dump(alunos, f, ensure_ascii=False, indent=4)

                        id_i += 1
                    else:
                        mensagem = formatar_status("INVALIDO", id_i)
                        limpar_e_imprimir(mensagem, limpar_linha=True)
                        ids_invalidos.add(str(id_i))
                        with open('invalidos.txt', 'a', encoding='utf-8') as invfile:
                            invfile.write(str(id_i) + '\n')
                        id_i += 1
                else:
                    mensagem = formatar_status("INVALIDO", id_i)
                    limpar_e_imprimir(mensagem, limpar_linha=True)
                    ids_invalidos.add(str(id_i))
                    with open('invalidos.txt', 'a', encoding='utf-8') as invfile:
                        invfile.write(str(id_i) + '\n')
                    id_i += 1
        else:
            mensagem = formatar_status("INVALIDO", id_i)
            limpar_e_imprimir(mensagem, limpar_linha=True)
            ids_invalidos.add(str(id_i))
            with open('invalidos.txt', 'a', encoding='utf-8') as invfile:
                invfile.write(str(id_i) + '\n')
            id_i += 1

    except Exception as e:
        print(formatar_status("ERRO", id_i, str(e)))
        id_i += 1
