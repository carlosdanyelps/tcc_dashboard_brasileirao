from flask import Flask, jsonify, request
import pandas as pd
import sys  
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from funcoes.estatistica import pontuacao_final_por_temporada, mid_derrota, mid_gol, mid_vitoria, mid_empate

df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'campeonato-brasileiro-full.csv'))
df['data'] = pd.to_datetime(df['data'], errors='coerce')

time1 = request.args.get('time1')
time2 = request.args.get('time2')
df = df[(df['mandante'] == time1) | (df['visitante'] == time1) | (df['mandante'] == time2) | (df['visitante'] == time2)]
df['mandante'] = time1 | time2
df['visitante'] = time1 | time2
def comparar_times():
    if not time1 or not time2:
        return jsonify({'erro': 'Ambos os times devem ser especificados'}), 400

    estatisticas = {
        'pontos_time1': pontuacao_final_por_temporada(time1),
        'pontos_time2': pontuacao_final_por_temporada(time2),
        'média_vitórias_time1': mid_vitoria(time1),
        'média_vitórias_time2': mid_vitoria(time2),
        'média_derrotas_time1': mid_derrota(time1),
        'média_derrotas_time2': mid_derrota(time2),
        'média_gols_time1': mid_gol(time1),
        'média_gols_time2': mid_gol(time2),
        'média_empates_time1': mid_empate(time1),
        'média_empates_time2': mid_empate(time2)
    }
    return jsonify(estatisticas)