"""Reproduce el experimento de regresión lineal del notebook de Alkomprar.

Ejecutar desde la raíz: python src/entrenar_modelo.py
Requiere data/raw/alkomprar_datos_inventados.csv.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "alkomprar_datos_inventados.csv"
OUT = ROOT / "data" / "processed"

def main():
    if not DATA.exists():
        sys.exit(f"No se encontró el archivo de datos: {DATA}\nGuarda allí el CSV original utilizado en el notebook.")

    df = pd.read_csv(DATA)
    objetivo = "Unidades_Vendidas"
    if objetivo not in df.columns:
        sys.exit(f"El CSV no contiene la variable objetivo requerida: {objetivo}")

    y = df[objetivo]
    
    # Eliminamos ID y variables con excesiva cardinalidad si existieran (ej. fechas directas o nombres únicos)
    X = df.drop(columns=[objetivo, "ID_Producto"], errors="ignore")
    
    numericas = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categoricas = X.select_dtypes(include=["object"]).columns.tolist()

    # PIPELINE DE PREPROCESAMIENTO EXPLÍCITO
    # Agregamos StandardScaler para mejorar la convergencia y análisis de coeficientes de la Regresión Lineal
    preprocesamiento = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categoricas),
            ("num", StandardScaler(), numericas)
        ]
    )
    
    modelo = Pipeline(steps=[
        ("preprocesamiento", preprocesamiento),
        ("regresion", LinearRegression())
    ])
    
    # Partición de datos garantizando reproducibilidad (random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    
    # Entrenamiento
    modelo.fit(X_train, y_train)
    
    # Predicción
    y_pred = modelo.predict(X_test)

    # Evaluación de métricas
    mse = mean_squared_error(y_test, y_pred)
    metricas = pd.DataFrame({
        "Metrica": ["MAE", "MSE", "RMSE", "R2"],
        "Resultado": [
            mean_absolute_error(y_test, y_pred), 
            mse, 
            np.sqrt(mse), 
            r2_score(y_test, y_pred)
        ]
    })
    
    # Construcción segura del dataframe de salida
    predicciones = pd.DataFrame({"Real": y_test.to_numpy(), "Prediccion": y_pred})
    
    # Escritura de resultados
    OUT.mkdir(parents=True, exist_ok=True)
    metricas.to_csv(OUT / "metricas_modelo.csv", index=False)
    predicciones.to_csv(OUT / "predicciones_modelo.csv", index=False)
    
    # Logs por consola
    print("=== Reporte de Ejecución ===")
    print("Registros totales:", len(df))
    print("Entrenamiento:", len(X_train), "| Prueba:", len(X_test))
    print("\n--- Métricas del Modelo ---")
    print(metricas.to_string(index=False))
    print("\nResultados guardados exitosamente en:", OUT)

if __name__ == "__main__":
    main()
