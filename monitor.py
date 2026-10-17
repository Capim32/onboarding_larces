import time
from datetime import datetime, timedelta 
from collections import defaultdict
import re

TENTATIVAS_FALHAS = defaultdict(int)
MAX_TENTATIVAS = 3

# regex para capturar o endereço IP de tentativas de login falhas
padrao_log = re.compile(
    r"Failed password.*from\s+(\d{1,3}(?:\.\d{1,3}){3})"
)

def monitorar_log(path_log):
    try:
        with open (path_log, "r") as file:
            for line in file:
                if match(line):
                    break
    except FileNotFoundError:
        print(f"[Erro] O arquivo {path_log} não foi encontrado.")
        exit(1)
    
def monitorar_log_tempo_real(path_log):
    print(f"monitorando {path_log} em tempo real...")
    try:
        with open(path_log, "r") as file:
            file.seek(0,2)

            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                if match(line):
                    break
    except FileNotFoundError:
        print(f"[Erro] O arquivo {path_log} não foi encontrado.")
        exit(1)

def match(line):
    match = padrao_log.search(line)
    if match:
        ip = match.group(1)
        TENTATIVAS_FALHAS[ip] += 1
        if TENTATIVAS_FALHAS[ip] >= MAX_TENTATIVAS:
            print(
                f"[ALERTA DE SEGURANÇA] Possível ataque de Força Bruta detectado"
                f" do IP: {ip}"
            )
            print(block_ip(ip))
            TENTATIVAS_FALHAS[ip] = 0


def block_ip(ip):
    return f"IP {ip} bloqueado ebaaa"


def menu(path_log):
    opcoes_validas = {"1", "2", "3"}
    while True:
        print("\n=== MENU DE MONITORAMENTO ===")
        print("1. Monitorar log de autenticação")
        print("2. Monitorar log de autenticação em tempo real")
        print("3. Sair")
        opcao = input("Opção: ").strip()

        if opcao not in opcoes_validas:
            print("\n[Erro] Opção inválida. Tente novamente.")
            continue

        if opcao == "1":
            monitorar_log(path_log)

        elif opcao == "2":
            monitorar_log_tempo_real(path_log)
        elif opcao == "3":
            print("Saindo do programa...")
            break

if __name__ == "__main__":  

    path_log = "auth_simulado.log"
    menu(path_log)