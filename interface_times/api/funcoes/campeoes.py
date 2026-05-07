import pandas as pd
import sys
import os

# =========================
# PATH
# =========================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from funcoes.ID import adicionar_ids
from escudos.cor import cor, bordaCor

# =========================
# CARREGAR DADOS
# =========================
caminho_csv = os.path.join(os.path.dirname(__file__), 'campeonato-brasileiro-full.csv')
df = pd.read_csv(caminho_csv)


df = adicionar_ids(df)
df['rodata'] = pd.to_numeric(df['rodata'], errors='coerce')

# =========================
# TRATAR DATAS
# =========================
df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d', errors='coerce')
df['ano_civil'] = df['data'].dt.year

# =========================
# ESCUDOS
# =========================
url_escudo_base = 'http://localhost:5000/escudo/'
df['escudo_m'] = url_escudo_base + df['mandante_id'].astype(str)
df['escudo_v'] = url_escudo_base + df['visitante_id'].astype(str)

# =========================
# TEMPORADA
# =========================
def definir_temporada(row):
    if pd.isna(row['rodata']):
        return row['ano_civil']

    rodata = row['rodata']
    ano = row['ano_civil']

    if ano == 2021 and rodata >= 28:
        return 2020

    if ano == 2020 and 1 <= rodata <= 27:
        return 2020

    return ano

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
# VITÓRIAS / EMPATES / DERROTAS
# =========================
df['vitorias_m'] = (df['mandante_Placar'] > df['visitante_Placar']).astype(int)
df['empates_m']  = (df['mandante_Placar'] == df['visitante_Placar']).astype(int)
df['derrotas_m'] = (df['mandante_Placar'] < df['visitante_Placar']).astype(int)

df['vitorias_v'] = (df['visitante_Placar'] > df['mandante_Placar']).astype(int)
df['empates_v']  = (df['visitante_Placar'] == df['mandante_Placar']).astype(int)
df['derrotas_v'] = (df['visitante_Placar'] < df['mandante_Placar']).astype(int)

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
# MANDANTES
# =========================
mandantes = df[[
    'temporada', 'mandante', 'mandante_id',
    'pontos_m', 'vitorias_m', 'empates_m', 'derrotas_m',
    'mandante_Placar', 'visitante_Placar',
    'escudo_m', 'rodata'
]].copy()

mandantes.columns = [
    'temporada', 'time', 'id',
    'pontos', 'vitorias', 'empates', 'derrotas',
    'gols_pro', 'gols_tomados',
    'escudo', 'rodada'
]

# =========================
# VISITANTES
# =========================
visitantes = df[[
    'temporada', 'visitante', 'visitante_id',
    'pontos_v', 'vitorias_v', 'empates_v', 'derrotas_v',
    'visitante_Placar', 'mandante_Placar',
    'escudo_v', 'rodata'
]].copy()

visitantes.columns = [
    'temporada', 'time', 'id',
    'pontos', 'vitorias', 'empates', 'derrotas',
    'gols_pro', 'gols_tomados',
    'escudo', 'rodada'
]

# =========================
# JUNTAR
# =========================
tabela_df = pd.concat([mandantes, visitantes], ignore_index=True)

# =========================
# AGRUPAR
# =========================
tabela_final = tabela_df.groupby(
    ['temporada', 'time', 'id', 'escudo'],
    as_index=False
).agg({
    'pontos': 'sum',
    'gols_pro': 'sum',
    'gols_tomados': 'sum',
    'vitorias': 'sum',
    'empates': 'sum',
    'derrotas': 'sum',
    'rodada': 'max'
})

# =========================
# SALDO + CORES
# =========================
tabela_final['saldo'] = tabela_final['gols_pro'] - tabela_final['gols_tomados']
tabela_final['cor'] = tabela_final['time'].apply(cor)
tabela_final['bordaCor'] = tabela_final['time'].apply(bordaCor)

# =========================
# CLASSIFICAÇÃO
# =========================
def tabela_ano(temporada):
    tabela = tabela_final[tabela_final['temporada'] == temporada].copy()

    if tabela.empty:
        return pd.DataFrame()

    tabela = tabela.sort_values(
        ['pontos', 'saldo', 'gols_pro', 'gols_tomados', 'vitorias', 'empates', 'derrotas'],
        ascending=[False, False, False, True, False, False, True]
    )

    tabela = tabela.head(20)
    tabela['posicao'] = range(1, len(tabela) + 1)

    return tabela

# =========================
# CAMPEÃO
# =========================
def obter_campeao(temporada):
    tabela = tabela_ano(temporada)

    if tabela.empty:
        return None

    campeao = tabela.iloc[0]

    return {
        'temporada': int(campeao['temporada']),
        'time': campeao['time'],
        'id': int(campeao['id']),
        'vitorias': int(campeao['vitorias']),
        'empates': int(campeao['empates']),
        'derrotas': int(campeao['derrotas']),
        'pontos': int(campeao['pontos']),
        'gols_pro': int(campeao['gols_pro']),
        'gols_tomados': int(campeao['gols_tomados']),
        'saldo': int(campeao['saldo']),
        'rodada_maxima': int(campeao['rodada']) if pd.notna(campeao['rodada']) else None,
        'escudo': campeao['escudo'],
        'cor': campeao['cor'],
        'bordaCor': campeao['bordaCor']
    }

# =========================
# TODOS CAMPEÕES
# =========================
def obter_todos_campeoes():
    temporadas = sorted(tabela_final['temporada'].unique())
    return [c for t in temporadas if (c := obter_campeao(t))]

# =========================
# TABELA POR TIME
# =========================
def tabela_time_ano(time, temporada):
    tabela = tabela_final[
        (tabela_final['temporada'] == temporada) &
        (tabela_final['time'].str.lower() == time.lower())
    ].copy()

    if tabela.empty:
        return pd.DataFrame()

    tabela_temp = tabela_final[tabela_final['temporada'] == temporada].copy()

    tabela_temp = tabela_temp.sort_values(
        ['pontos', 'saldo', 'gols_pro'],
        ascending=[False, False, False]
    )

    tabela_temp['posicao'] = range(1, len(tabela_temp) + 1)

    posicao = tabela_temp[
        tabela_temp['time'].str.lower() == time.lower()
    ]['posicao']

    tabela['posicao'] = int(posicao.values[0]) if not posicao.empty else None

    return tabela