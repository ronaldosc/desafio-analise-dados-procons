from __future__ import annotations

import random

import plotly.graph_objects as go
from database.database_config import create_connection
from flask import Flask
from flask import render_template
from flask import request
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
    # Consulta ao banco de dados para obter os dados de sazonalidade
    cur = conn.cursor()
    cur.execute('SELECT AnoAtendimento, MesAtendimento, COUNT(*) AS CountAtendimentos FROM Atendimento GROUP BY AnoAtendimento, MesAtendimento ORDER BY AnoAtendimento, MesAtendimento')
    data = cur.fetchall()
    cur.close()

    # Processar os dados
    anos = []
    meses = []
    contagem = []
    for row in data:
        anos.append(row[0])
        meses.append(row[1])
        contagem.append(row[2])

    # Criar o gráfico de retas com cores diferentes para cada ano
    fig = go.Figure()
    for ano in set(anos):
        indices_ano = [i for i, x in enumerate(anos) if x == ano]
        cor = f'rgb({random.randint(0, 255)},{random.randint(0, 255)},{random.randint(0, 255)})'
        fig.add_trace(go.Scatter(x=[meses[i] for i in indices_ano], y=[contagem[i]
                      for i in indices_ano], mode='lines', name=str(ano), line=dict(color=cor)))

    fig.update_layout(
        title='Sazonalidade de Atendimentos',
        xaxis=dict(title='Mês'),
        yaxis=dict(title='Contagem')
    )

    return render_template('sazonalidade.html', plot=fig.to_html())


@app.route('/mapa')
def mapa():
    # Consulta ao banco de dados para obter a distribuição dos atendimentos por região
    cur = conn.cursor()
    cur.execute('SELECT Regiao, COUNT(*) AS CountAtendimentos FROM Atendimento INNER JOIN Regiao ON Atendimento.CodigoRegiao = Regiao.CodigoRegiao GROUP BY Regiao ORDER BY Regiao')
    data = cur.fetchall()
    cur.close()

    # Processar os dados
    regioes = []
    contagem = []
    for row in data:
        regioes.append(row[0])
        contagem.append(row[1])

    # Criar o gráfico de pizza
    fig = go.Figure(data=go.Pie(labels=regioes, values=contagem))

    return render_template('mapa.html', plot=fig.to_html())


@app.route('/variacao-tempo')
def variacao_tempo():
    # Consulta ao banco de dados para obter a variação dos atendimentos por região ou UF ao longo do tempo
    cur = conn.cursor()
    cur.execute('SELECT DataAtendimento, Regiao, COUNT(*) AS CountAtendimentos FROM Atendimento INNER JOIN Regiao ON Atendimento.CodigoRegiao = Regiao.CodigoRegiao GROUP BY DataAtendimento, Regiao ORDER BY DataAtendimento, Regiao')
    data = cur.fetchall()
    cur.close()

    # Processar os dados
    datas = []
    regioes = []
    contagem = []
    for row in data:
        datas.append(row[0])
        regioes.append(row[1])
        contagem.append(row[2])

    # Criar o gráfico de linhas
    fig = go.Figure()
    for regiao in set(regioes):
        indices_regiao = [i for i, x in enumerate(regioes) if x == regiao]
        fig.add_trace(go.Scatter(x=[datas[i] for i in indices_regiao], y=[contagem[i]
                      for i in indices_regiao], mode='lines', name=str(regiao)))

    fig.update_layout(
        title='Variação dos Atendimentos por Região ou UF',
        xaxis=dict(title='Data de Atendimento'),
        yaxis=dict(title='Contagem')
    )

    return render_template('variacao_tempo.html', plot=fig.to_html())


@app.route('/assuntos-recorrentes')
def assuntos_recorrentes():
    # Consulta ao banco de dados para obter os assuntos mais recorrentes nas reclamações
    ano_selecionado = request.args.get('ano')

    cur = conn.cursor()
    query = 'SELECT Assunto.DescricaoAssunto, COUNT(*) AS CountReclamacoes FROM Atendimento INNER JOIN Assunto ON Atendimento.CodigoAssunto = Assunto.CodigoAssunto'
    if ano_selecionado:
        query += f' WHERE EXTRACT(YEAR FROM Atendimento.DataAtendimento) = {ano_selecionado}'
    query += ' GROUP BY Assunto.DescricaoAssunto ORDER BY CountReclamacoes DESC LIMIT 5'

    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    # Processar os dados
    assuntos = []
    contagem = []
    for row in data:
        assunto = row[0].split('(')[0].strip()
        assuntos.append(assunto)
        contagem.append(row[1])

    # Criar o gráfico de barras
    fig = go.Figure(data=go.Bar(x=assuntos, y=contagem))

    fig.update_layout(
        title='Assuntos Mais Recorrentes nas Reclamações',
        xaxis=dict(title='Assunto'),
        yaxis=dict(title='Contagem')
    )

    return render_template('assuntos_recorrentes.html', plot=fig.to_html())


@app.route('/problemas-comuns')
def problemas_comuns():
    # Consulta ao banco de dados para obter os problemas mais comuns relatados pelos consumidores
    ano_selecionado = request.args.get('ano')

    cur = conn.cursor()
    query = 'SELECT Problema.DescricaoProblema, COUNT(*) AS CountProblemas FROM Atendimento INNER JOIN Problema ON Atendimento.CodigoProblema = Problema.CodigoProblema'
    if ano_selecionado:
        query += f' WHERE EXTRACT(YEAR FROM Atendimento.DataAtendimento) = {ano_selecionado}'
    query += ' GROUP BY Problema.DescricaoProblema ORDER BY CountProblemas DESC LIMIT 5'

    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    # Processar os dados
    problemas = []
    contagem = []
    for row in data:
        problema = row[0].split('(')[0].strip()
        problemas.append(problema)
        contagem.append(row[1])

    # Criar o gráfico de barras
    fig = go.Figure(data=go.Bar(x=problemas, y=contagem))

    fig.update_layout(
        title='Problemas Mais Comuns Relatados pelos Consumidores',
        xaxis=dict(title='Problema'),
        yaxis=dict(title='Contagem')
    )

    return render_template('problemas_comuns.html', plot=fig.to_html())


@app.route('/destaques-regiao-uf')
def destaques_regiao_uf():
    # Consulta ao banco de dados para verificar os assuntos e problemas que se destacam em determinadas regiões ou UF
    uf_regiao = request.args.get('uf_regiao')

    cur = conn.cursor()
    query = 'SELECT Regiao, UF, Assunto.DescricaoAssunto, Problema.DescricaoProblema, COUNT(*) AS Contagem FROM Atendimento INNER JOIN Regiao ON Atendimento.CodigoRegiao = Regiao.CodigoRegiao INNER JOIN Assunto ON Atendimento.CodigoAssunto = Assunto.CodigoAssunto INNER JOIN Problema ON Atendimento.CodigoProblema = Problema.CodigoProblema'
    if uf_regiao:
        query += f" WHERE Regiao = '{uf_regiao}' OR UF = '{uf_regiao}'"
    query += ' GROUP BY Regiao, UF, Assunto.DescricaoAssunto, Problema.DescricaoProblema ORDER BY Contagem DESC'

    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    # Processar os dados
    regioes_uf = []
    assuntos = []
    contagem = []
    for row in data:
        regiao_uf = f'{row[0]} - {row[1]}'
        assuntos.append(row[2])
        contagem.append(row[4])
        regioes_uf.append(regiao_uf)

    # Criar o gráfico de barras
    fig = go.Figure(data=go.Bar(x=regioes_uf, y=contagem))

    fig.update_layout(
        title='Destaques por Região ou UF',
        xaxis=dict(title='Região ou UF'),
        yaxis=dict(title='Contagem')
    )

    return render_template('destaques_regiao_uf.html', plot=fig.to_html())


@app.route('/distribuicao-genero')
def distribuicao_sexo():
    # Consulta ao banco de dados para obter a distribuição dos atendimentos por sexo do consumidor
    cur = conn.cursor()
    cur.execute('SELECT SexoConsumidor, COUNT(*) AS CountAtendimentos FROM Atendimento GROUP BY SexoConsumidor')
    data = cur.fetchall()
    cur.close()

    # Processar os dados
    sexos = []
    contagem = []
    for row in data:
        sexos.append(row[0])
        contagem.append(row[1])

    # Criar o gráfico de pizza
    fig = go.Figure(data=go.Pie(labels=sexos, values=contagem))

    fig.update_layout(
        title='Distribuição dos Atendimentos por Sexo do Consumidor',
    )

    return render_template('distribuicao_genero.html', plot=fig.to_html())


@app.route('/distribuicao-faixa-etaria')
def distribuicao_faixa_etaria():
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

    return render_template('distribuicao_faixa_etaria.html', plot=fig.to_html())


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
