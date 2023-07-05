from src.database.database_config import create_connection
import pandas as pd
import matplotlib.pyplot as plt

# Conectar ao banco de dados
conn = create_connection()
cursor = conn.cursor()

# Consulta 1: Atendimentos por trimestre
query_atendimento = """
SELECT date_part('quarter', "dataAtendimento") AS quarter,
      date_part('year', "dataAtendimento") AS year,
      count(*) AS quantidade
FROM "Atendimento"
WHERE date_part('year', "dataAtendimento") IN (2019, 2020)
GROUP BY quarter, year
ORDER BY year, quarter
"""

# Executar a consulta e obter os resultados
df = pd.read_sql(query_atendimento, conn)

# Criar coluna 'year_quarter'
df['year_quarter'] = df['year'].astype(str) + 'Q' + df['quarter'].astype(str)

# Pivotar os dados
df_pivot = df.pivot(index='year_quarter', columns='year', values='quantidade')

# Gerar gráfico de barras dos atendimentos por trimestre
df_pivot.plot(kind='bar', figsize=(10, 6))
plt.title('Quantidade de Atendimentos por Trimestre')
plt.xlabel('Trimestre')
plt.ylabel('Quantidade de Atendimentos')
plt.show()

# Consulta 2: Tendências de atendimentos por mês
query_tendencias = """
SELECT date_trunc('month', "dataAtendimento") AS mes, COUNT(*) AS total_atendimentos
FROM "Atendimento"
WHERE date_part('year', "dataAtendimento") IN (2019, 2020)
GROUP BY mes
ORDER BY mes
"""

# Executar a consulta e obter os resultados
cursor.execute(query_tendencias)
results = cursor.fetchall()

# Extrair os dados retornados da consulta
meses = []
total_atendimentos = []

for row in results:
    mes = row[0]
    total = row[1]
    meses.append(mes)
    total_atendimentos.append(total)

# Gerar gráfico de tendências de atendimentos
plt.plot(meses, total_atendimentos)
plt.xlabel('Mês')
plt.ylabel('Total de Atendimentos')
plt.title('Tendências de Atendimentos (2019-2020)')
plt.xticks(rotation=45)
plt.show()

# Fechar cursor e conexão com o banco de dados
cursor.close()
conn.close()
