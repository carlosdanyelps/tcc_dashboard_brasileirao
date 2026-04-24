from flask import Flask, jsonify, request
import sys
import os
# Permitir importar da pasta funcoes
# <<<<<<< HEAD:interface_times/api/rotas_api/apis.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rotas_api.campeaosuporteapi import campeoes_geral
from funcoes.campeoes import tabela_ano
from rotas_api.timemain import resumo_time

from escudos.API_escudos import escudo
from funcoes.estatistica import pontuacao_final_por_temporada, mid_derrota, mid_gol, mid_vitoria, mid_empate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


#################### Tabela de classificação por ano #####################
@app.route('/tabela', methods=['GET'])
def get_tabela():
    ano = request.args.get('ano')

    if not ano:
        return jsonify({
    'Campeoes todas temporadas': campeoes_geral.to_dict(orient='records')
})
    try:
        ano = int(ano)
    except:
        return jsonify({'erro': 'Ano inválido'}), 400

    tabela = tabela_ano(ano)

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
        'média_gols': mid_gol(time),
        'média_vitórias': mid_vitoria(time),
        'média_derrotas': mid_derrota(time),
        'média_empates': mid_empate(time)
    }
    return jsonify(estatisticas)

if __name__ == '__main__':
    app.run(debug=True)