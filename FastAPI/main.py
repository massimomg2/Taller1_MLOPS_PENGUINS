"""
API FastAPI para predicción de especies de pingüinos.
Endpoints POST: sólamente /pred. Se pasa un argumento adicional para usar un modelo DT o RF, con las letras respectivamente
"""

import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

# Declaración de variables y rutas
API_DIR = os.path.dirname(os.path.abspath(__file__)) # __file__ es una variable de python que contiene la ruta del archivo siendo ejecutado
PROJECT_ROOT = os.path.dirname(API_DIR)
MODEL_DIR = os.path.join(PROJECT_ROOT, "Modelos")
DT_PATH = os.path.join(MODEL_DIR, "penguin_decision_tree.pkl")
RF_PATH = os.path.join(MODEL_DIR, "penguin_random_forest.pkl")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("iniciando aplicación")
    
    try:
        app.state.model_dt = joblib.load(DT_PATH)
        app.state.model_rf = joblib.load(RF_PATH)
        print(f"Aplicación iniciada con éxito, modelos cargados desde {DT_PATH}")
        yield
    except Exception as e:
        print("Error iniciando aplicación")
        print(str(e))
        return

app = FastAPI(
    title="Penguins Species API",
    description="Predicción de especie de pingüino con modelos DT y RF.",
    version="3.0.0",
    lifespan = lifespan
)

model_dt = None
model_rf = None

# Utilizamos BaseModel / Fetaure de pydantic, una librería que nos permite definir clases con los objetos que deseamos mandar que garantizan su fácil manejo

class PenguinFeatures(BaseModel):
    """Features requeridas para predecir species (mismo orden que en entrenamiento)."""

    island: str = Field(..., description="Isla: Torgersen, Biscoe o Dream")
    bill_length_mm: float = Field(..., description="Longitud del pico en mm")
    bill_depth_mm: float = Field(..., description="Profundidad del pico en mm")
    flipper_length_mm: float = Field(..., description="Longitud de aleta en mm")
    body_mass_g: float = Field(..., description="Masa corporal en gramos")
    sex: str = Field(..., description="Sexo: male o female")
    year: int = Field(..., description="Año (ej: 2007)")
    model: str = Field(..., description="Modelo que se desea usar para la predicción (DT, RF)")

def predict_penguin_species(features: PenguinFeatures) -> str:
    """Convierte las features a DataFrame y devuelve la especie predicha."""
    row = pd.DataFrame([{
        "island": features.island,
        "bill_length_mm": features.bill_length_mm,
        "bill_depth_mm": features.bill_depth_mm,
        "flipper_length_mm": features.flipper_length_mm,
        "body_mass_g": features.body_mass_g,
        "sex": features.sex,
        "year": features.year,
    }])
    if features.model == 'DT':
      pred = app.state.model_dt.predict(row)
    elif features.model == 'RF':
      pred = app.state.model_rf.predict(row)
    else:
      raise ValueError("Modelo inválido. Use 'DT' o 'RF'")
    return str(pred[0])

@app.post("/pred")
def predict(features: PenguinFeatures):
    """Predicción de especie usando el modelo especificado"""
    if app.state.model_rf is None or app.state.model_dt is None:
        raise HTTPException(status_code=503, detail="Modelos no cargados con éxito")
    try:
        species = predict_penguin_species(features)
        return {"model": features.model, "species": species}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/")
def root():
    """Información de la API."""
    return {
        "message": "Penguins Species API",
        "docs": "/docs",
        "endpoints": {"POST /pred": "predecir pinguino"},
    }
