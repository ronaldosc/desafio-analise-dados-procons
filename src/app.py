from __future__ import annotations

import random

import plotly.graph_objects as go
from database.database_config import create_connection
from flask import Flask
from flask import render_template
from flask import request

# Conectar ao banco de dados PostgreSQL
conn = create_connection()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tendencias')
def tendencias():
    # Consulta ao banco de dados para obter os dados de tendências
    cur = conn.cursor()
    cur.execute('SELECT AnoAtendimento, TrimestreAtendimento, MesAtendimento, COUNT(*) AS CountAtendimentos FROM Atendimento GROUP BY AnoAtendimento, TrimestreAtendimento, MesAtendimento ORDER BY AnoAtendimento, TrimestreAtendimento, MesAtendimento')
    data = cur.fetchall()
    cur.close()

    # Processar os dados
    anos = []
    trimestres = []
    meses = []
    contagem = []
    for row in data:
        anos.append(row[0])
        trimestres.append(row[1])
        meses.append(row[2])
        contagem.append(row[3])

    # Criar o gráfico de barras verticais com cores diferentes para cada ano
    fig = go.Figure()
    for ano in set(anos):
        indices_ano = [i for i, x in enumerate(anos) if x == ano]
        cor = f'rgb({random.randint(0, 255)},{random.randint(0, 255)},{random.randint(0, 255)})'
        fig.add_trace(go.Bar(x=[meses[i] for i in indices_ano], y=[contagem[i]
                      for i in indices_ano], name=str(ano), marker=dict(color=cor)))

    fig.update_layout(
        title='Tendências de Atendimentos',
        xaxis=dict(title='Mês'),
        yaxis=dict(title='Contagem'),
        barmode='group'
    )

    return render_template('tendencias.html', plot=fig.to_html())


if __name__ == '__main__':
    app.run(debug=True)
