from __future__ import annotations

import plotly.graph_objects as go
from database.database_config import create_connection

# Conectar ao banco de dados PostgreSQL
conn = create_connection()


def obter_dados_principais_problemas_faixa_etaria():
    # Consulta ao banco de dados para obter os principais problemas relatados por faixa etária
    cur = conn.cursor()
    cur.execute('SELECT Problema.DescricaoProblema, Atendimento.FaixaEtariaConsumidor, COUNT(*) AS CountProblemas FROM Atendimento INNER JOIN Problema ON Atendimento.CodigoProblema = Problema.CodigoProblema GROUP BY Problema.DescricaoProblema, Atendimento.FaixaEtariaConsumidor ORDER BY CountProblemas DESC')
    data = cur.fetchall()
    cur.close()

    # Processar os dados
    problemas = []
    faixas_etarias = []
    contagem = []
    for row in data:
        problema = row[0]
        faixa_etaria = row[1]
        count = row[2]

        if problema not in problemas:
            problemas.append(problema)
        if faixa_etaria not in faixas_etarias:
            faixas_etarias.append(faixa_etaria)

        contagem.append(count)

    # Ordenar os problemas por contagem decrescente
    problemas_ordenados = [problema for _, problema in sorted(zip(contagem, problemas), reverse=True)]
    problemas_5 = problemas_ordenados[:5]

    # Filtrar os dados apenas para os 5 problemas mais frequentes
    filtered_data = [row for row in data if row[0] in problemas_5]

    # Criar o gráfico de barras
    fig = go.Figure()

    for faixa_etaria in faixas_etarias:
        faixa_etaria_contagem = [row[2] for row in filtered_data if row[1] == faixa_etaria]
        texto = [f'Faixa Etária: {faixa_etaria}' for _ in range(len(problemas_5))]
        fig.add_trace(go.Bar(x=problemas_5, y=faixa_etaria_contagem, name=faixa_etaria, hovertext=texto))

    fig.update_layout(
        title='Principais Problemas Relatados por Faixa Etária',
        xaxis=dict(title='Problema'),
        yaxis=dict(title='Contagem')
    )

    return fig.to_html()
