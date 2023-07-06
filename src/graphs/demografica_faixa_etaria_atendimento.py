from __future__ import annotations

import plotly.graph_objects as go
from database.database_config import create_connection

# Conectar ao banco de dados PostgreSQL
conn = create_connection()


def obter_dados_distribuicao_faixa_etaria():
    # Consulta ao banco de dados para obter a distribuição dos atendimentos por faixa etária do consumidor
    cur = conn.cursor()
    cur.execute('SELECT FaixaEtariaConsumidor, COUNT(*) AS CountAtendimentos FROM Atendimento GROUP BY FaixaEtariaConsumidor')
    data = cur.fetchall()
    cur.close()

    # Processar os dados
    faixas_etarias = []
    contagem = []
    for row in data:
        faixas_etarias.append(row[0])
        contagem.append(row[1])

    # Criar o gráfico de pizza
    fig = go.Figure(data=go.Pie(labels=faixas_etarias, values=contagem))

    fig.update_layout(
        title='Distribuição dos Atendimentos por Faixa Etária do Consumidor',
    )

    return fig.to_html()
