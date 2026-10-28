import time
from datetime import datetime, timedelta 
from collections import defaultdict
import re
import subprocess

TENTATIVAS_FALHAS = defaultdict(list)
TIME_WINDOW = timedelta(minutes=5)
MAX_TENTATIVAS = 5
WHITELIST_IPS = {"127.0.0.1", "::1", "192.168.1.1"}

# regex para capturar o endereço IP de tentativas de login falhas
padrao_log = re.compile(
    r"Failed password.*from\s+(\d{1,3}(?:\.\d{1,3}){3})"
)

    
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


# o IP continua aparecendo depos de bloqueado por causa do script, em uma situação real, o IP seria bloqueado e não apareceria mais no log
def block_ip(ip):
    if ip in WHITELIST_IPS:
        print(f"[AVISO DE SEGURANÇA] O IP {ip} pertence à Whitelist e não será bloqueado.", flush=True)
        return 
        
    try:
        comando = ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
        result = subprocess.run(comando, capture_output=True, text=True, check=True)

        return f"[SUCESSO] IP {ip} bloqueado pelo iptables."
    except subprocess.CalledProcessError as e:
            return f"[ERRO] Falha ao bloquear o IP {ip}. Detalhes: {e.stderr.strip()}"
    except FileNotFoundError:
        return f"[ERRO] O comando iptables não foi encontrado."

if __name__ == "__main__":  

    path_log = "logs/auth_simulado.log"
    monitorar_log_tempo_real(path_log)