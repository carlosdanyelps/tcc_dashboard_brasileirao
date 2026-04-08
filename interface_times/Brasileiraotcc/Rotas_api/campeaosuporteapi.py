from flask import Flask, request, jsonify
import pandas as pd
import sys
import os
from funcoes.ID import adicionar_ids

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
df['ano'] = df['data'].dt.year

# =========================
# REMOVER JOGOS DUPLICADOS
# (resolve problema de 2014+)
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
# CALCULAR PONTOS (SEM ITERROWS)
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
    df.groupby(['ano', 'mandante', 'mandante_id'])['pontos_mandante']
    .sum()
    .reset_index()
)
pontos_mandantes['url_escudo'] = url_escudo_base + pontos_mandantes['mandante_id'].astype(str)
pontos_mandantes.rename(columns={
    'mandante': 'time',
    'pontos_mandante': 'pontos'
}, inplace=True)

pontos_visitantes = (
    df.groupby(['ano', 'visitante', 'visitante_id'])['pontos_visitante']
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

pontos_totais = pontos_totais.groupby(['ano', 'time', 'url_escudo'])['pontos'].sum().reset_index()

# =========================
# DEFINIR CAMPEÕES
# =========================
campeoes_geral = pontos_totais.loc[
    pontos_totais.groupby('ano')['pontos'].idxmax()
    
].sort_values('ano')

