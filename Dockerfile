FROM python:3.10-slim

WORKDIR /app
COPY . /app
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]