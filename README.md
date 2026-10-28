# Python Security Monitor (IDS/IPS)

Um sistema leve e containerizado de Detecção e Prevenção de Intrusão (IDS/IPS) desenvolvido em `Python`, projetado para rodar em ambientes `Linux`, monitorar arquivos de log de autenticação em tempo real e aplicar contramedidas ativas de bloqueio de rede via `iptables`.

---

## Arquitetura e Funcionamento do Projeto

O projeto foi construído seguindo uma arquitetura modular e orientada à segurança, dividida em quatro componentes principais:

1. **Monitoramento em Tempo Real (`monitor.py`):**
   * Lê arquivos de log linha por linha de forma contínua.
   * Utiliza Regular Expression em Python para analisar eventos de falha de autenticação (`Failed password`) associados a endereços IP.
   * Implementa uma janela temporal: se um mesmo IP acumular 5 ou mais falhas dentro dessa janela, o sistema classifica o comportamento como um **ataque de força bruta**.

2. **Blindagem e Whitelist (`WHITELIST_IPS`):**
   * Antes de qualquer tomada de ação drástica, o sistema verifica se o IP consta um dicionário de endereços confiáveis (`127.0.0.1`, `::1`, IPs locais). Caso o IP pertença à lista, o bloqueio é abortado.

3. **Mecanismo de Prevenção Ativa - IPS (`block_ip`):**
   * Caso o IP seja malicioso e passe pela whitelist, a função dispara comandos de sistema utilizando a biblioteca `subprocess` para interagir diretamente com o **`iptables`** do kernel Linux.
   * Aplica a regra de negação de tráfego (`iptables -A INPUT -s <IP> -j DROP`), silenciando o host na camada de rede.

4. **Isolamento e Orquestração (`Docker & SELinux`):**
   * Executa dentro de um container Docker (`python:3.10-slim`).
   * Utiliza a capacidade `NET_ADMIN` para manipular regras de rede e a flag de volume `:Z` para garantir compatibilidade com as políticas estritas de segurança do **SELinux** no Fedora.


## Passo a Passo para Rodar

### 1. Clonar ou Acessar a Pasta do Projeto
```bash
cd /path/onboarding_larces
```

### 2. Subir o Container
Execute o comando abaixo para construir e iniciar o container em segundo plano:
```bash
docker compose up --build -d
```

### 3. Acompanhar os Alertas em Tempo Real
Para visualizar a saída e os alertas do IDS, abra o acompanhamento dos logs:
```bash
docker compose logs -f
```

### 4. Parar a Aplicação
Para parar e remover o container:
```bash
docker compose down
```