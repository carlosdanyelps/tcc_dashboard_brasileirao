import pandas as pd
import sys
import os

# Garantir path correto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from funcoes.ID import adicionar_ids
from escudos.cor import cor, bordaCor


# =========================
# CARREGAR DADOS
# =========================
caminho_csv = os.path.join(os.path.dirname(__file__), 'campeonato-brasileiro-full.csv')
df = pd.read_csv(caminho_csv)

df = adicionar_ids(df)

# =========================
# TRATAR DATAS
# =========================
df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d', errors='coerce')
df['ano_civil'] = df['data'].dt.year

# URL base para escudo
url_escudo_base = 'http://localhost:5000/escudo/'

df['escudo_m'] = url_escudo_base + df['mandante_id'].astype(str)
df['escudo_v'] = url_escudo_base + df['visitante_id'].astype(str)

# =========================
# DEFINIR TEMPORADA
# =========================
def definir_temporada(row):
    if pd.isna(row['rodata']):
        return row['ano_civil']

    rodata = row['rodata']
    ano_civil = row['ano_civil']

    if ano_civil == 2021 and rodata >= 28.0:
        return 2020

    if ano_civil == 2020 and 1.0 <= rodata <= 27.0:
        return 2020

    return ano_civil

df['temporada'] = df.apply(definir_temporada, axis=1)

# =========================
# REMOVER DUPLICATAS
# =========================
df['id_jogo'] = df['partida_id'].fillna(
    df['data'].astype(str) + df['mandante'] + df['visitante']
)

df = df.drop_duplicates(subset='id_jogo')

# =========================
# TRATAR PLACARES
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
# MANDANTES
# =========================
mandantes = df[['temporada', 'mandante', 'mandante_id', 'pontos_m', 'mandante_Placar', 'visitante_Placar', 'escudo_m', 'rodata']].copy()
mandantes.columns = ['temporada', 'time', 'id', 'pontos', 'gols_pro', 'gols_tomados', 'escudo', 'rodada']

# =========================
# VISITANTES
# =========================
visitantes = df[['temporada', 'visitante', 'visitante_id', 'pontos_v', 'visitante_Placar', 'mandante_Placar', 'escudo_v', 'rodata']].copy()
visitantes.columns = ['temporada', 'time', 'id', 'pontos', 'gols_pro', 'gols_tomados', 'escudo', 'rodada']

# =========================
# JUNTAR
# =========================
tabela_df = pd.concat([mandantes, visitantes])

# =========================
# AGRUPAR
# =========================
tabela_final = tabela_df.groupby(['temporada', 'time', 'id', 'escudo'], as_index=False).agg({
    'pontos': 'sum',
    'gols_pro': 'sum',
    'gols_tomados': 'sum',
    'rodada': 'max'
})

# =========================
# SALDO
# =========================
tabela_final['saldo'] = tabela_final['gols_pro'] - tabela_final['gols_tomados']
tabela_final['cor'] = tabela_final['time'].apply(cor)
tabela_final['bordaCor'] = tabela_final['time'].apply(bordaCor)

# =========================
# FUNÇÃO PRINCIPAL (CORRIGIDA)
# =========================
def tabela_ano(temporada):
    tabela = tabela_final[tabela_final['temporada'] == temporada].copy()

    if tabela.empty:
        return pd.DataFrame()

    tabela = tabela.sort_values(
        ['pontos', 'saldo', 'gols_pro'],
        ascending=[False, False, False]
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
        'pontos': int(campeao['pontos']),
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
    campeoes = []

    for temporada in temporadas:
        campeao = obter_campeao(temporada)
        if campeao:
            campeoes.append(campeao)

    return campeoes