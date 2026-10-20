import time
from datetime import datetime, timedelta 
from collections import defaultdict
import re
import subprocess

TENTATIVAS_FALHAS = defaultdict(list)
TIME_WINDOW = timedelta(minutes=5)
MAX_TENTATIVAS = 5

# regex para capturar o endereço IP de tentativas de login falhas
padrao_log = re.compile(
    r"Failed password.*from\s+(\d{1,3}(?:\.\d{1,3}){3})"
)

def monitorar_log(path_log):
    try:
        with open (path_log, "r") as file:
            for line in file:
                match(line)
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
                match(line)  
    except FileNotFoundError:
        print(f"[Erro] O arquivo {path_log} não foi encontrado.", flush=True)
        exit(1)

def match(line):
    match = padrao_log.search(line)
    if match:
        ip = match.group(1)
        now = datetime.now()

        TENTATIVAS_FALHAS[ip].append(now)

        TENTATIVAS_FALHAS[ip] = [
            time for  time in TENTATIVAS_FALHAS[ip] 
            if now - time <= TIME_WINDOW
        ]

        tentativas = len(TENTATIVAS_FALHAS[ip])
        if tentativas >= MAX_TENTATIVAS:
            print(
                f"\n[ALERTA DE SEGURANÇA] Possível ataque de Força Bruta detectado!"
                f"\nIP: {ip} realizou {tentativas} ou mais tentativas em menos de {TIME_WINDOW.seconds // 60} minutos.",
                flush=True
            )
            print(block_ip(ip), flush=True)
            TENTATIVAS_FALHAS[ip].clear()


def block_ip(ip):
    try:
        # add o IP a lista de bloqueio (drop source)
        drop = ["firewall-cmd", "--permanent", f"--add-source={ip}", "--set-context=drop"]
        
        subprocess.run(drop, check=True)
        subprocess.run(["firewall-cmd", "--reload"], check=True)

        return f"[SUCESSO] IP {ip} bloqueado via firewalld no Fedora."
    except Exception as e:
        return f"[ERRO] falha ao bloquear o IP {ip}: {e}"

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

    path_log = "logs/auth_simulado.log"
    monitorar_log_tempo_real(path_log)