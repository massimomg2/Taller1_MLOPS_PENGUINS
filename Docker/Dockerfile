# Imagen base Python
FROM python:3.11-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install -r requirements.txt

# Copiar API y modelos (contexto de build = raíz del proyecto)
COPY FastAPI/ ./FastAPI/
COPY Modelos/penguin_decision_tree.pkl Modelos/penguin_random_forest.pkl ./Modelos/

# Puerto donde se expone la API
EXPOSE 8989

# Arrancar la API con uvicorn en 0.0.0.0 para aceptar conexiones externas
CMD ["uvicorn", "FastAPI.main:app", "--host", "0.0.0.0", "--port", "8989"]
