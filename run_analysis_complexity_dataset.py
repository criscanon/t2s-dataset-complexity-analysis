import pandas as pd
import sqlparse
import matplotlib.pyplot as plt

# Analysis functions
def parse_sql(query):
    parsed = sqlparse.parse(query)
    return parsed[0] if parsed else None

def count_joins(parsed):
    return sum(1 for token in parsed.tokens if token.ttype is sqlparse.tokens.Keyword and token.value.upper() == 'JOIN')

def _count_subqueries(parsed):
    count = 0
    for item in parsed.tokens:
            if isinstance(item, sqlparse.sql.Parenthesis):
                count += _count_subqueries(item)
            elif isinstance(item, sqlparse.sql.IdentifierList):
                count += _count_subqueries(item)
            elif isinstance(item, sqlparse.sql.Identifier):
                count += _count_subqueries(item)
            elif isinstance(item, sqlparse.sql.Function):
                count += _count_subqueries(item)
            elif isinstance(item, sqlparse.sql.Comparison):
                count += _count_subqueries(item)
            elif isinstance(item, sqlparse.sql.TokenList):
                count += _count_subqueries(item)
            elif item.is_group:
                count += _count_subqueries(item)
            elif item.ttype in (sqlparse.tokens.DML,):
                if item.normalized.lower() == 'select':
                    count += 1
    return count

def count_subqueries(parsed_query):
    return _count_subqueries(parsed_query) - 1 if parsed_query else 0

def count_where_conditions(parsed):
    where_conditions = 0
    where_clause = None

    # Buscamos la cláusula WHERE
    for token in parsed.tokens:
        if isinstance(token, sqlparse.sql.Where):
            where_clause = token
            break

    if where_clause:
        # Contamos las condiciones dentro de la cláusula WHERE
        where_conditions = count_conditions(where_clause)

    return where_conditions

def count_conditions(token):
    conditions_count = 0
    for cond_token in token.tokens:
        if isinstance(cond_token, sqlparse.sql.Comparison):
            conditions_count += 1
        elif isinstance(cond_token, sqlparse.sql.Parenthesis):
            # Si encontramos paréntesis, contamos las condiciones dentro de ellos
            conditions_count += count_conditions(cond_token)
        elif isinstance(cond_token, sqlparse.sql.IdentifierList):
            # Si encontramos una lista de identificadores, contamos las condiciones dentro de ellos
            conditions_count += sum(1 for sub_cond in cond_token.tokens if isinstance(sub_cond, sqlparse.sql.Comparison))
        elif cond_token.normalized in ('BETWEEN', 'IN'):
            conditions_count += 1
        elif cond_token.normalized in ('>', '<', '>=', '<=', '=', '<>', '!='):
            # Si encontramos un operador de comparación, lo contamos como una condición
            conditions_count += 1

    return conditions_count

def count_functions(parsed):
    functions_count = 0
    for token in parsed.tokens:
        functions_count += count_functions_recursive(token)
    return functions_count

def count_functions_recursive(token):
    functions_count = 0

    if isinstance(token, sqlparse.sql.Function):
        functions_count += 1
    elif isinstance(token, sqlparse.sql.IdentifierList):
        for sub_token in token.get_identifiers():
            functions_count += count_functions_recursive(sub_token)
    elif hasattr(token, "tokens"):
        for sub_token in token.tokens:
            functions_count += count_functions_recursive(sub_token)

    return functions_count

def count_tables(parsed):
    tables_count = 0
    from_seen = False

    for token in parsed.tokens:
        if from_seen:
            if isinstance(token, sqlparse.sql.Identifier):
                tables_count += 1
            elif isinstance(token, sqlparse.sql.IdentifierList):
                tables_count += sum(1 for sub_token in token.tokens if isinstance(sub_token, sqlparse.sql.Identifier))
            elif isinstance(token, sqlparse.sql.TokenList):
                tables_count += count_tables(token)
            elif token.ttype is sqlparse.tokens.Keyword and token.value.upper() in ('WHERE', 'GROUP BY', 'ORDER BY', 'LIMIT'):
                break
        if token.ttype is sqlparse.tokens.Keyword and token.value.upper() == 'FROM':
            from_seen = True

    return tables_count

def count_group_by(parsed):
    group_by_seen = False
    count = 0
    for token in parsed.tokens:
        if group_by_seen and token.ttype is sqlparse.tokens.Keyword:
            break
        if token.ttype is sqlparse.tokens.Keyword and token.value.upper() == 'GROUP BY':
            group_by_seen = True
        if group_by_seen and isinstance(token, sqlparse.sql.IdentifierList):
            count += len(list(token.get_identifiers()))
        elif group_by_seen and isinstance(token, sqlparse.sql.Identifier):
            count += 1
    return count

def count_order_by(parsed):
    order_by_seen = False
    count = 0
    for token in parsed.tokens:
        if order_by_seen and token.ttype is sqlparse.tokens.Keyword:
            break
        if token.ttype is sqlparse.tokens.Keyword and token.value.upper() == 'ORDER BY':
            order_by_seen = True
        if order_by_seen and isinstance(token, sqlparse.sql.IdentifierList):
            count += len(list(token.get_identifiers()))
        elif order_by_seen and isinstance(token, sqlparse.sql.Identifier):
            count += 1
    return count

def query_length(query):
    return len(query.splitlines()), len(query)

# General complexity metric
def calculate_complexity(row):
    complexity = (
        row['joins'] * 1.5 +
        row['subqueries'] * 2 +
        row['where_conditions'] * 1 +
        row['functions'] * 1.5 +
        row['tables'] * 1 +
        row['group_by'] * 1 +
        row['order_by'] * 1 
        # row['lines'] * 0.5 +
        # row['characters'] * 0.01
    )
    return complexity

# Read the Excel file
file_path = 'dataset\data-nlq-sql-120.xlsx'  # Update the file name as needed dataset\data-nlq-sql-80.xlsx
df = pd.read_excel(file_path)

# Assume the queries are in a column called 'query'
queries = df['sql'].tolist()

# Analyze the queries
results = []

for query in queries:
    parsed_query = parse_sql(query)
    if parsed_query:
        result = {
            "query": query,
            "joins": count_joins(parsed_query),
            "subqueries": count_subqueries(parsed_query),
            "where_conditions": count_where_conditions(parsed_query),
            "functions": count_functions(parsed_query),
            "tables": count_tables(parsed_query),
            "group_by": count_group_by(parsed_query),
            "order_by": count_order_by(parsed_query),
            "lines": query_length(query)[0],
            "characters": query_length(query)[1]
        }
        results.append(result)

# Create a DataFrame with the results
results_df = pd.DataFrame(results)

# Calculate the overall complexity
results_df['complexity'] = results_df.apply(calculate_complexity, axis=1)

# Show the DataFrame
print(results_df)

# Save the results to an Excel file
results_df.to_excel('output/query_analysis_results.xlsx', index=False)

# Generate graphs
plt.figure(figsize=(12, 8))

# Histogram of the number of joins
plt.subplot(3, 3, 1)
plt.hist(results_df['joins'], bins=10, color='skyblue', edgecolor='black')
plt.title('Distribution of the number of Joins')
plt.xlabel('Number of Joins')
plt.ylabel('Frequency')

# Histogram of the number of subqueries
plt.subplot(3, 3, 2)
plt.hist(results_df['subqueries'], bins=10, color='lightgreen', edgecolor='black')
plt.title('Distribution of the number of Subqueries')
plt.xlabel('Number of Subqueries')
plt.ylabel('Frequency')

# Histogram of the number of conditions in WHERE
plt.subplot(3, 3, 3)
plt.hist(results_df['where_conditions'], bins=10, color='salmon', edgecolor='black')
plt.title('Distribution of the number of conditions in WHERE')
plt.xlabel('Number of Conditions')
plt.ylabel('Frequency')

# Histogram of the number of functions
plt.subplot(3, 3, 4)
plt.hist(results_df['functions'], bins=10, color='lightcoral', edgecolor='black')
plt.title('Distribution of the number of Functions')
plt.xlabel('Number of Functions')
plt.ylabel('Frequency')

# Histogram of the number of tables
plt.subplot(3, 3, 5)
plt.hist(results_df['tables'], bins=10, color='orange', edgecolor='black')
plt.title('Distribution of the number of Tables')
plt.xlabel('Number of Tables')
plt.ylabel('Frequency')

# Histogram of the number of GROUP BY columns
plt.subplot(3, 3, 6)
plt.hist(results_df['group_by'], bins=10, color='purple', edgecolor='black')
plt.title('Distribution of the number of GROUP BY')
plt.xlabel('Number of GROUP BY')
plt.ylabel('Frequency')

# Histogram of the number of ORDER BY columns
plt.subplot(3, 3, 7)
plt.hist(results_df['order_by'], bins=10, color='brown', edgecolor='black')
plt.title('Distribution of the number of ORDER BY')
plt.xlabel('Number of ORDER BY')
plt.ylabel('Frequency')

# Histogram of code length (lines)
plt.subplot(3, 3, 8)
plt.hist(results_df['lines'], bins=10, color='gray', edgecolor='black')
plt.title('Distribution of code length (lines)')
plt.xlabel('Number of Lines')
plt.ylabel('Frequency')

# Histogram of code length (characters)
plt.subplot(3, 3, 9)
plt.hist(results_df['characters'], bins=10, color='teal', edgecolor='black')
plt.title('Distribution of code length (characters)')
plt.xlabel('Number of Characters')
plt.ylabel('Frequency')

plt.tight_layout()
plt.savefig('output/distribution_histograms.png')
plt.show()


# Histogram of overall complexity
plt.figure(figsize=(8, 6))
plt.hist(results_df['complexity'], bins=10, color='navy', edgecolor='black')
plt.title('Distribution of Overall Complexity')
plt.xlabel('Complexity')
plt.ylabel('Frequency')
plt.savefig('output/complexity.png')
plt.show()

import matplotlib.pyplot as plt

# Datos
columns = ['joins', 'subqueries', 'where_conditions', 'functions', 'tables', 'group_by', 'order_by']
colors = ['skyblue', 'lightgreen', 'salmon', 'lightcoral', 'orange', 'purple', 'brown']

# Filtrar columnas que existen en results_df
existing_columns = [col for col in columns if col in results_df.columns]

# Limitar a 7 subplots
existing_columns = existing_columns[:7]

# Calcular el número de filas y columnas necesarias para acomodar los subplots
num_cols = min(len(existing_columns), 3)
num_rows = (len(existing_columns) - 1) // num_cols + 1

# Crear figura y subtramas
fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, 2.5*num_rows), constrained_layout=True)

# Iterar sobre cada columna existente y crear los subplots correspondientes
for i, col in enumerate(existing_columns):
    ax = axs.flatten()[i]
    counts = results_df[col].value_counts()

    if len(counts) > 0:
        wedges, texts, autotexts = ax.pie(counts, labels=None, autopct='', colors=plt.cm.tab20.colors[:len(counts)])

        # Obtener porcentajes para la tabla de convención
        percentages = [(count / sum(counts) * 100) for count in counts]

        # Añadir leyenda con convención y porcentajes
        legend_labels = [f'{label} ({percent:.1f}%)' for label, percent in zip(counts.index, percentages)]
        ax.legend(wedges, legend_labels,
                  title=f'{col.capitalize()}',
                  loc='center left',
                  bbox_to_anchor=(1, 0, 0.5, 1))

        ax.set_title(f'Distribution of {col.capitalize()}')
    else:
        # Eliminar el subplot vacío
        fig.delaxes(ax)

# Ajustes de layout
plt.tight_layout()
plt.savefig('output/distribution_circular.png')
# Mostrar gráfico
plt.show()




import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Filtrar y contar valores mayores a cero
greater_than_zero = results_df[['joins', 'subqueries', 'where_conditions', 'functions', 'tables', 'group_by', 'order_by']] > 0
greater_than_zero_counts = greater_than_zero.sum()

# Mostrar los resultados
for metric, count in greater_than_zero_counts.items():
    print(f"Metric: {metric}")
    print(f"   Greater than zero frequency: {count}")
    print()

# Diagrama de radar
metrics = greater_than_zero_counts.index
values = greater_than_zero_counts.values

angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]  # Agrega el primer ángulo al final para cerrar el gráfico

# Calcular los valores para cerrar el gráfico
values = np.concatenate((values, [values[0]]))

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Añadir el área sombreada y la línea del gráfico
ax.fill(angles, values, color='skyblue', alpha=0.4)
ax.plot(angles, values, color='navy', linewidth=2, linestyle='solid')

# Etiquetar los valores en el gráfico con valores absolutos
for angle, value, metric in zip(angles[:-1], values[:-1], metrics):
    ax.text(angle, value + 5, f"{value}", ha='center', va='center', fontsize=10, color='navy')

# Ajustar los ejes para que estén proporcionales
ax.set_ylim(0, 90)

# Añadir escalas
ax.set_yticks([30, 60, 90, 120, 150])  # Define las escalas de los valores absolutos
ax.set_yticklabels([])  # Elimina las etiquetas de las escalas

# Añadir las etiquetas de los nombres de métricas con un desplazamiento angular y radial
ax.set_xticks(angles[:-1])
ax.set_xticklabels(metrics, fontsize=10, fontweight='bold', color='black', ha='center')

# Quitar la línea más externa del gráfico
ax.spines['polar'].set_visible(False)

# Añadir título y ajustar espaciado
plt.title('Composición del conjunto de datos versión 2', fontsize=16, fontweight='bold', pad=50)  # Ajusta el pad para mayor separación

# Mostrar el gráfico
plt.tight_layout()
plt.savefig('output/distribution_radar.png')
plt.show()
