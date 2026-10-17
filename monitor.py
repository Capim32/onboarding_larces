from datetime import datetime, time, timedelta 
from collections import defaultdict
import re

tentativas_falhas = defaultdict(int)
MAX_TENTATIVAS = 3

# regex para capturar o endereço IP de tentativas de login falhas
padrao_log = re.compile(
    r"Failed password.*from\s+(\d{1,3}(?:\.\d{1,3}){3})"
)

def monitorar_log(path_log):
    with open (path_log, "r") as file:
        for line in file:
            if match(line):
                break

def monitorar_log_tempo_real(path_log):
    print(f"monitorando {path_log} em tempo real...")
    with open(path_log, "r") as file:
        file.seek(0,2)

        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5)
                continue
            if match(line):
                break


def match(line):
    match = padrao_log.search(line)
    if match:
        ip = match.group(1)
        tentativas_falhas[ip] += 1
        if tentativas_falhas[ip] >= MAX_TENTATIVAS:
            print(
                f"[ALERTA DE SEGURANÇA] Possível ataque de Força Bruta detectado"
                f" do IP: {ip}"
            )
            print(block_ip(ip))
            return True
    return False


def block_ip(ip):
    return f"IP {ip} bloqueado ebaaa"



if __name__ == "__main__":
    monitorar_log("auth_simulado.log")
    # monitorar_log_tempo_real("auth_simulado.log")