# BITÁCORA DIGITAL DE EXPERIMENTACIÓN Y DECISIONES ANALÍTICAS
## Caso de estudio académico: Alkomprar – datos simulados

**Asignatura:** Herramientas de Inteligencia Artificial y Ciencia de Datos  
**Programa:** Tecnología en Análisis y Gestión de Datos  
**Institución:** Universidad Tecnológica de Santander (UTS)  
**Integrantes:** Cristian Julian Vega Florez, Sergio Andres Valenzuela Guerrero
**Proyecto:** MiProyectoAnalisis7  
**Archivo de datos:** [`alkomprar_datos_inventados.csv`](DATA/RAW/alkomprar_datos_inventados.csv)  
**Notebook:** [`analisis_alkomprar.ipynb`](NOTEBOOKS/analisis_alkomprar.ipynb)  

---

## 1. Descripción del caso y objetivo analítico

En este proyecto trabajamos como equipo consultor analítico sobre un conjunto de datos simulado que representa el catálogo y movimiento comercial de productos, tomando a **Alkomprar** como contexto empresarial. Las variables disponibles abarcan precios de venta y de competencia, unidades vendidas, existencias, devoluciones, costos operativos, tiempos de entrega, promociones, satisfacción del cliente, temporada, canal de venta y proveedor.

Nuestro objetivo técnico fue construir y evaluar un modelo de aprendizaje supervisado capaz de predecir la cantidad de `Unidades_Vendidas` a partir de las características comerciales y logísticas de cada producto, excluyendo el identificador `ID_Producto`.

**Nota metodológica sobre el alcance:** Aunque el título inicial del cuaderno de trabajo hacía referencia a la rotación de inventario, como equipo definimos explícitamente `y = df['Unidades_Vendidas']` como nuestra variable objetivo. Si bien el dataset contiene la columna `Rotacion_Inventario`, decidimos orientar esta primera iteración a estimar directamente el volumen de ventas por unidad.

---

## 2. Organización y trazabilidad del proyecto

Para garantizar la reproducibilidad y el control de versiones, estructuramos el repositorio digital separando los datos crudos, los resultados procesados, el código fuente y las evidencias visuales:

```text
MiProyectoAnalisis7/
├── DATA/
│   ├── RAW/                 # Dataset original simulado
│   └── PROCESSED/           # Métricas y predicciones exportadas
├── NOTEBOOKS/               # Desarrollo exploratorio y modelado
├── SRC/                     # Scripts en Python
├── DOCS/
│   └── EVIDENCIAS/          # Capturas de pantalla y gráficos
│  
├── README.md                # Bitácora principal del proyecto
└── .gitignore
```

Gestionamos el historial de cambios mediante *commits* descriptivos en GitHub (por ejemplo: *"Agrega revisión de calidad de datos"* y *"Documenta métricas del modelo"*), permitiendo rastrear cada ajuste técnico realizado por el equipo.

---

## 3. Registro de experimentación y decisiones

### Registro 1. Carga y exploración inicial

- **Fecha:** 07 de Noviembre 2026
- **Actividad realizada:** Importamos el archivo `alkomprar_datos_inventados.csv` utilizando la librería Pandas e inspeccionamos los primeros registros, las estadísticas descriptivas y la estructura general de columnas.
- **Decisión tomada:** Emplear Pandas para la carga y perfilamiento inicial del dataset antes de plantear cualquier transformación.
- **Justificación:** Comprender la dimensionalidad del conjunto de datos, la naturaleza de cada variable y sus rangos numéricos es indispensable para detectar inconsistencias tempranas y diseñar el flujo de preprocesamiento.
- **Evidencia:** Captura de `df.head()`, `df.describe()` y listado de columnas. *(Adjuntar en `DOCS/EVIDENCIAS/01_carga_datos.png`)*
- **Resultado:** Confirmamos un volumen de 150 observaciones y 21 columnas.
- **Reflexión:** La exploración inicial nos permitió diferenciar claramente las variables numéricas de las categóricas. Al trabajar con un entorno simulado, asumimos este ejercicio como una prueba de concepto metodológica cuyos patrones no representan necesariamente la operación real de Alkomprar.

### Registro 2. Revisión de calidad de los datos

- **Fecha:** 08 de Noviembre 2026
- **Actividad realizada:** Ejecutamos auditorías de integridad mediante `isnull().sum()`, `duplicated().sum()` y verificación de tipos de datos (`dtypes`).
- **Decisión tomada:** Conservar la totalidad de los registros sin aplicar técnicas de eliminación de filas ni imputación de valores.
- **Justificación:** Las pruebas diagnósticas confirmaron ausencia total de valores faltantes y registros duplicados, por lo que intervenir los datos habría sido innecesario.
- **Evidencia:** Captura de los resultados de nulos, duplicados y tipos de datos. *(Adjuntar en `DOCS/EVIDENCIAS/03_calidad_datos.png`)*
- **Resultado:** 0 valores nulos y 0 filas duplicadas sobre las 150 observaciones.
- **Reflexión:** Aunque la limpieza estructural del archivo fue óptima, reconocemos como equipo que la ausencia de nulos no garantiza consistencia de negocio; en futuras iteraciones incluiremos validaciones de rangos lógicos y detección de valores atípicos (*outliers*).

### Registro 3. Selección de variables

- **Fecha:** 08 de Noviembre 2026
- **Actividad realizada:** Establecimos `Unidades_Vendidas` como variable dependiente (`y`) y conformamos la matriz de características (`X`) descartando `ID_Producto` y la propia variable objetivo.
- **Decisión tomada:** Excluir `ID_Producto` del entrenamiento y mantener las 19 variables restantes como predictoras.
- **Justificación:** Los códigos identificadores son etiquetas administrativas únicas que no aportan valor explicativo sobre la demanda y pueden inducir memorización artificial en el modelo.
- **Evidencia:** Captura del bloque de código de selección de `X` y `y`, junto con la separación de listas numéricas y categóricas. *(Adjuntar en `DOCS/EVIDENCIAS/04_variables.png`)*
- **Resultado:** Seleccionamos 10 variables predictoras numéricas y 9 categóricas.
- **Reflexión:** Al analizar las variables retenidas, identificamos que columnas como `Rotacion_Inventario` y `Dias_Inventario` suelen calcularse en entornos reales a partir del histórico de ventas. Decidimos mantenerlas en esta primera línea base, pero dejamos documentado que su inclusión representa un riesgo de fuga de información (*data leakage*) que auditaremos antes de llevar el modelo a un entorno productivo.

### Registro 4. División de entrenamiento y prueba

- **Fecha:** 09 de Noviembre 2026
- **Actividad realizada:** Particionamos el conjunto de datos mediante la función `train_test_split` de Scikit-learn.
- **Decisión tomada:** Asignar el 80 % de los registros al conjunto de entrenamiento y reservar el 20 % para prueba, fijando la semilla `random_state=42`.
- **Justificación:** Evaluar el algoritmo sobre datos no vistos durante el ajuste nos permite medir su capacidad real de generalización. Fijar la semilla garantiza que cualquier miembro del equipo obtenga exactamente la misma partición al replicar el código.
- **Evidencia:** Captura de la celda `train_test_split` y verificación de dimensiones (`.shape`). *(Adjuntar en `DOCS/EVIDENCIAS/05_division_datos.png`)*
- **Resultado:** 120 registros destinados a entrenamiento y 30 registros para evaluación.
- **Reflexión:** Dado el tamaño reducido del dataset (150 filas), evaluar sobre 30 observaciones genera alta sensibilidad ante variaciones muestrales. Para estabilizar las métricas en la siguiente fase, implementaremos validación cruzada (*k-fold cross-validation*).

### Registro 5. Preparación de variables categóricas y construcción del modelo

- **Fecha:** 09 de Noviembre 2026
- **Actividad realizada:** Configuramos un `ColumnTransformer` aplicando `OneHotEncoder(handle_unknown='ignore')` a las variables categóricas y `remainder='passthrough'` a las numéricas, integrando todo dentro de un `Pipeline` junto con `LinearRegression`.
- **Decisión tomada:** Transformar las categorías mediante codificación One-Hot y encapsular el preprocesamiento y el estimador en un único flujo (`Pipeline`).
- **Justificación:** Los modelos lineales requieren entradas estrictamente numéricas; One-Hot Encoding evita imponer jerarquías artificiales entre categorías nominales. Por su parte, el `Pipeline` previene errores de procesamiento entre entrenamiento y prueba.
- **Evidencia:** Captura de la definición del `ColumnTransformer`, `OneHotEncoder` y `Pipeline`. *(Adjuntar en `DOCS/EVIDENCIAS/06_preprocesamiento_modelo.png`)*
- **Resultado:** Flujo automatizado de transformación y regresión listo para ejecución.
- **Reflexión:** Aunque importamos la clase `SimpleImputer` durante la preparación del entorno, optamos por no incluirla en el `Pipeline` tras verificar que el dataset no contenía valores nulos.

### Registro 6. Entrenamiento y generación de predicciones

- **Fecha:** 10 de Noviembre 2026
- **Actividad realizada:** Ajustamos el flujo completo sobre los datos de entrenamiento (`modelo.fit(X_train, y_train)`) y calculamos las estimaciones sobre el conjunto reservado (`modelo.predict(X_test)`).
- **Decisión tomada:** Entrenar el estimador exclusivamente con el subconjunto del 80 % y generar predicciones sobre el 20 % restante.
- **Justificación:** Mantener un aislamiento estricto entre ambos conjuntos evita el sesgo de evaluación optimista y refleja cómo respondería el modelo frente a productos nuevos.
- **Evidencia:** Captura de las celdas de ajuste (`fit`) y predicción (`predict`). *(Adjuntar en `DOCS/EVIDENCIAS/07_entrenamiento.png`)*
- **Resultado:** Obtuvimos el vector de 30 predicciones correspondiente al conjunto de prueba.
- **Reflexión:** Las salidas generadas constituyen estimaciones estadísticas preliminares que contrastamos rigurosamente contra los valores reales en la etapa de evaluación.

### Registro 7. Evaluación del modelo

- **Fecha:** 10 de Noviembre 2026
- **Actividad realizada:** Calculamos las métricas de error MAE, MSE, RMSE y el coeficiente de determinación R² utilizando `sklearn.metrics`.
- **Decisión tomada:** Evaluar el rendimiento mediante cuatro métricas complementarias en lugar de depender de un único indicador.
- **Justificación:** El MAE nos muestra la desviación promedio en unidades reales; el MSE y el RMSE penalizan con mayor severidad los errores atípicos; y el R² mide qué proporción de la varianza logra explicar nuestro modelo frente a una predicción basada simplemente en el promedio.
- **Evidencia:** Captura de los resultados en consola y exportación en [`DATA/PROCESSED/metricas_modelo.csv`](DATA/PROCESSED/metricas_modelo.csv). *(Adjuntar en `DOCS/EVIDENCIAS/08_metricas.png`)*
- **Resultado obtenido:**

| Métrica | Valor |
|---|---:|
| MAE | 36.2058 |
| MSE | 2967.7389 |
| RMSE | 54.4770 |
| R² | -0.8375 |

- **Interpretación:** El modelo presenta un error absoluto medio de 36.21 unidades y un RMSE de 54.48 unidades. El coeficiente R² negativo (-0.8375) demuestra que, en esta partición de prueba, la regresión lineal tiene un desempeño inferior al de un modelo base que predijera constantemente la media de ventas. Concluimos que el modelo actual no es apto para respaldar decisiones de compra o inventario.
- **Reflexión:** Documentar este resultado negativo con transparencia es clave en nuestro proceso consultivo. Este comportamiento evidencia que la relación entre las variables comerciales no es estrictamente lineal y que el alto número de columnas generadas por el One-Hot Encoding frente a solo 120 filas de entrenamiento provocó sobreajuste (*overfitting*).

### Registro 8. Visualización de resultados

- **Fecha:** 10 de Noviembre 2026
- **Actividad realizada:** Construimos un gráfico de dispersión comparando unidades reales frente a predichas y un gráfico comparativo para las primeras 15 observaciones del conjunto de prueba.
- **Decisión tomada:** Incorporar análisis visual para diagnosticar la distribución de los errores residuales.
- **Justificación:** Las representaciones gráficas permiten detectar rápidamente desviaciones sistemáticas, subestimaciones o valores extremos que las métricas globales promedian.
- **Evidencia:** Gráficos exportados desde el notebook. *(Adjuntar en `DOCS/EVIDENCIAS/09_graficos.png`)*
- **Resultado:** Visualizamos una alta dispersión entre los valores reales y las estimaciones del modelo lineal.
- **Reflexión:** Las gráficas confirman visualmente lo advertido por el R² negativo: el modelo no logra capturar la tendencia de los datos con el volumen de muestra y la arquitectura actual.

---

## 4. Variables utilizadas

### Variable objetivo
- `Unidades_Vendidas`: Cantidad total de unidades comercializadas por registro.

### Variables predictoras
Excluimos `ID_Producto` (identificador) y utilizamos las 19 características restantes:

- **Variables numéricas (10):** `Precio_Venta`, `Precio_Competencia`, `Stock_Disponible`, `Unidades_Devueltas`, `Costo_Operativo`, `Tiempo_Entrega`, `Diferencia_Precio`, `Tasa_Devolucion`, `Rotacion_Inventario` y `Dias_Inventario`.
- **Variables categóricas (9):** `Categoria`, `Marca`, `Promocion`, `Devolucion`, `Nivel_Satisfaccion`, `Motivo_Devolucion`, `Temporada`, `Canal_Venta` y `Proveedor`.

**Observación técnica sobre variables derivadas:** Al auditar el diccionario de datos, identificamos cuatro métricas calculadas: `Diferencia_Precio`, `Tasa_Devolucion`, `Rotacion_Inventario` y `Dias_Inventario`. Mientras que `Diferencia_Precio` es una variable válida previa a la venta, los indicadores de rotación y días de inventario suelen depender del flujo histórico de salidas. En nuestra próxima iteración aislaremos estas columnas para comprobar si introducen fuga de información (*data leakage*) y medir su impacto real en el entrenamiento.

---

## 5. Transformaciones, algoritmo y parámetros

### Transformaciones aplicadas
1. Separación programática de variables según su tipo de dato (`int64`/`float64` frente a `object`).
2. Codificación binaria de categorías mediante `OneHotEncoder(handle_unknown='ignore')`.
3. Transferencia directa de variables numéricas mediante `remainder='passthrough'`.
4. Encapsulamiento del preprocesamiento y del estimador en un `Pipeline` secuencial.

*Nota:* En esta línea base no aplicamos escalamiento estándar (`StandardScaler`), imputación ni selección automática de características.

### Algoritmo seleccionado
Implementamos `LinearRegression` (Mínimos Cuadrados Ordinarios) de Scikit-learn. Como equipo elegimos este algoritmo como modelo base (*baseline*) por su rapidez computacional, facilidad de interpretación y capacidad para establecer un punto de referencia inicial antes de probar ensambles o modelos no lineales más complejos.

### Parámetros configurados

| Componente / Parámetro | Configuración aplicada |
|---|---|
| Algoritmo base | `LinearRegression()` |
| Proporción de prueba | `test_size=0.20` (30 registros) |
| Proporción de entrenamiento | `0.80` (120 registros) |
| Semilla aleatoria | `random_state=42` |
| Codificador categórico | `OneHotEncoder(handle_unknown='ignore')` |
| Manejo de numéricas | `remainder='passthrough'` |

---

## 6. Dificultades, limitaciones e inconsistencias identificadas

1. **Limitación por datos simulados:** El archivo consta de 150 registros sintéticos; por ende, los hallazgos tienen alcance estrictamente académico y no son extrapolables a la operación real de Alkomprar.
2. **Dimensionalidad frente al tamaño de muestra:** Al aplicar `OneHotEncoder` sobre 9 variables categóricas con solo 120 filas de entrenamiento, aumentó considerablemente la dimensionalidad del espacio de características, degradando la capacidad de generalización de la regresión lineal (R² = -0.8375).
3. **Tamaño reducido de evaluación:** Contar con apenas 30 registros en el conjunto de prueba hace que las métricas sean sensibles a casos puntuales.
4. **Riesgo de fuga de datos (*data leakage*):** La presencia de variables derivadas de inventario (`Rotacion_Inventario`, `Dias_Inventario`) y devoluciones (`Unidades_Devueltas`, `Tasa_Devolucion`) exige una depuración previa, ya que en un escenario real de predicción futura varios de estos datos no estarían disponibles antes de que ocurra la venta.

---

## 7. Mejoras futuras propuestas

Para evolucionar este modelo en una segunda iteración, como equipo definimos el siguiente plan de acción:

- **Depuración de características:** Eliminar variables posteriores a la venta (`Unidades_Devueltas`, `Tasa_Devolucion`) y auditar las fórmulas de `Rotacion_Inventario` y `Dias_Inventario` para garantizar cero fuga de información.
- **Ampliación y validación:** Incrementar el volumen de registros históricos y sustituir la partición simple 80/20 por validación cruzada de 5 o 10 pliegues (*k-fold CV*).
- **Exploración de algoritmos alternativos:** Comparar nuestra línea base lineal contra modelos regularizados (Ridge, Lasso) y algoritmos basados en árboles (Random Forest Regressor, Gradient Boosting), que manejan mejor relaciones no lineales y múltiples variables categóricas.
- **Ingeniería de características y escalamiento:** Incorporar `StandardScaler` para las variables numéricas y analizar la distribución de `Unidades_Vendidas` para tratar posibles valores atípicos.

---

## 8. Registro de evidencias visuales del repositorio

Las capturas de respaldo se almacenan en la carpeta `DOCS/EVIDENCIAS/` bajo la siguiente estructura:

| Archivo | Evidencia respaldada |
|---|---|
| `01_carga_datos.png` | Carga del CSV y vista preliminar (`df.head()`) |
| `02_exploracion.png` | Estadísticas descriptivas y estructura de columnas |
| `03_calidad_datos.png` | Auditoría de valores nulos, duplicados y tipos de datos |
| `04_variables.png` | Definición de `X`, `y` y clasificación de variables |
| `05_division_datos.png` | Partición 80/20 y dimensiones de entrenamiento/prueba |
| `06_preprocesamiento_modelo.png` | Configuración de `OneHotEncoder` y `Pipeline` |
| `07_entrenamiento.png` | Ejecución del ajuste (`fit`) y generación de predicciones |
| `08_metricas.png` | Salida de métricas MAE, MSE, RMSE y R² |
| `09_graficos.png` | Gráficos comparativos de valores reales frente a predichos |

---

## 9. Fundamentos teóricos y relación con las decisiones

Cada decisión técnica tomada en nuestro flujo de trabajo se sustenta en principios establecidos de la ciencia de datos:

- **Regresión lineal como línea base:** Según James et al. (2021), la regresión lineal por mínimos cuadrados ordinarios constituye el punto de partida estándar en problemas de predicción cuantitativa, permitiendo evaluar si existe una relación lineal directa antes de escalar hacia modelos de mayor complejidad.
- **Codificación One-Hot:** Géron (2022) señala que los algoritmos basados en ecuaciones lineales interpretan los números como magnitudes ordenadas; por ello, el uso de variables indicadoras binarias (`OneHotEncoder`) es fundamental para representar atributos nominales sin introducir sesgos de orden.
- **Aislamiento de datos y Pipelines:** Kuhn y Johnson (2019) advierten que aplicar transformaciones sobre todo el dataset antes de dividirlo filtra estadísticas del conjunto de prueba hacia el entrenamiento. Encapsular el preprocesamiento en un `Pipeline` (Scikit-learn) asegura que los parámetros de transformación se aprendan únicamente sobre `X_train`.
- **Interpretación de métricas de error y R² negativo:** De acuerdo con la documentación oficial de Scikit-learn, mientras el MAE y el RMSE cuantifican la magnitud del error en las unidades originales de la variable objetivo, el coeficiente R² evalúa el ajuste relativo frente a la media; un valor negativo confirma empíricamente que el modelo sobreajusta el ruido de entrenamiento.

### Referencias bibliográficas

- Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3.ª ed.). O'Reilly Media.
- James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning with Applications in R* (2.ª ed.). Springer.
- Kuhn, M., & Johnson, K. (2019). *Feature Engineering and Selection: A Practical Approach for Predictive Models*. CRC Press.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.
- The pandas development team. (2024). *pandas-dev/pandas: Pandas* (Documentación oficial). Zenodo.

---

## 10. Reflexión crítica final

La ejecución de esta bitácora nos permitió consolidar una metodología de trabajo reproducible, pasando de la simple ejecución de código a la documentación razonada de cada decisión técnica. Como equipo consultor, comprobamos que la trazabilidad mediante Git y la estructuración modular del proyecto facilitan enormemente la auditoría y el trabajo colaborativo.

Desde el punto de vista analítico, el principal aprendizaje radica en la interpretación crítica de los resultados: obtener un R² de **-0.8375** y un error medio de **36.21 unidades** demuestra que ajustar un algoritmo sin depurar variables derivadas ni controlar la dimensionalidad produce modelos poco confiables. En consecuencia, determinamos con total rigor profesional que esta primera versión **no debe utilizarse para la toma de decisiones comerciales** en Alkomprar.

Finalmente, reconocemos las limitaciones inherentes al uso de una muestra simulada de 150 registros. No obstante, el flujo construido deja una base sólida, limpia y verificable sobre la cual ejecutaremos nuestra segunda iteración incorporando depuración de fuga de datos, validación cruzada y modelos no lineales.
