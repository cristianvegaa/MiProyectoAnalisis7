#  Bitácora Digital de Experimentación y Decisiones Analíticas

**Proyecto:** Análisis Predictivo de Ventas e Inventario  
**Caso de Estudio:** Alkomprar  
**Consultor Analítico Junior:** Cristian Julian Vega Florez  
**Programa:** Tecnología en Análisis y Gestión de Datos  
**Institución:** Universidad Tecnológica de Santander (UTS)  
**Asignatura:** Herramientas de Inteligencia Artificial y Ciencia de Datos

---

## 1. Contexto del Caso y Objetivo Analítico

El ejercicio toma como referencia operativa a **Alkomprar** y plantea el análisis de información de productos, precios, inventario, ventas, devoluciones y logística. La intención estratégica del trabajo es explorar si estas características permiten construir un modelo predictivo capaz de apoyar la toma de decisiones comerciales y el reabastecimiento seguro de stock.

*Nota de trazabilidad técnica:* Aunque el planteamiento inicial del ejercicio mencionaba la predicción de la rotación del inventario, la auditoría profunda del código demostró que la variable objetivo real (*target*) definida y evaluada es `Unidades_Vendidas`. Como consultores junior, registramos el experimento que efectivamente se ejecutó para garantizar la honestidad intelectual y la coherencia metodológica de la solución.

---

##  2. Datos y Variables Seleccionadas

El modelo se alimenta del dataset piloto `data/raw/alkomprar_datos_inventados.csv`, el cual consolida **150 registros** y **21 columnas**:

*   **Variable Objetivo (Target):** `Unidades_Vendidas` (Numérica).
*   **Variable Excluida:** `ID_Producto`. Se descartó proactivamente del entrenamiento dado que funciona como un identificador único con una cardinalidad igual al total de filas; no aporta valor predictivo y causaría sobreajuste (*overfitting*) destructivo.
*   **Variables Predictoras Conservadas (19 en total):**

| Tipo | Variables Identificadas por el Equipo | Razón de Inclusión Analítica |
|---|---|---|
| **Numéricas** | `Precio_Venta`, `Precio_Competencia`, `Stock_Disponible`, `Unidades_Devueltas`, `Costo_Operativo`, `Tiempo_Entrega`, `Diferencia_Precio`, `Tasa_Devolucion`, `Rotacion_Inventario`, `Dias_Inventario` | Representan la magnitud del comportamiento comercial, costos logísticos y elasticidad de precios competitivos de Alkomprar. |
| **Categóricas** | `Categoria`, `Marca`, `Promocion`, `Devolucion`, `Nivel_Satisfaccion`, `Motivo_Devolucion`, `Temporada`, `Canal_Venta`, `Proveedor` | Representan las dimensiones del contexto comercial, segmentación de productos y variables cualitativas de la experiencia del cliente. |

---

##  3. Registro Cronológico de Experimentos y Decisiones

### Entrada: 10/11/2026 - Fase de Limpieza, Modelado Lineal y Línea Base (Baseline)

*   **Actividad realizada:** Inspección de calidad del dataset piloto, estructuración del pipeline de transformaciones mixtas e inicialización del algoritmo de Regresión Lineal ordinaria.
*   **Decisión tomada:** 
    1. Instalar de forma controlada el stack científico indispensable (`numpy`, `pandas`, `scikit-learn`) en el entorno local de VS Code para mitigar errores de módulos.
    2. Mantener la totalidad de los 150 registros tras comprobar un conteo limpio de **0 valores nulos** y **0 registros duplicados**.
    3. Construir un objeto `ColumnTransformer` aplicando de forma explícita `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` para las variables categóricas, dejando pasar las numéricas con un paso de normalización estándar (`StandardScaler`).
    4. Configurar la división del dataset mediante `train_test_split` reservando el 80% (120 filas) para entrenamiento y el 20% (30 filas) para validación ciega con una semilla fija de reproducibilidad (`random_state=42`).
*   **Justificación:** El uso de un `Pipeline` encapsulado de *scikit-learn* constituye una mejor práctica mandatoria en ciencia de datos, puesto que garantiza que el preprocesamiento de los datos de prueba se mantenga hermético y libre de filtración de información (*data leakage*). La regresión lineal con parámetros por defecto establece nuestra línea base (*baseline*) para medir el grado de complejidad del negocio.
*   **Evidencia:** El código fuente se encuentra automatizado en `SRC/entrenar_modelo.py`. El árbol de directorios limpio se preserva en GitHub y las salidas se guardan en la ruta local `data/processed/`.
*   **Resultado:** 
    El script ejecutó de manera exitosa y arrojó las siguientes métricas estadísticas grabadas en `metricas_modelo.csv`:
    *   **MAE (Error Absoluto Medio):** 36.2058 (En promedio, las predicciones varían en 36.21 unidades frente a la venta real).
    *   **MSE (Error Cuadrático Medio):** 2967.7389 (Métrica de penalización cuadrática para errores grandes).
    *   **RMSE (Raíz del Error Cuadrático Medio):** 54.4770 (Desviación típica típica en la misma unidad física del target).
    *   **R² (Coeficiente de Determinación):** -0.8375.
*   **Reflexión:** Un coeficiente $R^2$ negativo es una bandera roja analítica grave. Explica formalmente que el modelo es incapaz de seguir la variabilidad de los datos de prueba y rinde peor que un estimador ingenuo basado en la simple media aritmética de las ventas. Esto nos comprueba técnicamente dos realidades: que la demanda en Alkomprar no se comporta de forma lineal recta y que la codificación masiva de categorías mediante One-Hot Encoding está inyectando ruido severo que confunde al estimador lineal.

---

## 4. Profundización Analítica: Limitaciones y Riesgos de Negocio

Como consultores analíticos del equipo, identificamos los siguientes riesgos críticos de interpretación antes de transferir estas conclusiones a la toma de decisiones estratégicas de la compañía:

1.  **Riesgo Crítico de Fuga de Información (*Data Leakage*):** Las variables predictoras `Rotacion_Inventario` y `Dias_Inventario` probablemente se calculan de forma matemática usando las ventas pasadas, lo que introduce una filtración circular. De igual manera, variables como `Unidades_Devueltas`, `Devolucion`, `Motivo_Devolucion` y `Nivel_Satisfaccion` corresponden a variables **post-evento**; es decir, Alkomprar solo las conoce *después* de que el cliente ya compró el artículo. Si el objetivo comercial es predecir la demanda futura para planificar las compras del próximo mes, usar estas variables del futuro infla el rendimiento en el laboratorio pero destruye la utilidad práctica del modelo en un entorno de producción real, ya que esas celdas estarán vacías al momento de predecir.
2.  **Restricción del Volumen de Muestra:** Un conjunto piloto de 150 registros simulados limita severamente la capacidad de generalización del modelo ante el comportamiento masivo y estacional de los consumidores reales de Alkomprar.

---

## 5. Conclusión y Acciones de Mejora Futura

*   **Validez del Proceso:** El flujo metodológico implementado y el control de versiones en GitHub son completamente válidos, reproducibles y transparentes. No obstante, el algoritmo seleccionado (Regresión Lineal) queda descartado como solución final debido a su ajuste deficiente ($R^2 < 0$).
*   **Aprendizajes alcanzados:** El ejercicio demostró que un algoritmo avanzado no garantiza predicciones útiles. La fase de preprocesamiento, la interpretación madura de los coeficientes de error y la comprensión del negocio (saber en qué momento del tiempo se genera cada variable) son mucho más importantes que la simple ejecución del código.
*   **Acciones recomendadas para la siguiente iteración:**
    1.  **Saneamiento de la Ventana Temporal:** Eliminar de inmediato las variables post-venta (`Motivo_Devolucion`, `Nivel_Satisfaccion`, etc.) para erradicar la fuga de información.
    2.  **Evolución Algorítmica No Lineal:** Reemplazar el estimador lineal y comparar su rendimiento contra modelos basados en conjuntos de árboles como **Random Forest** o **XGBoost**. Estos algoritmos controlan de forma nativa la alta dimensionalidad de las marcas y proveedores de Alkomprar y capturan interacciones complejas no lineales sin degradar las métricas de evaluación.

---

## 6. Fuentes de Consulta (Normas APA 7)

*   **Hair, J. F., Black, W. C., Babin, B. J., & Anderson, R. E. (2014).** *Multivariate Data Analysis* (7th ed.). Pearson Education.
*   **Kuhn, M., & Johnson, K. (2013).** *Applied Predictive Modeling*. Springer.
*   **Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011).** Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12(Oct), 2825–2830.
*   **Scikit-learn developers. (2026).** *Model evaluation: quantifying the quality of predictions*. Scikit-learn User Guide. https://scikit-learn.org

---

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
