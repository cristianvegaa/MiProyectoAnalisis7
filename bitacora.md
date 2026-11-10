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

Se deben agregar en `docs/evidence/` capturas del notebook que muestren: carga del conjunto de datos, exploración inicial, conteo de nulos y duplicados, selección de la variable objetivo, división entrenamiento/prueba, pipeline, entrenamiento, tabla de métricas y gráficos de valores reales frente a predichos. Las capturas deben corresponder a la ejecución real del notebook.

## 9. Conclusión

El experimento permitió construir y evaluar un modelo de regresión lineal para estimar `Unidades_Vendidas` en un conjunto simulado de 150 registros de Alkomprar. Se identificó que los datos revisados no tenían valores nulos ni duplicados y se aplicó One-Hot Encoding a las variables categóricas. La evaluación obtuvo MAE de 36,21, RMSE de 54,48 y R² de -0,8375, lo que indica un desempeño insuficiente. Por ello, el modelo debe considerarse una primera práctica académica y no una herramienta lista para decisiones comerciales. Para mejorarlo se necesita trabajar con datos reales y suficientes, definir con precisión la variable objetivo y evitar predictores que puedan filtrar información futura.

## 10. Fuentes de consulta

- Scikit-learn. (s. f.). *LinearRegression*. https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
- Scikit-learn. (s. f.). *ColumnTransformer*. https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html
- Scikit-learn. (s. f.). *OneHotEncoder*. https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
- Scikit-learn. (s. f.). *Model evaluation: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html
