# t2s-dataset-complexity-analysis

Este repositorio contiene un script en Python para analizar la complejidad de consultas SQL extraídas de un archivo Excel. La herramienta utiliza la biblioteca [sqlparse](https://github.com/andialbrecht/sqlparse) para procesar y extraer métricas de cada consulta, y [matplotlib](https://matplotlib.org/) para generar visualizaciones que ayudan a comprender la distribución y complejidad de las consultas.

---

## Características

El script realiza los siguientes análisis sobre cada consulta SQL:

- **Conteo de JOINs**: Determina cuántas veces se utilizan cláusulas `JOIN`.
- **Detección de subconsultas**: Cuenta la cantidad de subconsultas (anidamientos de `SELECT`).
- **Condiciones en WHERE**: Mide el número de condiciones presentes en la cláusula `WHERE`.
- **Funciones SQL**: Cuenta la cantidad de funciones utilizadas.
- **Tablas involucradas**: Identifica y cuenta las tablas referenciadas en la consulta.
- **Agrupaciones y ordenamientos**: Evalúa la presencia de cláusulas `GROUP BY` y `ORDER BY`.
- **Longitud del código**: Mide la longitud de la consulta en líneas y caracteres.
- **Métrica de complejidad**: Calcula una métrica compuesta ponderando cada uno de los elementos anteriores.

Además, el script genera diferentes gráficos (histogramas, gráficos circulares y diagramas de radar) para visualizar la distribución de las métricas analizadas.

---

## Estructura del Repositorio

La organización del repositorio es la siguiente:

```
t2s-dataset-complexity-analysis/
├── dataset/                     # Carpeta con el archivo Excel que contiene las consultas SQL.
├── output/                      # Carpeta donde se guardan los resultados y gráficos generados.
├── LICENSE                      # Archivo de licencia (MIT).
├── README.md                    # Este archivo.
├── requirements.txt             # Archivo con las dependencias necesarias.
└── run_analysis_complexity_dataset.py   # Script principal de ejecución.
```

---

## Instalación

Sigue estos pasos para preparar y ejecutar el análisis:

1. **Clonar el repositorio**
   ```sh
   git clone https://github.com/criscanon/t2s-dataset-complexity-analysis.git
   cd t2s-dataset-complexity-analysis
   ```

2. **Instalar dependencias**
   Asegúrate de tener instalado [Python](https://www.python.org/) (recomendado Python 3.7 o superior) y ejecuta:
   ```sh
   pip install -r requirements.txt
   ```

3. **Preparar el dataset**
   - Coloca el archivo Excel (por ejemplo, `data-nlq-sql-80.xlsx`) dentro de la carpeta `dataset/`.
   - Asegúrate de que el archivo contenga una columna llamada `sql` con las consultas a analizar.

4. **Ejecutar el análisis**
   ```sh
   python run_analysis_complexity_dataset.py
   ```

---

## Salida y Resultados

Al ejecutar el script, se generan los siguientes resultados en la carpeta `output/`:

- **`query_analysis_results.xlsx`**: Archivo Excel con las métricas extraídas para cada consulta.
- **Gráficos de distribución**:
  - Histogramas de JOINs, subconsultas, condiciones en WHERE, funciones, tablas, GROUP BY, ORDER BY, líneas y caracteres.
  - Un histograma de la métrica de complejidad global.
  - Gráficos circulares y un diagrama de radar que muestran la composición de las métricas.

Además, se imprime en consola un resumen de la frecuencia de cada métrica (por ejemplo, cuántas consultas tienen más de cero JOINs, subconsultas, etc.).

---

## Licencia

Este proyecto se distribuye bajo la [Licencia MIT](LICENSE).

---
