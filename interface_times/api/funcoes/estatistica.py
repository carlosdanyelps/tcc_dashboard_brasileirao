import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

df = pd.read_csv('campeonato-brasileiro-full.csv')
df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')
df['ano'] = df['data'].dt.year
matches = df.drop_duplicates(subset='ID', keep='first').copy()
#====================MÉDIAS===========================
def mid_gol(time):
    gols_mandante = matches[matches['mandante'] == time]['mandante_Placar'].sum()
    gols_visitante = matches[matches['visitante'] == time]['visitante_Placar'].sum()
    total_gols = gols_mandante + gols_visitante
    mid_gol = total_gols / len(matches[(matches['mandante'] == time) | (matches['visitante'] == time)]) if len(matches[(matches['mandante'] == time) | (matches['visitante'] == time)]) > 0 else 0
    return mid_gol

def mid_vitoria(time):
    vitorias_mandante = matches[(matches['mandante'] == time) & (matches['mandante_Placar'] > matches['visitante_Placar'])].shape[0]
    vitorias_visitante = matches[(matches['visitante'] == time) & (matches['visitante_Placar'] > matches['mandante_Placar'])].shape[0]
    total_vitorias = vitorias_mandante + vitorias_visitante
    jogos = len(matches[(matches['mandante'] == time) | (matches['visitante'] == time)])
    mid_vitoria = total_vitorias / jogos if jogos > 0 else 0
    return mid_vitoria

def mid_derrota(time):
    derrotas_mandante = matches[(matches['mandante'] == time) & (matches['mandante_Placar'] < matches['visitante_Placar'])].shape[0]
    derrotas_visitante = matches[(matches['visitante'] == time) & (matches['visitante_Placar'] < matches['mandante_Placar'])].shape[0]
    total_derrotas = derrotas_mandante + derrotas_visitante
    jogos = len(matches[(matches['mandante'] == time) | (matches['visitante'] == time)])
    mid_derrota = total_derrotas / jogos if jogos > 0 else 0
    return mid_derrota

def mid_empate(time):
    empates_mandante = matches[(matches['mandante'] == time) & (matches['mandante_Placar'] == matches['visitante_Placar'])].shape[0]
    empates_visitante = matches[(matches['visitante'] == time) & (matches['visitante_Placar'] == matches['mandante_Placar'])].shape[0]
    total_empates = empates_mandante + empates_visitante
    jogos = len(matches[(matches['mandante'] == time) | (matches['visitante'] == time)])
    mid_empate = total_empates / jogos if jogos > 0 else 0
    return mid_empate
#===========================================================
#====================PONTUAÇÃO FINAL========================
#===========================================================


def pontuacao_final(time):
    vitorias_mandante = matches[(matches['mandante'] == time) & (matches['mandante_Placar'] > matches['visitante_Placar'])].shape[0]
    vitorias_visitante = matches[(matches['visitante'] == time) & (matches['visitante_Placar'] > matches['mandante_Placar'])].shape[0]
    empates_mandante = matches[(matches['mandante'] == time) & (matches['mandante_Placar'] == matches['visitante_Placar'])].shape[0]
    empates_visitante = matches[(matches['visitante'] == time) & (matches['visitante_Placar'] == matches['mandante_Placar'])].shape[0]
    total_vitorias = vitorias_mandante + vitorias_visitante
    total_empates = empates_mandante + empates_visitante
    pontos = total_vitorias * 3 + total_empates
    return pontos



def pontuacao_final_por_temporada(time):
    pontos_por_ano = {}

    for ano, grupo in matches.groupby('ano'):
        if pd.isna(ano):
            continue

        vitorias_mandante = grupo[(grupo['mandante'] == time) & (grupo['mandante_Placar'] > grupo['visitante_Placar'])].shape[0]
        vitorias_visitante = grupo[(grupo['visitante'] == time) & (grupo['visitante_Placar'] > grupo['mandante_Placar'])].shape[0]
        empates_mandante = grupo[(grupo['mandante'] == time) & (grupo['mandante_Placar'] == grupo['visitante_Placar'])].shape[0]
        empates_visitante = grupo[(grupo['visitante'] == time) & (grupo['visitante_Placar'] == grupo['mandante_Placar'])].shape[0]

        pontos = (vitorias_mandante + vitorias_visitante) * 3 + empates_mandante + empates_visitante
        pontos_por_ano[int(ano)] = pontos
    return pontos_por_ano

def comparar_times(time1, time2):
    pontos_time1 = pontuacao_final(time1)
    pontos_time2 = pontuacao_final(time2)
    return pontos_time1, pontos_time2  