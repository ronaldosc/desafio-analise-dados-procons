from src.database.database_config import create_connection
import pandas as pd
import matplotlib.pyplot as plt


def execute_query_and_get_dataframe(query, conn):
    return pd.read_sql(query, conn)


def plot_bar_chart(dataframe, title, x_label, y_label):
    dataframe.plot(kind='bar', figsize=(10, 6))
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc='best')
    plt.show()


def plot_line_chart(dataframe, title, x_label, y_label):
    dataframe.plot(kind='line', figsize=(10, 6))
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.show()


# Conectar ao banco de dados
conn = create_connection()
cursor = conn.cursor()

# Consulta 1: Distribuição de Atendimentos por Região
query_regiao = """
SELECT r."nomeRegiao", date_part('quarter', a."dataAtendimento") AS quarter, date_part('year', a."dataAtendimento") AS year, count(*) AS quantidade
FROM "Atendimento" AS a
INNER JOIN "Regiao" AS r ON a."idRegiao" = r."idRegiao"
WHERE date_part('year', a."dataAtendimento") IN (2019, 2020)
GROUP BY r."nomeRegiao", quarter, year
ORDER BY r."nomeRegiao", year, quarter
"""

df_regiao = execute_query_and_get_dataframe(query_regiao, conn)

df_regiao['year_quarter'] = df_regiao['year'].astype(str) + 'Q' + df_regiao['quarter'].astype(str)
df_regiao_pivot = df_regiao.pivot(index='year_quarter', columns='nomeRegiao', values='quantidade')

plot_bar_chart(df_regiao_pivot, 'Distribuição de Atendimentos por Região', 'Trimestre', 'Quantidade de Atendimentos')

# Consulta 2: Região com o Maior Volume de Dados
query_top_regiao_uf = """
SELECT r."nomeRegiao", r."ufRegiao", count(*) AS quantidade
FROM "Atendimento" AS a
INNER JOIN "Regiao" AS r ON a."idRegiao" = r."idRegiao"
WHERE date_part('year', a."dataAtendimento") IN (2019, 2020)
GROUP BY r."nomeRegiao", r."ufRegiao"
ORDER BY quantidade DESC
LIMIT 1
"""

# Consulta 3: Variação de Atendimento por UF
query_variacao_uf = """
SELECT r."ufRegiao", date_part('quarter', a."dataAtendimento") AS quarter, date_part('year', a."dataAtendimento") AS year, count(*) AS quantidade
FROM "Atendimento" AS a
INNER JOIN "Regiao" AS r ON a."idRegiao" = r."idRegiao"
WHERE date_part('year', a."dataAtendimento") IN (2019, 2020)
GROUP BY r."ufRegiao", quarter, year
ORDER BY r."ufRegiao", year, quarter
"""

df_variacao_uf = execute_query_and_get_dataframe(query_variacao_uf, conn)

df_variacao_uf['year_quarter'] = df_variacao_uf['year'].astype(str) + 'Q' + df_variacao_uf['quarter'].astype(str)
df_variacao_uf_pivot = df_variacao_uf.pivot(index='year_quarter', columns='ufRegiao', values='quantidade')

plot_line_chart(df_variacao_uf_pivot, 'Variação de Atendimento por UF', 'Trimestre', 'Quantidade de Atendimentos')

# Fechar cursor e conexão com o banco de dados
cursor.close()
conn.close()
