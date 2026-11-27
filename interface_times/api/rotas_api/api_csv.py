from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes.campeoes import obter_todos_campeoes, tabela_ano, tabela_time_ano
from rotas_api.timemain import resumo_time
from escudos.API_escudos import escudo
from funcoes.estatistica import pontuacao_final_por_temporada, mid_derrota, mid_gol, mid_vitoria, mid_empate
from escudos.cor import cor, bordaCor
from tmp import classificacao_por_rodada
from funcoes.confronto import confrontos
from timemain import comparar_times

from sqlalchemy import text
from db.db import engine
from db.db import SessionLocal
from db.models import CampeonatoBrasileiro


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
        return jsonify({
            'Campeoes todas temporadas': obter_todos_campeoes()
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
#######################(((((((CONFRONTOS DIRETOS)))))))########################

@app.route("/comp",methods=['GET'])
def comp():
    time1 = request.args.get('time1')
    time2 = request.args.get('time2')
    resultado = confrontos(time1, time2)
    return jsonify(resultado)

@app.route("/comp/geral",methods=['GET'])
def comp_geral():
    time1 = request.args.get('time1')
    time2 = request.args.get('time2')
    resultado = comparar_times(time1, time2)
    return jsonify(resultado)



@app.route("/teste-db",methods=['GET'])
def teste_db():
    with engine.connect() as conn:

        resultado = conn.execute(
            text("""
                SELECT COUNT(*) AS total
                FROM campeonato_brasileiro
            """)
        )

        total = resultado.scalar()

    return jsonify({
        "status": "ok",
        "total_registros": total
    })



@app.route("/dados-db", methods=['GET'])
def dados_db():

    db = SessionLocal()

    try:
        registros = db.query(CampeonatoBrasileiro).all()

        dados = []

        for registro in registros:
            dados.append({
                "id": registro.id,
                "rodata": registro.rodata,
                "data": registro.data,
                #"hora": registro.hora,
                "mandante": registro.mandante,
                "visitante": registro.visitante,
                "formacao_mandante": registro.formacao_mandante,
                "formacao_visitante": registro.formacao_visitante,
                "tecnico_mandante": registro.tecnico_mandante,
                "tecnico_visitante": registro.tecnico_visitante,
                "vencedor": registro.vencedor,
                "arena": registro.arena,
                "mandante_placar": registro.mandante_placar,
                "visitante_placar": registro.visitante_placar,
                "mandante_estado": registro.mandante_estado,
                "visitante_estado": registro.visitante_estado,
                "rodata_x": registro.rodata_x,
                "partida_id": registro.partida_id,
                "rodata_y": registro.rodata_y,
                "clube": registro.clube,
                "atleta": registro.atleta,
                "minuto": registro.minuto,
                "tipo_de_gol": registro.tipo_de_gol,
                "ano_civil": registro.ano_civil,
                "temporada": registro.temporada,
                "rodata_calculada": registro.rodata_calculada,
                "rodata_final": registro.rodata_final,
                "rodata_corrigida": registro.rodata_corrigida,
                "temporada_corrigida": registro.temporada_corrigida
            })

        return jsonify(dados)

    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)