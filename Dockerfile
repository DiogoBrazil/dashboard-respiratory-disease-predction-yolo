# Use uma imagem base com Python 3.10
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Atualizar pip antes de instalar as dependências
RUN pip install --upgrade pip

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o conteúdo da pasta atual para o diretório de trabalho no container
COPY . .

# Expor a porta padrão do Streamlit (8501)
EXPOSE 8501

# Comando para rodar a aplicação
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS=false"]
