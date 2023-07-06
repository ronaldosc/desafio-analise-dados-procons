from __future__ import annotations

import random

import plotly.graph_objects as go
from database.database_config import create_connection
from flask import Flask
from flask import render_template
from flask import request
from graphs.demografica_faixa_etaria_atendimento import obter_dados_distribuicao_faixa_etaria
from graphs.demografica_genero_atendimento import obter_dados_distribuicao_genero
from graphs.geografica_regiao_distribuicao import obter_dados_distribuicao_regiao
from graphs.geografica_regiao_variacao import obter_dados_variacao_tempo
from graphs.reclamacao_assuntos import obter_dados_assuntos_recorrentes
from graphs.reclamacao_problema_comum import obter_dados_problemas_comuns
from graphs.reclamacao_problema_regiao import obter_dados_destaques_regiao_uf
from graphs.temporal_sazonalidade import obter_dados_sazonalidade
from graphs.temporal_tendencias import obter_dados_tendencias

# Conectar ao banco de dados PostgreSQL
conn = create_connection()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tendencias')
def tendencias():
    plot = obter_dados_tendencias()
    return render_template('tendencias.html', plot=plot)


@app.route('/sazonalidade')
def sazonalidade():
    plot = obter_dados_sazonalidade()
    return render_template('sazonalidade.html', plot=plot)


@app.route('/mapa')
def mapa():
    plot = obter_dados_distribuicao_regiao()
    return render_template('mapa.html', plot=plot)


@app.route('/variacao-tempo')
def variacao_tempo():
    plot = obter_dados_variacao_tempo()
    return render_template('variacao_tempo.html', plot=plot)


@app.route('/assuntos-recorrentes')
def assuntos_recorrentes():
    ano_selecionado = request.args.get('ano')
    plot = obter_dados_assuntos_recorrentes(ano_selecionado)
    return render_template('assuntos_recorrentes.html', plot=plot)


@app.route('/problemas-comuns')
def problemas_comuns():
    ano_selecionado = request.args.get('ano')
    plot = obter_dados_problemas_comuns(ano_selecionado)
    return render_template('problemas_comuns.html', plot=plot)


@app.route('/destaques-regiao-uf')
def destaques_regiao_uf():
    uf_regiao = request.args.get('uf_regiao')
    plot = obter_dados_destaques_regiao_uf(uf_regiao)
    return render_template('destaques_regiao_uf.html', plot=plot)


@app.route('/distribuicao-genero')
def distribuicao_sexo():
    plot = obter_dados_distribuicao_genero()
    return render_template('distribuicao_genero.html', plot=plot)


@app.route('/distribuicao-faixa-etaria')
def distribuicao_faixa_etaria():
    plot = obter_dados_distribuicao_faixa_etaria()
    return render_template('distribuicao_faixa_etaria.html', plot=plot)


@app.route('/principais-problemas-genero')
def principais_problemas_genero():
    # Consulta ao banco de dados para obter os principais problemas relatados por diferentes gêneros
    cur = conn.cursor()
    cur.execute('SELECT Problema.DescricaoProblema, Atendimento.SexoConsumidor, COUNT(*) AS CountProblemas FROM Atendimento INNER JOIN Problema ON Atendimento.CodigoProblema = Problema.CodigoProblema GROUP BY Problema.DescricaoProblema, Atendimento.SexoConsumidor ORDER BY CountProblemas DESC')
    data = cur.fetchall()
    cur.close()

    # Processar os dados
    problemas = []
    generos = []
    contagem = []
    for row in data:
        problema = row[0].split('(')[0].strip()
        genero = row[1]
        count = row[2]

        if problema not in problemas:
            problemas.append(problema)
        if genero not in generos:
            generos.append(genero)

        contagem.append(count)

    # Ordenar os problemas por contagem decrescente
    problemas_ordenados = [problema for _, problema in sorted(zip(contagem, problemas), reverse=True)]
    problemas_5 = problemas_ordenados[:5]

    # Filtrar os dados apenas para os 5 problemas mais frequentes
    filtered_data = [row for row in data if row[0] in problemas_5]

    # Criar o gráfico de barras
    fig = go.Figure()

    for genero in generos:
        genero_contagem = [row[2] for row in filtered_data if row[1] == genero]
        fig.add_trace(go.Bar(x=problemas_5, y=genero_contagem, name=genero))

    fig.update_layout(
        title='Principais Problemas Relatados por Gênero',
        xaxis=dict(title='Problema'),
        yaxis=dict(title='Contagem')
    )

    return render_template('principais_problemas_genero.html', plot=fig.to_html())


@app.route('/principais-problemas-faixa-etaria')
def principais_problemas_faixa_etaria():
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

    return render_template('principais_problemas_faixa_etaria.html', plot=fig.to_html())


if __name__ == '__main__':
    app.run(debug=True)
