from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rotas_api.campeaosuporteapi import campeoes_geral, ordenar_campeao

from funcoes.campeoes import tabela_ano, tabela_time_ano
from rotas_api.timemain import resumo_time
from escudos.API_escudos import escudo
from funcoes.estatistica import pontuacao_final_por_temporada, mid_derrota, mid_gol, mid_vitoria, mid_empate
from escudos.cor import cor, bordaCor
from tmp import classificacao_por_rodada


df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'campeonato-brasileiro-full.csv'))


app = Flask(__name__)
CORS(app)


#################### Tabela de classificação por ano #####################

@app.route('/tabela', methods=['GET'])
def get_tabela():
    ano = request.args.get('ano', type=int)
    time = request.args.get('time')

    # =========================
    # para retornar a tavela geral sem especificação
    # =========================
    if not ano and not time:
        campeoes = campeoes_geral.to_dict(orient='records')
        campeoes_ordenados = [ordenar_campeao(c) for c in campeoes]

        return jsonify({
            'Campeoes todas temporadas': campeoes_ordenados
        })


    if ano and time:
        tabela = tabela_time_ano(time, ano)

        if tabela.empty:
            return jsonify({'erro': 'Time ou ano não encontrado'}), 404

        return jsonify(tabela.to_dict(orient='records'))
    if ano:
        tabela = tabela_ano(ano)

        if tabela.empty:
            return jsonify({'erro': 'Ano não encontrado'}), 404

        return jsonify(tabela.to_dict(orient='records'))

    return jsonify({
        'erro': 'Parâmetros inválidos. Use /tabela?ano=2003 ou /tabela?time=Flamengo&ano=2003'
    }), 400

#################################################################
############### tabela de classificação por rodada ##############
#################################################################

@app.route('/tabela/rodada', methods=['GET'])
def get_tabela_rodada():
    ano = request.args.get('ano', type=int)

    if not ano:
        return jsonify({'erro': 'Informe o ano'}), 400

    tabela = classificacao_por_rodada(df, ano)

    if tabela is None:
        return jsonify({'erro': f'Ano {ano} não encontrado'}), 404

    return jsonify(tabela.to_dict(orient='records'))

###############################################################
############# TIME ESPECÍFICO - RESUMO COMPLETO #############
###############################################################
@app.route('/timemain')
def timemain():
    return resumo_time()

################################################################
############# ESCUDO #############
###############################################################
@app.route('/escudo/<int:id>')
def get_escudo(id):
    return escudo(id)

@app.route('/pontuacao_temporada')
def get_pontuacao_por_temporada():
    time = request.args.get('time')
    ano = request.args.get('ano')

    if not time:
        return jsonify({'erro': 'Time não especificado'}), 400

    pontos = pontuacao_final_por_temporada(time)
    if ano:
        try:
            ano = int(ano)
        except ValueError:
            return jsonify({'erro': 'Ano inválido'}), 400

        if ano not in pontos:
            return jsonify({'erro': f'Pontuação não encontrada para o ano {ano}'}), 404
        return jsonify({'time': time, 'ano': ano, 'pontos': pontos[ano]})

    return jsonify({'time': time, 'pontos_por_temporada': pontos})

@app.route('/estatisticas')
def get_estatisticas():
    time = request.args.get('time')

    if not time:
        return jsonify({'erro': 'Time não especificado'}), 400

    estatisticas = {
        'time': time,
        'cor': cor(time),
        'borderColor': bordaCor(time),
        'média_gols': mid_gol(time),
        'média_vitórias': mid_vitoria(time),
        'média_derrotas': mid_derrota(time),
        'média_empates': mid_empate(time)

    }
    return jsonify(estatisticas)

####################################comparação geral dos times#####################################


if __name__ == '__main__':
    app.run(debug=True)