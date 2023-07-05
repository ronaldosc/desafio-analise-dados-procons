from src.database.database_config import create_connection
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap

conn = create_connection()
cursor = conn.cursor()

# Consulta SQL para identificar os 5 assuntos mais recorrentes em 2019
assuntos_2019_query = """
SELECT "descricaoAssunto" AS "assunto",
COUNT(*) AS total
FROM "Atendimento"
JOIN "Assunto" ON "Atendimento"."idAssunto" = "Assunto"."idAssunto"
WHERE EXTRACT(YEAR FROM "dataAtendimento") = 2019
GROUP BY "assunto"
ORDER BY total DESC
LIMIT 5
"""

# Consulta SQL para identificar os 5 assuntos mais recorrentes em 2020
assuntos_2020_query = """
SELECT "descricaoAssunto" AS "assunto",
COUNT(*) AS total
FROM "Atendimento"
JOIN "Assunto" ON "Atendimento"."idAssunto" = "Assunto"."idAssunto"
WHERE EXTRACT(YEAR FROM "dataAtendimento") = 2020
GROUP BY "assunto"
ORDER BY total DESC
LIMIT 5
"""

# Consulta SQL para identificar os 5 problemas mais recorrentes em 2019
problemas_2019_query = """
SELECT "descricaoProblema" AS "problema",
COUNT(*) AS total
FROM "Atendimento"
JOIN "Problema" ON "Atendimento"."idProblema" = "Problema"."idProblema"
WHERE EXTRACT(YEAR FROM "dataAtendimento") = 2019
GROUP BY "problema"
ORDER BY total DESC
LIMIT 5
"""

# Consulta SQL para identificar os 5 problemas mais recorrentes em 2020
problemas_2020_query = """
SELECT "descricaoProblema" AS "problema",
COUNT(*) AS total
FROM "Atendimento"
JOIN "Problema" ON "Atendimento"."idProblema" = "Problema"."idProblema"
WHERE EXTRACT(YEAR FROM "dataAtendimento") = 2020
GROUP BY "problema"
ORDER BY total DESC
LIMIT 5
"""

# Executar as consultas SQL
assuntos_2019_data = pd.read_sql_query(assuntos_2019_query, conn)
assuntos_2020_data = pd.read_sql_query(assuntos_2020_query, conn)
problemas_2019_data = pd.read_sql_query(problemas_2019_query, conn)
problemas_2020_data = pd.read_sql_query(problemas_2020_query, conn)

# Fechar a conexão com o banco de dados
conn.close()

# Função para quebrar as descrições em várias linhas
def wrap_text(text, width):
    return '\n'.join(textwrap.wrap(text, width=width))

# Ajustar as descrições dos problemas e assuntos
assuntos_2019_data['assunto'] = assuntos_2019_data['assunto'].apply(lambda x: wrap_text(x, 20))
assuntos_2020_data['assunto'] = assuntos_2020_data['assunto'].apply(lambda x: wrap_text(x, 20))
problemas_2019_data['problema'] = problemas_2019_data['problema'].apply(lambda x: wrap_text(x, 20))
problemas_2020_data['problema'] = problemas_2020_data['problema'].apply(lambda x: wrap_text(x, 20))

# Criar o gráfico para os assuntos mais recorrentes
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.barplot(x="total", y="assunto", data=assuntos_2019_data, color="skyblue")
plt.xlabel("Total de Reclamações")
plt.ylabel("Assunto")
plt.title("Top 5 Assuntos Mais Recorrentes (2019)")

plt.subplot(1, 2, 2)
sns.barplot(x="total", y="assunto", data=assuntos_2020_data, color="lightgreen")
plt.xlabel("Total de Reclamações")
plt.ylabel("Assunto")
plt.title("Top 5 Assuntos Mais Recorrentes (2020)")

plt.tight_layout()
plt.show()

# Criar o gráfico para os problemas mais recorrentes
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.barplot(x="total", y="problema", data=problemas_2019_data, color="skyblue")
plt.xlabel("Total de Reclamações")
plt.ylabel("Problema")
plt.title("Top 5 Problemas Mais Recorrentes (2019)")

plt.subplot(1, 2, 2)
sns.barplot(x="total", y="problema", data=problemas_2020_data, color="lightgreen")
plt.xlabel("Total de Reclamações")
plt.ylabel("Problema")
plt.title("Top 5 Problemas Mais Recorrentes (2020)")

plt.tight_layout()
plt.show()
