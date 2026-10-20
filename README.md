# Monitor de Logs de Autenticação com Alerta (Simulador de IDS básico)


## Passo a Passo para Rodar

### 1. Clonar ou Acessar a Pasta do Projeto
```bash
cd /path/project
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


Parar a Aplicação

Para parar e remover o container:
```bash
docker compose down
```