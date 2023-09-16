import httpx
import random
import colorama
from keyauth import api
import time
from eemail import TempMailGenerator
import os
import asyncio
import string
import webbrowser
import json
import hashlib
import sys

CONFIG_FILE_PATH = "config.json"

DEFAULT_AVATAR_URL = "https://cdn.discordapp.com/icons/1107824834181877792/10376ec9f920f757c50724ae0d48dc2e.png?size=2048"
DEFAULT_WEBHOOK_NAME = "OneWay Checker"
DEFAULT_DELAY = 8
DEFAULT_WEBHOOK_URL = "SUA WEBHOOK AQUI"
DEFAULT_USERNAME_LENGTH = 4

delay = DEFAULT_DELAY
webhook_url = DEFAULT_WEBHOOK_URL
avatar_url = DEFAULT_AVATAR_URL
username_length = DEFAULT_USERNAME_LENGTH
webhook_name = DEFAULT_WEBHOOK_NAME

is_logged_in = False

ENDPOINT = "https://xboxgamertag.com/search/"

def clear():
    if platform.system() == 'Windows':
        os.system('title OneWay Tools') 

def getchecksum():
    md5_hash = hashlib.md5()
    file = open(''.join(sys.argv), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest


keyauthapp = api(
    name = "OneWay",
    ownerid = "LDdcY26bEq",
    secret = "42b933faea8c4208a7dd9f70f13f5b313e221e36534a88edd6d391e7415bf53a",
    version = "1.0",
    hash_to_check = getchecksum()
)

def generate_random_username(length=None):
    if length is None:
        length = username_length

    characters = string.ascii_letters + string.digits
    while True:
        username = ''.join(random.choice(characters) for _ in range(length))
        if not username[0].isdigit():
            return username

def check(username, length=None, proxy=""):
    if length is None:
        length = username_length

    if proxy != "":
        r = httpx.head(endpoint + username, proxies={proxy.split('|')[0]: proxy.split('|')[1].strip('\n')},
                      headers={'User-Agent': 'Mozilla/5.0 (Kanye) West/5.765 Ye/42.1 (mov-ebx/username-checker on git hub)'})
    else:
        r = httpx.head(ENDPOINT + username,
              headers={'User-Agent': 'Mozilla/5.0 (Kanye) West/5.765 Ye/42.1 (mov-ebx/username-checker on git hub)'})

    if r.status_code == 429:
        time.sleep(5)
        return check(username=username, length=length, proxy=proxy)
    elif r.status_code == 404:
        return username
    return None

def carregar_configuracoes():
    global webhook_url, avatar_url, webhook_name, delay, username_length 

    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r") as config_file:
            config_data = json.load(config_file)
            webhook_url = config_data.get("webhook_url", DEFAULT_WEBHOOK_URL)      
            avatar_url = config_data.get("avatar_url", DEFAULT_AVATAR_URL)
            webhook_name = config_data.get("webhook_name", DEFAULT_WEBHOOK_NAME)
            delay = int(config_data.get("default_delay", DEFAULT_DELAY))
            username_length = int(config_data.get("username_length", DEFAULT_USERNAME_LENGTH)) 

def salvar_configuracoes():
    config_data = {
        "webhook_url": webhook_url,
        "default_delay": delay,
        "avatar_url": avatar_url,
        "webhook_name": webhook_name,
        "username_length": username_length 
    }
    with open(CONFIG_FILE_PATH, "w") as config_file:
        json.dump(config_data, config_file, indent=4)

def send_discord_webhook(username, webhook_url):
    embed_data = {
        "embeds": [
            {
                "title": f"Conta Encontrada! - {username}",
                "description": f"Clique [aqui](https://social.xbox.com/changegamertag) para mudar sua gamertag.",
                "color": 3447003,
                "footer": {
                    "text": webhook_name
                }
            }
        ],
        "username": webhook_name,
        "avatar_url": avatar_url
    }
    payload = json.dumps(embed_data)
    headers = {"Content-Type": "application/json"}
    httpx.post(webhook_url, data=payload, headers=headers)

def answer():
    global is_logged_in 
    try:
        if is_logged_in:
            show_menu()
            return

        os.system('cls & title OneWay Tools')
        ascii_art = colorama.Fore.MAGENTA + """
 ▒█████   ███▄    █ ▓█████  █     █░ ▄▄▄     ▓██   ██▓
▒██▒  ██▒ ██ ▀█   █ ▓█   ▀ ▓█░ █ ░█░▒████▄    ▒██  ██▒
▒██░  ██▒▓██  ▀█ ██▒▒███   ▒█░ █ ░█ ▒██  ▀█▄   ▒██ ██░
▒██   ██░▓██▒  ▐▌██▒▒▓█  ▄ ░█░ █ ░█ ░██▄▄▄▄██  ░ ▐██▓░
░ ████▓▒░▒██░   ▓██░░▒████▒░░██▒██▓  ▓█   ▓██▒ ░ ██▒▓░
░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▓░▒ ▒   ▒▒   ▓▒█░  ██▒▒▒ 
  ░ ▒ ▒░ ░ ░░   ░ ▒░ ░ ░  ░  ▒ ░ ░    ▒   ▒▒ ░▓██ ░▒░ 
░ ░ ░ ▒     ░   ░ ░    ░     ░   ░    ░   ▒   ▒ ▒ ░░  
    ░ ░           ░    ░  ░    ░          ░  ░░ ░     
                                              ░ ░     
            1.Login         2.Register

        """ + colorama.Style.RESET_ALL

        print(ascii_art)  # Print the ASCII art

        ans = input("Selecione uma Opção: ")
        if ans == "1":
            user = input('Provide username: ')
            password = input('Provide password: ')
            keyauthapp.login(user, password)
            is_logged_in = True  # Defina a variável como True após o login
        elif ans == "2":
            user = input('Provide username: ')
            password = input('Provide password: ')
            license = input('Provide License: ')
            keyauthapp.register(user, password, license)
        else:
            print("\nOpção invalida")
            time.sleep(1)
            clear()
            answer()
    except KeyboardInterrupt:
        os._exit(1)

def show_menu():
    os.system('cls')
    ascii_art = colorama.Fore.MAGENTA + """
 ▒█████   ███▄    █ ▓█████  █     █░ ▄▄▄     ▓██   ██▓
▒██▒  ██▒ ██ ▀█   █ ▓█   ▀ ▓█░ █ ░█░▒████▄    ▒██  ██▒
▒██░  ██▒▓██  ▀█ ██▒▒███   ▒█░ █ ░█ ▒██  ▀█▄   ▒██ ██░
▒██   ██░▓██▒  ▐▌██▒▒▓█  ▄ ░█░ █ ░█ ░██▄▄▄▄██  ░ ▐██▓░
░ ████▓▒░▒██░   ▓██░░▒████▒░░██▒██▓  ▓█   ▓██▒ ░ ██▒▓░
░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▓░▒ ▒   ▒▒   ▓▒█░  ██▒▒▒ 
  ░ ▒ ▒░ ░ ░░   ░ ▒░ ░ ░  ░  ▒ ░ ░    ▒   ▒▒ ░▓██ ░▒░ 
░ ░ ░ ▒     ░   ░ ░    ░     ░   ░    ░   ▒   ▒ ▒ ░░  
    ░ ░           ░    ░  ░    ░          ░  ░░ ░     
                                              ░ ░     
    """ + colorama.Style.RESET_ALL

    print(ascii_art)
    print("1. Gamertag Checker")
    print("2. TempEmail")
    print("3. Configurações")
    print("4. Sair" + colorama.Style.RESET_ALL)

def gamertag_checker2_menu():
    os.system('cls')
    ascii_art = colorama.Fore.MAGENTA + """
 ▒█████   ███▄    █ ▓█████  █     █░ ▄▄▄     ▓██   ██▓
▒██▒  ██▒ ██ ▀█   █ ▓█   ▀ ▓█░ █ ░█░▒████▄    ▒██  ██▒
▒██░  ██▒▓██  ▀█ ██▒▒███   ▒█░ █ ░█ ▒██  ▀█▄   ▒██ ██░
▒██   ██░▓██▒  ▐▌██▒▒▓█  ▄ ░█░ █ ░█ ░██▄▄▄▄██  ░ ▐██▓░
░ ████▓▒░▒██░   ▓██░░▒████▒░░██▒██▓  ▓█   ▓██▒ ░ ██▒▓░
░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▓░▒ ▒   ▒▒   ▓▒█░  ██▒▒▒ 
  ░ ▒ ▒░ ░ ░░   ░ ▒░ ░ ░  ░  ▒ ░ ░    ▒   ▒▒ ░▓██ ░▒░ 
░ ░ ░ ▒     ░   ░ ░    ░     ░   ░    ░   ▒   ▒ ▒ ░░  
    ░ ░           ░    ░  ░    ░          ░  ░░ ░     
                                              ░ ░     
    """ + colorama.Style.RESET_ALL

    print(ascii_art)
    print("1. Começar o Checker")
    print("2. Checkar 1 Gamertag")
    print(colorama.Style.RESET_ALL)
    choice = input("Escolha a opção do submenu: ")

    if choice == "1":
        gamertag_checker_menu()
    elif choice == "2":
        checkar_usuario()
    else:
        print("Opção inválida. Tente novamente.")


def gamertag_checker_menu():
    global webhook_url, delay
    os.system('cls')
    ascii_art = colorama.Fore.MAGENTA + """
 ▒█████   ███▄    █ ▓█████  █     █░ ▄▄▄     ▓██   ██▓
▒██▒  ██▒ ██ ▀█   █ ▓█   ▀ ▓█░ █ ░█░▒████▄    ▒██  ██▒
▒██░  ██▒▓██  ▀█ ██▒▒███   ▒█░ █ ░█ ▒██  ▀█▄   ▒██ ██░
▒██   ██░▓██▒  ▐▌██▒▒▓█  ▄ ░█░ █ ░█ ░██▄▄▄▄██  ░ ▐██▓░
░ ████▓▒░▒██░   ▓██░░▒████▒░░██▒██▓  ▓█   ▓██▒ ░ ██▒▓░
░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▓░▒ ▒   ▒▒   ▓▒█░  ██▒▒▒ 
  ░ ▒ ▒░ ░ ░░   ░ ▒░ ░ ░  ░  ▒ ░ ░    ▒   ▒▒ ░▓██ ░▒░ 
░ ░ ░ ▒     ░   ░ ░    ░     ░   ░    ░   ▒   ▒ ▒ ░░  
    ░ ░           ░    ░  ░    ░          ░  ░░ ░     
                                              ░ ░     
    """ + colorama.Style.RESET_ALL

    print(ascii_art)
    if webhook_url == DEFAULT_WEBHOOK_URL:
        print(colorama.Fore.RED + "ATENÇÃO: A webhook está definida como a padrão. Configure uma webhook válida nas configurações.\n" + colorama.Style.RESET_ALL)
        time.sleep(5)
        configuracoes_menu()
        return

    print("Utilizando a webhook:", webhook_url)
    print("Delay entre as verificações:", delay)   
    print("")   
    time.sleep(5)
    while True:
        random_username = generate_random_username()
        print("Checking username:", random_username)
        hit = check(random_username)
        if hit == random_username:
            print("Valid username found:", random_username)
            send_discord_webhook(random_username, webhook_url)

        time.sleep(delay)

def checkar_usuario():
    os.system('cls')
    ascii_art = colorama.Fore.MAGENTA + """
 ▒█████   ███▄    █ ▓█████  █     █░ ▄▄▄     ▓██   ██▓
▒██▒  ██▒ ██ ▀█   █ ▓█   ▀ ▓█░ █ ░█░▒████▄    ▒██  ██▒
▒██░  ██▒▓██  ▀█ ██▒▒███   ▒█░ █ ░█ ▒██  ▀█▄   ▒██ ██░
▒██   ██░▓██▒  ▐▌██▒▒▓█  ▄ ░█░ █ ░█ ░██▄▄▄▄██  ░ ▐██▓░
░ ████▓▒░▒██░   ▓██░░▒████▒░░██▒██▓  ▓█   ▓██▒ ░ ██▒▓░
░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▓░▒ ▒   ▒▒   ▓▒█░  ██▒▒▒ 
  ░ ▒ ▒░ ░ ░░   ░ ▒░ ░ ░  ░  ▒ ░ ░    ▒   ▒▒ ░▓██ ░▒░ 
░ ░ ░ ▒     ░   ░ ░    ░     ░   ░    ░   ▒   ▒ ▒ ░░  
    ░ ░           ░    ░  ░    ░          ░  ░░ ░     
                                              ░ ░     
    """ + colorama.Style.RESET_ALL

    print(ascii_art)
    username = input("Digite o nome de usuário que deseja verificar: ")
    hit = check(username)
    if hit == username:
        print(colorama.Fore.GREEN + f"Nick Verificado está liberado! - {username}" + colorama.Style.RESET_ALL)
        resposta = input("Clique em 'sim' para prosseguir para o link de trocar gamertag da Xbox (sim/não): ").lower()
        if resposta == "sim":
            webbrowser.open("https://social.xbox.com/changegamertag")
    else:
        print(colorama.Fore.RED + f"Nome de usuário inválido: {username}" + colorama.Style.RESET_ALL)
        time.sleep(5)
        checkar_usuario()


def tempemail_menu():
    num_emails = int(input("Digite o número de endereços de e-mail a serem gerados: "))
    email_manager = TempMailGenerator()
    asyncio.run(email_manager.run(num_emails))


def configuracoes_menu():
    global avatar_url, webhook_name, delay, webhook_url, username_length  
    os.system('cls')
    ascii_art = colorama.Fore.MAGENTA + """
 ▒█████   ███▄    █ ▓█████  █     █░ ▄▄▄     ▓██   ██▓
▒██▒  ██▒ ██ ▀█   █ ▓█   ▀ ▓█░ █ ░█░▒████▄    ▒██  ██▒
▒██░  ██▒▓██  ▀█ ██▒▒███   ▒█░ █ ░█ ▒██  ▀█▄   ▒██ ██░
▒██   ██░▓██▒  ▐▌██▒▒▓█  ▄ ░█░ █ ░█ ░██▄▄▄▄██  ░ ▐██▓░
░ ████▓▒░▒██░   ▓██░░▒████▒░░██▒██▓  ▓█   ▓██▒ ░ ██▒▓░
░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▓░▒ ▒   ▒▒   ▓▒█░  ██▒▒▒ 
  ░ ▒ ▒░ ░ ░░   ░ ▒░ ░ ░  ░  ▒ ░ ░    ▒   ▒▒ ░▓██ ░▒░ 
░ ░ ░ ▒     ░   ░ ░    ░     ░   ░    ░   ▒   ▒ ▒ ░░  
    ░ ░           ░    ░  ░    ░          ░  ░░ ░     
                                              ░ ░     
    """ + colorama.Style.RESET_ALL

    print(ascii_art)

    print("[1] Webhook (Webhook atual: {})".format(webhook_url))
    print("[2] Avatar URL (Avatar URL atual: {})".format(avatar_url))
    print("[3] Nome da Webhook (Nome da Webhook atual: {})".format(webhook_name))
    print("[4] Delay (Delay atual: {})".format(delay))
    print("[5] Número de caracteres (Número atual: {})".format(username_length))

    choice = input("Escolha a opção que deseja alterar (ou pressione Enter para sair): ")

    if choice == "1":
        new_webhook_url = input("Informe o novo nome da webhook (ou pressione Enter para manter o atual): ")
        webhook_url = new_webhook_url if new_webhook_url else webhook_url
    elif choice == "2":
        new_avatar_url = input("Informe a nova URL do avatar (ou pressione Enter para manter a atual): ")
        avatar_url = new_avatar_url if new_avatar_url else avatar_url
    elif choice == "3":
        new_webhook_name = input("Informe o novo nome da webhook (ou pressione Enter para manter o atual): ")
        webhook_name = new_webhook_name if new_webhook_name else webhook_name
    elif choice == "4":
        new_delay = input("Informe o novo delay em segundos (ou pressione Enter para manter o atual): ")
        new_delay = int(new_delay) if new_delay and new_delay.isdigit() else None
        delay = new_delay if new_delay is not None else delay
    elif choice == "5":
        new_username_length = input("Informe o novo comprimento da gamertag (ou pressione Enter para manter o atual): ")
        new_username_length = int(new_username_length) if new_username_length and new_username_length.isdigit() else None
        username_length = new_username_length if new_username_length is not None else username_length
    else:
        print("Opção inválida ou nenhum valor fornecido. As configurações permanecerão as mesmas.")

    salvar_configuracoes()
    print("Configurações salvas com sucesso!")



def run():
    global is_logged_in 
    while True:
        if is_logged_in:
            show_menu()
            choice = input("Escolha a opção desejada: ")

            if choice == "1":
                gamertag_checker2_menu()
            elif choice == "2":
                tempemail_menu()
            elif choice == "3":
                configuracoes_menu()
            elif choice == "4":
                break
            else:
                print("Opção inválida. Tente novamente.")
        else:
            answer()

if __name__ == "__main__":
    carregar_configuracoes()
    run()
