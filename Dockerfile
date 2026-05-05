FROM python:3.11-slim

WORKDIR /app

# Copiar arquivos
COPY requirements.txt .
COPY main.py .
COPY app.py .
COPY cartoes_golfville.csv .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor porta
EXPOSE 7860

# Variáveis de ambiente
ENV FLET_SERVER_PORT=7860
ENV FLET_FORCE_WEB_VIEW=true

# Comando para rodar
CMD ["python", "app.py"]