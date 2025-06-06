# api_analytics.py (Guarda este código en un archivo con este nombre)
from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from typing import Optional

# Inicializar la aplicación FastAPI
app = FastAPI(title="API de Resultados Analíticos con Pandas")

# Crear un DataFrame de ejemplo
data = {
    'Producto': ['Producto A', 'Producto B', 'Producto C', 'Producto D'],
    'Categoría': ['Electrónica', 'Ropa', 'Alimentos', 'Electrónica'],
    'Ventas': [100, 150, 200, 80],
    'Precio': [50.0, 30.0, 20.0, 100.0]
}
df = pd.DataFrame(data)
df['Ingresos'] = df['Ventas'] * df['Precio']

# Modelo Pydantic para validar parámetros de entrada (opcional)
class FiltroCategoria(BaseModel):
    categoria: Optional[str] = None

# Endpoint raíz
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de resultados analíticos con Pandas"}

# Endpoint para obtener el DataFrame completo
@app.get("/datos")
def get_datos():
    return df.to_dict(orient="records")

# Endpoint para estadísticas descriptivas
@app.get("/estadisticas")
def get_estadisticas():
    estadisticas = df.describe().to_dict()
    return estadisticas

# Endpoint para filtrar por categoría
@app.post("/filtro")
def filtrar_por_categoria(filtro: FiltroCategoria):
    if filtro.categoria:
        df_filtrado = df[df['Categoría'] == filtro.categoria]
    else:
        df_filtrado = df
    return df_filtrado.to_dict(orient="records")

# Endpoint para obtener ingresos totales por categoría
@app.get("/ingresos_por_categoria")
def get_ingresos_por_categoria():
    ingresos = df.groupby('Categoría')['Ingresos'].sum().to_dict()
    return ingresos