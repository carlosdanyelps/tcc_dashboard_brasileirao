from flask import Flask, request, jsonify
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from funcoes.ID import adicionar_ids
from escudos.cor import cor, bordaCor

app = Flask(__name__)

# =========================
# CARREGAR DADOS
# =========================
df = pd.read_csv('campeonato-brasileiro-full.csv')
df = adicionar_ids(df)

url_escudo_base = 'http://localhost:5000/escudo/'

# =========================
# TRATAR DATAS
# =========================
df['data'] = pd.to_datetime(df['data'], errors='coerce')
df['ano_civil'] = df['data'].dt.year

# =========================
# DEFINIR TEMPORADA
# =========================

df['temporada'] = df.apply(
    lambda x: 2020
    if x['ano_civil'] in [2020, 2021]
       and x['rodata_corrigida'] <= 38
       and x['temporada_corrigida'] == 2020
    else x['ano_civil'],
    axis=1
)
# =========================
# TRATAR DATAS
# =========================
df['data'] = pd.to_datetime(df['data'], errors='coerce')

# =========================
# USAR TEMPORADA JÁ CORRIGIDA
# =========================
df['temporada_corrigida'] = pd.to_numeric(
    df['temporada_corrigida'],
    errors='coerce'
).astype('Int64')

# =========================
# PLACARES
# =========================
df['mandante_Placar'] = pd.to_numeric(
    df['mandante_Placar'],
    errors='coerce'
)

df['visitante_Placar'] = pd.to_numeric(
    df['visitante_Placar'],
    errors='coerce'
)

# =========================
# CRIAR BASE COM APENAS UMA LINHA POR PARTIDA
# =========================
partidas = (
    df.sort_values('data')
      .drop_duplicates(subset='partida_id')
      .copy()
)

# =========================
# PONTOS
# =========================
partidas['pontos_m'] = 0
partidas['pontos_v'] = 0

partidas.loc[
    partidas['mandante_Placar'] > partidas['visitante_Placar'],
    'pontos_m'
] = 3

partidas.loc[
    partidas['visitante_Placar'] > partidas['mandante_Placar'],
    'pontos_v'
] = 3

partidas.loc[
    partidas['mandante_Placar'] == partidas['visitante_Placar'],
    ['pontos_m', 'pontos_v']
] = 1

# =========================
# GOLS
# =========================
gols_mandantes = (
    partidas.groupby(
        ['temporada_corrigida', 'mandante', 'mandante_id']
    )
    .agg(
        gols_pro=('mandante_Placar', 'sum'),
        gols_tomados=('visitante_Placar', 'sum')
    )
    .reset_index()
    .rename(columns={'mandante': 'time'})
)

gols_visitantes = (
    partidas.groupby(
        ['temporada_corrigida', 'visitante', 'visitante_id']
    )
    .agg(
        gols_pro=('visitante_Placar', 'sum'),
        gols_tomados=('mandante_Placar', 'sum')
    )
    .reset_index()
    .rename(columns={'visitante': 'time'})
)

gols_totais = pd.concat(
    [gols_mandantes, gols_visitantes],
    ignore_index=True
)

gols_totais = (
    gols_totais.groupby(
        ['temporada_corrigida', 'time']
    )[['gols_pro', 'gols_tomados']]
    .sum()
    .reset_index()
)

# =========================
# PONTOS
# =========================
pontos_mandantes = (
    partidas.groupby(
        ['temporada_corrigida', 'mandante', 'mandante_id']
    )['pontos_m']
    .sum()
    .reset_index()
    .rename(columns={
        'mandante': 'time',
        'pontos_m': 'pontos'
    })
)

pontos_mandantes['url_escudo'] = (
    url_escudo_base +
    pontos_mandantes['mandante_id'].astype(str)
)

pontos_visitantes = (
    partidas.groupby(
        ['temporada_corrigida', 'visitante', 'visitante_id']
    )['pontos_v']
    .sum()
    .reset_index()
    .rename(columns={
        'visitante': 'time',
        'pontos_v': 'pontos'
    })
)

pontos_visitantes['url_escudo'] = (
    url_escudo_base +
    pontos_visitantes['visitante_id'].astype(str)
)

pontos_totais = pd.concat(
    [pontos_mandantes, pontos_visitantes],
    ignore_index=True
)

pontos_totais = (
    pontos_totais.groupby(
        ['temporada_corrigida', 'time', 'url_escudo']
    )['pontos']
    .sum()
    .reset_index()
)

# =========================
# JUNTAR DADOS
# =========================
pontos_totais = pontos_totais.merge(
    gols_totais,
    on=['temporada_corrigida', 'time'],
    how='left'
)

pontos_totais['saldo'] = (
    pontos_totais['gols_pro']
    - pontos_totais['gols_tomados']
)

# =========================
# CORES
# =========================
pontos_totais['cor'] = pontos_totais['time'].apply(cor)
pontos_totais['bordaCor'] = pontos_totais['time'].apply(bordaCor)

# =========================
# CAMPEÕES
# =========================
campeoes_geral = (
    pontos_totais
    .sort_values(
        ['temporada_corrigida', 'pontos', 'saldo', 'gols_pro'],
        ascending=[True, False, False, False]
    )
    .groupby('temporada_corrigida')
    .first()
    .reset_index()
)

# =========================
# FUNÇÃO DE ORDENAÇÃO JSON
# =========================
def ordenar_campeao(c):
    return {
        'temporada': int(c['temporada_corrigida']),
        'time': c['time'],
        'pontos': int(c['pontos']),
        'gols_pro': int(c['gols_pro']),
        'gols_tomados': int(c['gols_tomados']),
        'saldo': int(c['saldo']),
        'escudo': c['url_escudo'],
        'cor': c['cor'],
        'bordaCor': c['bordaCor']
    }

# =========================
# ROTAS
# =========================


@app.route('/tabela')
def tabela():
    ano = request.args.get('ano', type=int)

    if not ano:
        campeoes = campeoes_geral.to_dict('records')
        campeoes_ordenados = [ordenar_campeao(c) for c in campeoes]

        return jsonify({
            'campeoes': campeoes_ordenados
        })

    tabela = pontos_totais[pontos_totais['temporada_corrigida'] == ano].copy()

    tabela = tabela.sort_values(
        ['pontos', 'saldo', 'gols_pro'],
        ascending=[False, False, False]
    )

    tabela['posicao'] = range(1, len(tabela) + 1)

    return jsonify(tabela.to_dict('records'))

@app.route('/campeao')
def campeao():
    ano = request.args.get('ano', type=int)

    if not ano:
        return jsonify({'erro': 'Informe o ano'}), 400

    campeao = (
        pontos_totais[
            pontos_totais['temporada_corrigida'] == ano
        ]
        .sort_values(
            ['pontos', 'saldo', 'gols_pro'],
            ascending=False
        )
        .head(1)
    )
    if campeao.empty:
        return jsonify({'erro': 'Ano não encontrado'}), 404

    c = campeao.iloc[0]

    return jsonify(ordenar_campeao(c))


# =========================
# RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)

 
