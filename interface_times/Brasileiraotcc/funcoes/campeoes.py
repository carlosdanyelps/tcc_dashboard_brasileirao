import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from funcoes.ID import adicionar_ids

# =========================
# CARREGAR DADOS
# =========================
df = pd.read_csv('campeonato-brasileiro-full.csv')
df = adicionar_ids(df)

# =========================
# TRATAR DATAS
# =========================
df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')
df['ano_civil'] = df['data'].dt.year

# URL base para escudo de cada time
url_escudo_base = 'http://localhost:5000/escudo/'

df['escudo_m'] = url_escudo_base + df['mandante_id'].astype(str)
df['escudo_v'] = url_escudo_base + df['visitante_id'].astype(str)

# =========================
# DEFINIR TEMPORADA BASEADA EM RODATA
# =========================
# A coluna 'rodata' define a rodada dentro da temporada
# Temporadas normais: 1-38 rodadas em um ano
# Temporada 2020/2021: rodadas 1-27 em 2020, rodadas 28-38 em 2021

def definir_temporada(row):
    """
    Define a temporada baseada em rodata e ano civil
    """
    if pd.isna(row['rodata']):
        # Se não tem rodada, usar ano civil como fallback
        return row['ano_civil']
    
    rodata = row['rodata']
    ano_civil = row['ano_civil']
    
    # Para 2021 com rodata >= 28, pertence à temporada 2020/2021
    if ano_civil == 2021 and rodata >= 28.0:
        return 2020  # A temporada é "2020/2021", representada como 2020
    
    # Para 2020 com rodata 1-27, também pertence a 2020/2021
    if ano_civil == 2020 and 1.0 <= rodata <= 27.0:
        return 2020
    
    # Todos os outros casos, usar ano civil
    return ano_civil

df['temporada'] = df.apply(definir_temporada, axis=1)

# =========================
# REMOVER DUPLICATAS (ESSENCIAL)
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
    'rodada': 'max'  # Pega a última rodada que o time jogou
})

# =========================
# SALDO
# =========================
tabela_final['saldo'] = tabela_final['gols_pro'] - tabela_final['gols_tomados']

# =========================
# FUNÇÃO FINAL
# =========================


def tabela_temporada(temporada):
    """
    Retorna a tabela final de uma temporada específica
    Para 2020/2021, usar temporada=2020
    """
    tabela = tabela_final[tabela_final['temporada'] == temporada].copy()
    
    tabela = tabela.sort_values(
        ['pontos', 'saldo', 'gols_pro'],
        ascending=[False, False, False]
    )
    
    tabela = tabela.head(20)
    
    tabela['posicao'] = range(1, len(tabela) + 1)

    print(tabela)
    return tabela


# =========================
# FUNÇÕES DE CAMPEONATO
# =========================

def obter_campeao(temporada):
    """
    Retorna o campeão de uma temporada específica
    """
    tabela = tabela_final[tabela_final['temporada'] == temporada].copy()
    
    if tabela.empty:
        return None
    
    tabela = tabela.sort_values(
        ['pontos', 'saldo', 'gols_pro'],
        ascending=[False, False, False]
    )
    
    campeao = tabela.iloc[0]
    return {
        'temporada': int(campeao['temporada']),
        'time': campeao['time'],
        'id': int(campeao['id']),
        'pontos': int(campeao['pontos']),
        'escudo': campeao['escudo'],
        'rodada_maxima': int(campeao['rodada']) if pd.notna(campeao['rodada']) else None
    }


def obter_todos_campeoes():
    """
    Retorna lista de campeões de todas as temporadas
    """
    temporadas = sorted(tabela_final['temporada'].unique())
    campeoes = []
    
    for temporada in temporadas:
        campeao = obter_campeao(temporada)
        if campeao:
            campeoes.append(campeao)
    
    return campeoes


# TESTE
