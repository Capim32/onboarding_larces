#!/bin/bash

echo "[*] Iniciando o ambiente de monitoramento de segurança..."

mkdir -p /app/logs

if [ ! -f /app/logs/auth_simulado.log ]; then
    touch /app/logs/auth_simulado.log
fi

# Gerador de logs em background para testes
while true; do
    echo "$(date -Iseconds) auth[124]: Failed password for invalid user admin from 203.0.113.50" >> /app/logs/auth_simulado.log
    sleep 3
done &

echo "[*] Disparando o monitoramento de logs em tempo real..."
exec python3 -c 'from monitor import monitorar_log_tempo_real; monitorar_log_tempo_real("logs/auth_simulado.log")'