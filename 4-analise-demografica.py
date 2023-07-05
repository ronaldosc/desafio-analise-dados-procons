from src.database.database_config import create_connection
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Conectar ao banco de dados
conn = create_connection()

def execute_query_and_get_results(query):
    # Executar a consulta e obter os resultados
    df = pd.read_sql_query(query, conn)
    return df

# Consulta 1: Faixa Etária
query_faixa_etaria = """
SELECT EXTRACT(YEAR FROM "dataAtendimento") AS ano,
       EXTRACT(QUARTER FROM "dataAtendimento") AS trimestre,
       "faixaEtaria",
       COUNT(*) AS ocorrencia
FROM "Atendimento"
WHERE EXTRACT(YEAR FROM "dataAtendimento") IN (2019, 2020)
  AND "faixaEtaria" != 'Nao se aplica'
GROUP BY ano, trimestre, "faixaEtaria"
ORDER BY ano, trimestre, "faixaEtaria";
"""

# Executar a consulta de faixa etária e obter os resultados
df_faixa_etaria = execute_query_and_get_results(query_faixa_etaria)

# Consulta 2: Sexo
query_sexo = """
SELECT EXTRACT(YEAR FROM "dataAtendimento") AS ano,
       EXTRACT(QUARTER FROM "dataAtendimento") AS trimestre,
       "sexo",
       COUNT(*) AS ocorrencia
FROM "Atendimento"
WHERE EXTRACT(YEAR FROM "dataAtendimento") IN (2019, 2020)
  AND "sexo" IS NOT NULL
  AND "sexo" != '0'
GROUP BY ano, trimestre, "sexo"
ORDER BY ano, trimestre, "sexo";
"""

# Executar a consulta de sexo e obter os resultados
df_sexo = execute_query_and_get_results(query_sexo)

# Converter a coluna 'ano' para inteiro nas duas consultas
df_faixa_etaria['ano'] = df_faixa_etaria['ano'].astype(int)
df_sexo['ano'] = df_sexo['ano'].astype(int)

# Configurar estilo do seaborn
sns.set(style='ticks', palette='colorblind')

# Gerar gráficos de barras agrupadas por trimestre e faixa etária
g1 = sns.catplot(x='trimestre', y='ocorrencia', hue='faixaEtaria', col='ano', kind='bar', data=df_faixa_etaria, height=4, aspect=1)
g1.set_titles('Atendimentos por faixa etária - Ano {col_name}')

# Gerar gráficos de barras agrupadas por trimestre e sexo
g2 = sns.catplot(x='trimestre', y='ocorrencia', hue='sexo', col='ano', kind='bar', data=df_sexo, height=4, aspect=1)
g2.set_titles('Ocorrências por sexo do consumidor - Ano {col_name}')

# Definir a consulta SQL
query = """
SELECT "faixaEtaria",
       sub."descricaoAssunto",
       sub.ocorrencia
FROM (
    SELECT "faixaEtaria",
           "descricaoAssunto",
           COUNT(*) AS ocorrencia,
           ROW_NUMBER() OVER (PARTITION BY "faixaEtaria" ORDER BY COUNT(*) DESC) AS rn
    FROM "Atendimento" AS atd
    JOIN "Assunto" AS ast ON atd."idAssunto" = ast."idAssunto"
    WHERE EXTRACT(YEAR FROM atd."dataAtendimento") IN (2019, 2020)
      AND atd."faixaEtaria" != 'Nao se aplica'
    GROUP BY "faixaEtaria", "descricaoAssunto"
) AS sub
WHERE sub.rn = 1
ORDER BY "faixaEtaria";
"""

# Executar a consulta e obter os resultados
df = execute_query_and_get_results(query)

# Configurar estilo do seaborn
sns.set(style='ticks', palette='colorblind')

# Gerar gráfico de barras agrupadas por faixa etária e descrição do assunto
g3 = sns.catplot(x='faixaEtaria', y='ocorrencia', hue='descricaoAssunto', kind='bar', data=df, height=4, aspect=2)
g3.set_titles('Assunto mais relevante - Faixa Etária {col_name}')

# Exibir o gráfico
plt.show()

# Fechar a conexão com o banco de dados
conn.close()
