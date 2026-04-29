from flask import Flask, request, jsonify
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes.ID import adicionar_ids
from escudos.cor import cor, bordaCor

# =========================
# CARREGAR DADOS
# =========================
df = pd.read_csv('campeonato-brasileiro-full.csv')
df = adicionar_ids(df)

url_escudo_base = 'http://localhost:5000/escudo/'

# =========================
# TRATAR DATAS
# =========================
df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')
df['ano_civil'] = df['data'].dt.year

# =========================
# DEFINIR TEMPORADA BASEADA EM RODATA
# =========================
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
# REMOVER JOGOS DUPLICADOS
# =========================
df['id_jogo'] = df['partida_id'].fillna(
    df['data'].astype(str) + df['mandante'] + df['visitante']
)

df = df.drop_duplicates(subset='id_jogo')

# =========================
# CONVERTER PLACARES
# =========================
df['mandante_Placar'] = pd.to_numeric(df['mandante_Placar'], errors='coerce')
df['visitante_Placar'] = pd.to_numeric(df['visitante_Placar'], errors='coerce')

# =========================
# CALCULAR PONTOS
# =========================
df['pontos_mandante'] = (
    (df['mandante_Placar'] > df['visitante_Placar']) * 3 +
    (df['mandante_Placar'] == df['visitante_Placar']) * 1
)

df['pontos_visitante'] = (
    (df['visitante_Placar'] > df['mandante_Placar']) * 3 +
    (df['mandante_Placar'] == df['visitante_Placar']) * 1
)

# =========================
# AGRUPAR PONTOS
# =========================
pontos_mandantes = (
    df.groupby(['temporada', 'mandante', 'mandante_id'])['pontos_mandante']
    .sum()
    .reset_index()
)
pontos_mandantes['url_escudo'] = url_escudo_base + pontos_mandantes['mandante_id'].astype(str)
pontos_mandantes.rename(columns={
    'mandante': 'time',
    'pontos_mandante': 'pontos'
}, inplace=True)

pontos_visitantes = (
    df.groupby(['temporada', 'visitante', 'visitante_id'])['pontos_visitante']
    .sum()
    .reset_index()
)
pontos_visitantes['url_escudo'] = url_escudo_base + pontos_visitantes['visitante_id'].astype(str)
pontos_visitantes.rename(columns={
    'visitante': 'time',
    'pontos_visitante': 'pontos'
}, inplace=True)

# =========================
# SOMAR TOTAL POR TIME
# =========================
pontos_totais = pd.concat([pontos_mandantes, pontos_visitantes])
pontos_totais = pontos_totais.groupby(['temporada', 'time', 'url_escudo'])['pontos'].sum().reset_index()
# Adiciona coluna de cor ao DataFrame pontos_totais

pontos_totais['cor'] = pontos_totais['time'].apply(cor)
pontos_totais['bordaCor'] = pontos_totais['time'].apply(bordaCor)

# =========================
# DEFINIR CAMPEÕES
# =========================
campeoes_geral = pontos_totais.loc[
    pontos_totais.groupby('temporada')['pontos'].idxmax()
].sort_values('temporada')
 # Adiciona coluna de cor e borderColor ao DataFrame campeoes_geral
campeoes_geral['cor'] = campeoes_geral['time'].apply(cor)
campeoes_geral['bordaCor'] = campeoes_geral['time'].apply(bordaCor)


# =========================
# FUNÇÕES DA API
# =========================

def get_campeao_temporada(temporada):
    """
    Retorna o campeão de uma temporada específica
    """
    campeao = pontos_totais.loc[
        (pontos_totais['temporada'] == temporada),
        ['time', 'url_escudo', 'pontos', 'cor', 'bordaCor']
    ].nlargest(1, 'pontos')
    
    if campeao.empty:
        return None
    
    resultado = campeao.iloc[0]
    return {
        'temporada': int(temporada),
        'time': resultado['time'],
        'cor': resultado['cor'],
        'bordaCor': resultado['bordaCor'],
        'pontos': int(resultado['pontos']),
        'gols_pro': int(resultado['gols_pro']) if 'gols_pro' in resultado else None,
        'gols_tomados': int(resultado['gols_tomados']) if 'gols_tomados' in resultado else None,
        'saldo': int(resultado['saldo']) if 'saldo' in resultado else None,
        'escudo': resultado['url_escudo']
    }


def get_todos_campeoes():
    """
    Retorna lista de campeões de todas as temporadas
    """
    campeoes_list = []
    temporadas = sorted(pontos_totais['temporada'].unique())
    
    for temporada in temporadas:
        campeao = get_campeao_temporada(temporada)
        if campeao:
            campeoes_list.append(campeao)
    
    return campeoes_list


def get_tabela_temporada(temporada):
    """
    Retorna a tabela completa de uma temporada
    """
    tabela = pontos_totais[pontos_totais['temporada'] == temporada].sort_values(
        'pontos', ascending=False
    )
    
    return tabela.to_dict('records')
