# Bitácora digital de experimentación y decisiones analíticas

**Proyecto:** Análisis predictivo de ventas e inventario en Alkomprar  
**Estudiante:** Cristian Julian Vega Florez  
**Programa:** Tecnología en Análisis y Gestión de Datos  
**Institución:** Universidad Tecnológica de Santander (UTS)  
**Asignatura:** Herramientas de Inteligencia Artificial y Ciencia de Datos

## 1. Contexto y objetivo del caso

El ejercicio toma como referencia a Alkomprar y plantea el análisis de información de productos, precios, inventario, ventas, devoluciones y logística. La intención general del trabajo es explorar si estas características permiten construir un modelo predictivo que apoye el análisis comercial.

Aunque el título del notebook original menciona la predicción de la rotación del inventario, al revisar el código se observa que la variable objetivo definida es `Unidades_Vendidas`. Por esta razón, esta bitácora registra el experimento que efectivamente se ejecutó: estimar las unidades vendidas de cada registro mediante regresión lineal. No se presentan las métricas como si fueran una evaluación directa de la rotación.

## 2. Datos y variables seleccionadas

El notebook carga el archivo `alkomprar_datos_inventados.csv` y muestra un conjunto de 150 registros. En el código se identifican 21 columnas: `ID_Producto`, `Categoria`, `Marca`, `Precio_Venta`, `Precio_Competencia`, `Unidades_Vendidas`, `Stock_Disponible`, `Unidades_Devueltas`, `Costo_Operativo`, `Tiempo_Entrega`, `Promocion`, `Devolucion`, `Nivel_Satisfaccion`, `Motivo_Devolucion`, `Temporada`, `Canal_Venta`, `Proveedor`, `Diferencia_Precio`, `Tasa_Devolucion`, `Rotacion_Inventario` y `Dias_Inventario`.

La variable objetivo fue `Unidades_Vendidas`. Se excluyó `ID_Producto` porque funciona como identificador. Las demás 19 columnas se utilizaron como predictoras en el experimento original.

| Tipo | Variables identificadas por el notebook |
|---|---|
| Numéricas | `Precio_Venta`, `Precio_Competencia`, `Stock_Disponible`, `Unidades_Devueltas`, `Costo_Operativo`, `Tiempo_Entrega`, `Diferencia_Precio`, `Tasa_Devolucion`, `Rotacion_Inventario`, `Dias_Inventario` |
| Categóricas | `Categoria`, `Marca`, `Promocion`, `Devolucion`, `Nivel_Satisfaccion`, `Motivo_Devolucion`, `Temporada`, `Canal_Venta`, `Proveedor` |

**Disponibilidad del archivo:** el notebook hace referencia al CSV, pero el archivo CSV no estaba incluido entre los archivos adjuntos. Por lo tanto, se conserva la referencia al nombre original y no se reconstruyen datos faltantes.

## 3. Exploración, limpieza y transformación

Se revisaron las primeras filas, las estadísticas descriptivas, los nombres de las columnas y los tipos de datos. El resultado registrado fue de **0 valores nulos** y **0 registros duplicados**. Las variables numéricas aparecen como `int64` o `float64`, mientras que las categóricas aparecen como `object`.

Como el conjunto no presentó valores nulos, el notebook no necesitó aplicar imputación. Tampoco eliminó registros duplicados, porque el conteo fue cero. Para preparar las variables categóricas se utilizó `OneHotEncoder(handle_unknown='ignore')`, que convierte las categorías en columnas numéricas. Las variables numéricas se dejaron pasar sin transformación mediante `remainder='passthrough'`.

No se observa en el código una estandarización o normalización de las variables numéricas. Esta decisión se registra tal como aparece en el notebook.

## 4. Algoritmo y decisiones de modelado

Se seleccionó **regresión lineal**, un algoritmo de aprendizaje supervisado apropiado para estimar una variable numérica. En este caso, la salida que se busca estimar es la cantidad de unidades vendidas.

El flujo se implementó mediante un `Pipeline`, que primero aplica el preprocesamiento y después entrena el modelo. Se utilizó `ColumnTransformer` para aplicar One-Hot Encoding únicamente a las columnas categóricas y dejar las numéricas sin cambios.

La división de datos se realizó con `train_test_split`, reservando el 80 % para entrenamiento y el 20 % para prueba. Se configuró `random_state=42` para mantener reproducible la partición. El resultado fue de 120 registros de entrenamiento y 30 de prueba. El notebook no especifica otros hiperparámetros del modelo; se utilizó `LinearRegression()` con sus valores predeterminados.

## 5. Resultados y métricas de evaluación

El notebook calculó cuatro métricas sobre el conjunto de prueba:

| Métrica | Resultado | Interpretación |
|---|---:|---|
| MAE | 36,2058 | En promedio, las predicciones se alejaron aproximadamente 36,21 unidades del valor real. |
| MSE | 2967,7389 | Promedio de los errores al cuadrado; penaliza con mayor fuerza los errores grandes. |
| RMSE | 54,4770 | Error típico expresado en la misma unidad de la variable objetivo: unidades vendidas. |
| R² | -0,8375 | El modelo explica mal la variabilidad de los datos de prueba y queda por debajo de una referencia que predice la media. |

Los resultados muestran que el modelo no tuvo un buen desempeño predictivo en esta prueba. El valor negativo de R² es una señal clara de que la regresión lineal, con las variables y datos usados, no logró representar adecuadamente las unidades vendidas. No sería correcto afirmar que el modelo es preciso o que está listo para apoyar decisiones reales.

## 6. Dificultades, limitaciones y ajustes recomendados

Una limitación importante es que el conjunto tiene 150 registros y se describe como datos inventados o simulados. Esto restringe la posibilidad de generalizar los resultados al comportamiento real de una empresa. Además, el R² negativo y el RMSE de aproximadamente 54,48 unidades muestran un error considerable frente a una variable que en los datos observados va de 5 a 177 unidades.

También es necesario revisar la posible **fuga de información** antes de volver a entrenar el modelo. El notebook utiliza como predictoras `Rotacion_Inventario` y `Dias_Inventario`, variables que podrían estar calculadas a partir de las ventas o del inventario y, por tanto, contener indirectamente información relacionada con el objetivo. De igual manera, `Unidades_Devueltas`, `Devolucion`, `Motivo_Devolucion` y `Nivel_Satisfaccion` podrían conocerse después de concretarse una venta. Si el propósito es predecir ventas antes de que ocurran, estas variables no estarían disponibles en el momento de la predicción.

Como ajuste, se recomienda definir primero el momento exacto en que se realizará la predicción y seleccionar únicamente variables disponibles en ese momento. Luego se debe comparar el modelo base con alternativas, por ejemplo un modelo de árbol o Random Forest, mediante la misma partición y métricas. Estos ajustes son recomendaciones para una siguiente experimentación; no se presentan como cambios ya ejecutados ni se les atribuyen resultados.

## 7. Reflexión crítica

Durante el ejercicio se pudo organizar un flujo básico de ciencia de datos: cargar información, explorarla, revisar su calidad, seleccionar variables, preparar datos categóricos, dividir el conjunto, entrenar un modelo y evaluar sus predicciones. El uso de un pipeline facilita mantener el preprocesamiento unido al modelo y reduce el riesgo de aplicar pasos diferentes durante entrenamiento y predicción.

Sin embargo, los resultados también muestran que ejecutar un algoritmo no garantiza obtener predicciones útiles. Es necesario interpretar las métricas y revisar si las variables realmente sirven para anticipar el comportamiento que se quiere estudiar. La calidad, el origen y la representatividad de los datos son fundamentales. Al tratarse de registros simulados, no se puede concluir que el modelo describa las ventas reales de Alkomprar ni que sus resultados se puedan generalizar a otros periodos, productos o empresas.

La principal decisión para una siguiente versión será aclarar el objetivo del proyecto: si se desea predecir unidades vendidas, mantener esa variable objetivo y retirar predictores que generen fuga de información; si se desea predecir rotación, definirla matemáticamente y entrenar un modelo con esa variable como objetivo.

## 8. Evidencias del proceso

Para avalar la transparencia y reproducibilidad del análisis, se han integrado y estructurado capturas de pantalla y archivos de salida indexados dentro del directorio institucional `docs/evidence/` (o la ruta homóloga del repositorio `MiProyectoAnalisis7`). Estos elementos documentan visualmente las siguientes fases del pipeline ejecutadas de forma real:

*   **Carga y Exploración Inicial:** Bloque del notebook donde se lee el archivo `alkomprar_datos_inventados.csv` y se verifican los tipos de datos de las 21 columnas mediante métodos descriptivos.
*   **Conteo de Nulos y Duplicados:** Evidencia explícita del resultado numérico (0 registros nulos y 0 duplicados) que validó la omisión de técnicas de imputación.
*   **Definición del Target y Partición:** Segmentación manual aislando la variable dependiente `Unidades_Vendidas` y la configuración de `train_test_split(..., test_size=0.20, random_state=42)`.
*   **Pipeline de Preprocesamiento y Entrenamiento:** Inicialización del `ColumnTransformer` aislando variables categóricas mediante `OneHotEncoder(handle_unknown='ignore')` y su acoplamiento secuencial con el estimador `LinearRegression()`.
*   **Evaluación del Modelo:** Captura del bloque de la terminal de VS Code que expone las métricas finales (MAE: 36.21, RMSE: 54.48, R²: -0.8375).
*   **Análisis Gráfico:** Gráficos de dispersión que contrastan los valores reales frente a las predicciones puntuales calculadas sobre el conjunto de test.

---

## 9. Conclusión y Reflexión Crítica Final

El experimento permitió estructurar un flujo metodológico completo de ciencia de datos para estimar la variable objetivo `Unidades_Vendidas` en un conjunto simulado de 150 registros comerciales de Alkomprar. A nivel operativo, el uso de pipelines garantizó una separación hermética de las transformaciones de datos, minimizando errores lógicos durante la codificación.

Sin embargo, los resultados estadísticos (MAE de 36.21, RMSE de 54.48 y un R² de -0.8375) determinan un desempeño predictivo críticamente deficiente. Un coeficiente de determinación negativo demuestra formalmente que la regresión lineal por mínimos cuadrados ordinarios no logró extraer patrones útiles de los predictores correlacionados, rindiendo peor que un modelo ingenuo basado simplemente en la media muestral de las ventas. Por este motivo, el modelo actual debe considerarse estrictamente como una primera práctica académica y bajo ninguna circunstancia como una herramienta de soporte analítico para decisiones comerciales reales en Alkomprar.

Para futuras iteraciones experimentales, se establece la necesidad perentoria de:
1. Utilizar un volumen de datos real, robusto y significativamente mayor a 150 registros.
2. Formular con exactitud la variable objetivo del negocio (diferenciando ventas directas de la tasa matemática de rotación de inventarios).
3. Excluir proactivamente predictores que introduzcan fuga de información (*data leakage*), garantizando que el modelo sea evaluado únicamente con variables recolectadas antes del evento de venta.

---

## 10. Fuentes de consulta (Formato APA 7)

*   Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12(Oct), 2825–2830.
*   Scikit-learn developers. (2026). *sklearn.linear_model.LinearRegression*. Scikit-learn documentation. https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
*   Scikit-learn developers. (2026). *sklearn.compose.ColumnTransformer*. Scikit-learn documentation. https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html
*   Scikit-learn developers. (2026). *sklearn.preprocessing.OneHotEncoder*. Scikit-learn documentation. https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
*   Scikit-learn developers. (2026). *Model evaluation: quantifying the quality of predictions*. Scikit-learn User Guide. https://scikit-learn.org/stable/modules/model_evaluation.html
