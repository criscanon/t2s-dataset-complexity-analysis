# T2S Dataset Complexity Analysis

This repository contains a Python script that analyzes the complexity of SQL queries extracted from an Excel file. The tool uses the [sqlparse](https://github.com/andialbrecht/sqlparse) library to parse and extract metrics from each query and [matplotlib](https://matplotlib.org/) to generate visualizations that help understand the distribution and complexity of the queries.

---

## Features

The script performs the following analyses on each SQL query:

- **JOIN Count:** Counts the number of `JOIN` clauses used.
- **Subquery Detection:** Counts the number of nested `SELECT` statements (subqueries).
- **WHERE Conditions:** Measures the number of conditions in the `WHERE` clause.
- **SQL Functions:** Counts the number of SQL functions utilized.
- **Table References:** Identifies and counts the tables referenced.
- **GROUP BY and ORDER BY:** Evaluates the presence of `GROUP BY` and `ORDER BY` clauses.
- **Query Length:** Measures the query length in lines and characters.
- **Complexity Metric:** Calculates an overall complexity metric by weighting the above elements.

Additionally, the script generates various visualizations—including histograms, pie charts, and a radar chart—to display the distribution of the analyzed metrics.

---

## Repository Structure

```
t2s-dataset-complexity-analysis/
├── dataset/                           # Contains the Excel file with SQL queries.
├── output/                            # Directory where analysis results and visualizations are saved.
├── LICENSE                            # Project license (MIT).
├── README.md                          # This file.
├── requirements.txt                   # List of required dependencies.
└── run_analysis_complexity_dataset.py # Main Python script to run the analysis.
```

---

## Installation

Follow these steps to set up and run the analysis:

1. **Clone the repository:**
   ```sh
   git clone https://github.com/criscanon/t2s-dataset-complexity-analysis.git
   cd t2s-dataset-complexity-analysis
   ```

2. **Install dependencies:**
   Ensure you have [Python](https://www.python.org/) (version 3.7 or later recommended) installed, then run:
   ```sh
   pip install -r requirements.txt
   ```

3. **Prepare the dataset:**
   - Place your Excel file (e.g., `data-nlq-sql-120.xlsx`) inside the `dataset/` folder.
   - Ensure the file contains a column named `sql` with the SQL queries to analyze.

4. **Run the analysis:**
   ```sh
   python run_analysis_complexity_dataset.py
   ```

---

## Output and Results

After running the script, the following outputs will be generated in the `output/` folder:

- **query_analysis_results.xlsx:** An Excel file containing the metrics extracted for each query.
- **Visualizations:**
  - Histograms for JOINs, subqueries, WHERE conditions, functions, table references, GROUP BY, ORDER BY, query lines, and characters.
  - A histogram of the overall complexity metric.
  - Pie charts and a radar chart showing the composition of the metrics.

Additionally, a summary of the metrics (e.g., the frequency of queries with more than zero JOINs, subqueries, etc.) is printed to the console.

---

## License

This project is licensed under the [MIT License](LICENSE).

---
