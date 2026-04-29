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
def definir_temporada(row):
    if pd.isna(row['rodata']):
        return row['ano_civil']

    if row['ano_civil'] == 2021 and row['rodata'] >= 28:
        return 2020

    if row['ano_civil'] == 2020 and row['rodata'] <= 27:
        return 2020

    return row['ano_civil']

df['temporada'] = df.apply(definir_temporada, axis=1)

# =========================
# REMOVER DUPLICATAS
# =========================
df['id_jogo'] = df['partida_id'].fillna(
    df['data'].astype(str) + df['mandante'] + df['visitante']
)
df = df.drop_duplicates(subset='id_jogo')

# =========================
# PLACARES
# =========================
df['mandante_Placar'] = pd.to_numeric(df['mandante_Placar'], errors='coerce')
df['visitante_Placar'] = pd.to_numeric(df['visitante_Placar'], errors='coerce')

# =========================
# PONTOS
# =========================
df['pontos_m'] = (
    (df['mandante_Placar'] > df['visitante_Placar']) * 3 +
    (df['mandante_Placar'] == df['visitante_Placar']) * 1
)

df['pontos_v'] = (
    (df['visitante_Placar'] > df['mandante_Placar']) * 3 +
    (df['visitante_Placar'] == df['mandante_Placar']) * 1
)

# =========================
# GOLS
# =========================
gols_mandantes = df.groupby(
    ['temporada', 'mandante', 'mandante_id']
).agg({
    'mandante_Placar': 'sum',
    'visitante_Placar': 'sum'
}).reset_index()

gols_mandantes.rename(columns={
    'mandante': 'time',
    'mandante_Placar': 'gols_pro',
    'visitante_Placar': 'gols_tomados'
}, inplace=True)

gols_visitantes = df.groupby(
    ['temporada', 'visitante', 'visitante_id']
).agg({
    'visitante_Placar': 'sum',
    'mandante_Placar': 'sum'
}).reset_index()

gols_visitantes.rename(columns={
    'visitante': 'time',
    'visitante_Placar': 'gols_pro',
    'mandante_Placar': 'gols_tomados'
}, inplace=True)

gols_totais = pd.concat([gols_mandantes, gols_visitantes])
gols_totais = gols_totais.groupby(
    ['temporada', 'time']
)[['gols_pro', 'gols_tomados']].sum().reset_index()

# =========================
# PONTOS
# =========================
pontos_mandantes = df.groupby(
    ['temporada', 'mandante', 'mandante_id']
)['pontos_m'].sum().reset_index()

pontos_mandantes['url_escudo'] = url_escudo_base + pontos_mandantes['mandante_id'].astype(str)
pontos_mandantes.rename(columns={'mandante': 'time', 'pontos_m': 'pontos'}, inplace=True)

pontos_visitantes = df.groupby(
    ['temporada', 'visitante', 'visitante_id']
)['pontos_v'].sum().reset_index()

pontos_visitantes['url_escudo'] = url_escudo_base + pontos_visitantes['visitante_id'].astype(str)
pontos_visitantes.rename(columns={'visitante': 'time', 'pontos_v': 'pontos'}, inplace=True)

pontos_totais = pd.concat([pontos_mandantes, pontos_visitantes])
pontos_totais = pontos_totais.groupby(
    ['temporada', 'time', 'url_escudo']
)['pontos'].sum().reset_index()

# =========================
# JUNTAR + SALDO
# =========================
pontos_totais = pontos_totais.merge(gols_totais, on=['temporada', 'time'], how='left')
pontos_totais['saldo'] = pontos_totais['gols_pro'] - pontos_totais['gols_tomados']

# =========================
# CORES
# =========================
pontos_totais['cor'] = pontos_totais['time'].apply(cor)
pontos_totais['bordaCor'] = pontos_totais['time'].apply(bordaCor)

# =========================
# CAMPEÕES
# =========================
campeoes_geral = pontos_totais.loc[
    pontos_totais.groupby('temporada')['pontos'].idxmax()
].sort_values('temporada')

# =========================
# FUNÇÃO DE ORDENAÇÃO JSON
# =========================
def ordenar_campeao(c):
    return {
        'temporada': int(c['temporada']),
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

    tabela = pontos_totais[pontos_totais['temporada'] == ano].copy()

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

    campeao = pontos_totais[pontos_totais['temporada'] == ano] \
        .sort_values('pontos', ascending=False).head(1)

    if campeao.empty:
        return jsonify({'erro': 'Ano não encontrado'}), 404

    c = campeao.iloc[0]

    return jsonify(ordenar_campeao(c))


# =========================
# RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)