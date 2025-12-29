# Dockerfile para FastAPI + Uvicorn + requirements.txt
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto de la app
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
