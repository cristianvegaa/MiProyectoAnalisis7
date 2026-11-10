# MiProyectoAnalisis — Análisis predictivo de ventas en Alkomprar

**Asignatura:** Herramientas de Inteligencia Artificial y Ciencia de Datos  
**Estudiante:** Cristian Julian Vega Florez  
**Programa:** Tecnología en Análisis y Gestión de Datos  
**Institución:** Universidad Tecnológica de Santander (UTS)

## Presentación

Este repositorio organiza el ejercicio desarrollado en el notebook de análisis de Alkomprar. El experimento utiliza un conjunto de datos simulado de 150 productos y un modelo de aprendizaje supervisado de **regresión lineal** para estimar `Unidades_Vendidas` a partir de características de producto, precio, inventario, devoluciones, logística y variables comerciales.

> **Aclaración del objetivo:** aunque el título original del notebook menciona la rotación del inventario, el código define `y = df['Unidades_Vendidas']`. Por tanto, el objetivo que realmente se entrenó y evaluó fue la predicción de unidades vendidas. La bitácora conserva esta diferencia para no atribuir al experimento un resultado distinto.

## Estructura del proyecto

```text
MiProyectoAnalisis/
├── .gitignore
├── README.md
├── bitacora.md
├── data/
│   ├── raw/
│   │   ├── README.md
│   │   └── .gitkeep
│   └── processed/
│       ├── README.md
│       └── .gitkeep
├── notebooks/
│   └── analisis_alkomprar.ipynb
├── src/
│   └── entrenar_modelo.py
└── docs/
    └── evidence/
        └── README.md
```

## Datos necesarios

El notebook original carga `alkomprar_datos_inventados.csv`. Ese CSV no venía adjunto junto con el notebook, por eso no se ha creado ni reemplazado con datos inventados. Coloca el archivo original en `data/raw/alkomprar_datos_inventados.csv`. La carpeta `data/raw` está excluida de Git por configuración; si los datos son sintéticos y el equipo decide publicarlos, se puede modificar `.gitignore` conscientemente.

## Cómo ejecutar

1. Instala Python 3.10 o superior.
2. Instala las dependencias: `pip install pandas numpy scikit-learn matplotlib jupyter`.
3. Guarda el CSV original en `data/raw/alkomprar_datos_inventados.csv`.
4. Ejecuta `python src/entrenar_modelo.py` desde la raíz del proyecto.
5. También puedes abrir `notebooks/analisis_alkomprar.ipynb` en Jupyter o subirlo a Google Colab.

El script genera `metricas_modelo.csv` y `predicciones_modelo.csv` dentro de `data/processed/`.

## Resultados registrados en el notebook

| Métrica | Resultado |
|---|---:|
| MAE | 36.2058 |
| MSE | 2967.7389 |
| RMSE | 54.4770 |
| R² | -0.8375 |

El R² negativo indica que, en el conjunto de prueba utilizado, el modelo rindió peor que una predicción de referencia basada en la media de la variable objetivo.

## Consideraciones

- Los 150 registros se describen en el trabajo como datos inventados/simulados; no representan necesariamente las operaciones reales de Alkomprar.
- El notebook reporta cero valores nulos y cero registros duplicados.
- El preprocesamiento convierte variables categóricas mediante `OneHotEncoder(handle_unknown='ignore')` y deja las numéricas sin transformar (`remainder='passthrough'`).
- Antes de interpretar el modelo como herramienta de decisión, se debe revisar la posible fuga de información en variables derivadas de ventas o registradas después de la venta, como `Rotacion_Inventario`, `Dias_Inventario`, `Unidades_Devueltas`, `Devolucion` y `Motivo_Devolucion`.
- Los archivos originales y las evidencias deben agregarse en las carpetas correspondientes.
