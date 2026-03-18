from flask import Flask, request, jsonify
import pandas as pd
from API import *
df = pd.read_csv('campeonato-brasileiro-full.csv')

#filtradno a coluna data do csv no formato certo
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
app = Flask(__name__)
##pedido do heber
@app.route('/anorodada/partidarodada', methods=['GET'])
def partidarodada():
    ano = ano.request.args.get('ano')
    df_ano = df[df['data'].dt.year == ano]
    if not ano:
        return jsonify({'error': 'ano não fornecido'}), 400
    time = time.args.request.get('time')
    if not time:
        return jsonify({'error':'Time não fornecido'}), 400
    for i in df_ano['rodata'].unique():
        if i == df[df['mandante'] == time, 'mandante_placar'> 'visitante_placar']:
            situ = 'vitória'
        elif i == df[df['mandante']==time, 'mandante_placar'<'visitante_placar']:
            situ = 'derrota'
        elif i  == df[df['visitante']==time, 'visitante_placar'>'mandante_placar']:
            situ = 'vitória'
        elif i == df[df['visitante']==time, 'visitante_placar'<'mandante_placar']:
            situ = 'derrota'
        else:
            situ = 'empate'
        return jsonify({
         'ano': ano,
         'time': time,
         'rodada': i,
         'situação': situ
        })