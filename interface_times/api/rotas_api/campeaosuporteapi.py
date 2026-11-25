from flask import Flask, request, jsonify
from sqlalchemy import text
import os
import sys


API_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if API_DIR not in sys.path:
    sys.path.insert(0, API_DIR)

from db.db import SessionLocal
from escudos.cor import cor, bordaCor


app = Flask(__name__)


# =========================
# CONFIGURAÇÕES
# =========================

url_escudo_base = 'http://localhost:5000/escudo/'


# =========================
# CARREGAR DADOS DO BANCO
# =========================

def carregar_partidas():

    db = SessionLocal()

    try:
        resultado = db.execute(
            text("""
                SELECT
                    id,
                    data,
                    mandante,
                    visitante,
                    mandante_placar,
                    visitante_placar,
                    partida_id,
                    ano_civil,
                    temporada,
                    rodata_corrigida,
                    temporada_corrigida
                FROM campeonato_brasileiro
                ORDER BY data
            """)
        )

        return [dict(row._mapping) for row in resultado]

    finally:
        db.close()


# =========================
# PREPARAR DADOS
# =========================

def preparar_dados():

    dados = carregar_partidas()

    if not dados:
        return []

    # ---------------------------------
    # Criar IDs dos times
    # ---------------------------------

    todos_times = []

    for partida in dados:

        if partida['mandante'] not in todos_times:
            todos_times.append(partida['mandante'])

        if partida['visitante'] not in todos_times:
            todos_times.append(partida['visitante'])

    time_para_id = {
        time: i + 1
        for i, time in enumerate(todos_times)
    }


    # ---------------------------------
    # Criar partidas únicas
    # ---------------------------------

    partidas = {}

    for partida in dados:

        partida_id = partida['partida_id']

        if partida_id not in partidas:
            partidas[partida_id] = partida

    partidas = list(partidas.values())


    # ---------------------------------
    # Calcular pontos
    # ---------------------------------

    for partida in partidas:

        mandante_placar = partida['mandante_placar']
        visitante_placar = partida['visitante_placar']

        if mandante_placar is None or visitante_placar is None:

            partida['pontos_m'] = 0
            partida['pontos_v'] = 0

        elif mandante_placar > visitante_placar:

            partida['pontos_m'] = 3
            partida['pontos_v'] = 0

        elif visitante_placar > mandante_placar:

            partida['pontos_m'] = 0
            partida['pontos_v'] = 3

        else:

            partida['pontos_m'] = 1
            partida['pontos_v'] = 1


        # IDs

        partida['mandante_id'] = time_para_id[
            partida['mandante']
        ]

        partida['visitante_id'] = time_para_id[
            partida['visitante']
        ]


    return partidas


# =========================
# CONSTRUIR TABELA
# =========================

def construir_tabela():

    partidas = preparar_dados()

    tabela = {}


    for partida in partidas:

        temporada = partida['temporada_corrigida']

        if temporada is None:
            continue


        mandante = partida['mandante']
        visitante = partida['visitante']


        # ---------------------------------
        # Criar registros dos times
        # ---------------------------------

        if (temporada, mandante) not in tabela:

            tabela[(temporada, mandante)] = {

                'temporada': temporada,
                'time': mandante,

                'pontos': 0,
                'gols_pro': 0,
                'gols_tomados': 0,

                'mandante_id':
                    partida['mandante_id']
            }


        if (temporada, visitante) not in tabela:

            tabela[(temporada, visitante)] = {

                'temporada': temporada,
                'time': visitante,

                'pontos': 0,
                'gols_pro': 0,
                'gols_tomados': 0,

                'mandante_id':
                    partida['visitante_id']
            }


        time_m = tabela[(temporada, mandante)]
        time_v = tabela[(temporada, visitante)]


        # ---------------------------------
        # GOLS
        # ---------------------------------

        gols_m = partida['mandante_placar'] or 0
        gols_v = partida['visitante_placar'] or 0


        time_m['gols_pro'] += gols_m
        time_m['gols_tomados'] += gols_v

        time_v['gols_pro'] += gols_v
        time_v['gols_tomados'] += gols_m


        # ---------------------------------
        # PONTOS
        # ---------------------------------

        time_m['pontos'] += partida['pontos_m']
        time_v['pontos'] += partida['pontos_v']


    # ---------------------------------
    # Transformar em lista
    # ---------------------------------

    resultado = []

    for registro in tabela.values():

        registro['saldo'] = (
            registro['gols_pro']
            - registro['gols_tomados']
        )

        registro['url_escudo'] = (
            url_escudo_base
            + str(registro['mandante_id'])
        )

        registro['cor'] = cor(registro['time'])
        registro['bordaCor'] = bordaCor(registro['time'])

        resultado.append(registro)


    return resultado


# =========================
# TABELA GERAL
# =========================

def obter_tabela():

    return construir_tabela()


# =========================
# CAMPEÕES
# =========================

def construir_campeoes():

    tabela = construir_tabela()

    campeoes = {}


    for registro in tabela:

        temporada = registro['temporada']

        atual = campeoes.get(temporada)

        if atual is None:

            campeoes[temporada] = registro

            continue


        # Critérios de classificação

        chave_atual = (
            registro['pontos'],
            registro['saldo'],
            registro['gols_pro']
        )

        chave_anterior = (
            atual['pontos'],
            atual['saldo'],
            atual['gols_pro']
        )


        if chave_atual > chave_anterior:

            campeoes[temporada] = registro


    return list(campeoes.values())


# =========================
# FORMATO JSON DO CAMPEÃO
# =========================

def ordenar_campeao(c):

    return {

        'temporada':
            int(c['temporada']),

        'time':
            c['time'],

        'pontos':
            int(c['pontos']),

        'gols_pro':
            int(c['gols_pro']),

        'gols_tomados':
            int(c['gols_tomados']),

        'saldo':
            int(c['saldo']),

        'escudo':
            c['url_escudo'],

        'cor':
            c['cor'],

        'bordaCor':
            c['bordaCor']
    }


# =========================
# ROTA /tabela
# =========================

@app.route('/tabela')
def tabela():

    ano = request.args.get('ano', type=int)


    # ---------------------------------
    # Sem ano
    # ---------------------------------

    if not ano:

        campeoes = construir_campeoes()

        campeoes_ordenados = [
            ordenar_campeao(c)
            for c in campeoes
        ]

        return jsonify({
            'campeoes': campeoes_ordenados
        })


    # ---------------------------------
    # Com ano
    # ---------------------------------

    dados = obter_tabela()

    tabela_ano = [
        registro
        for registro in dados
        if registro['temporada'] == ano
    ]


    if not tabela_ano:

        return jsonify({
            'erro': 'Ano não encontrado'
        }), 404


    tabela_ano.sort(
        key=lambda x: (
            x['pontos'],
            x['saldo'],
            x['gols_pro']
        ),
        reverse=True
    )


    for posicao, registro in enumerate(
        tabela_ano,
        start=1
    ):

        registro['posicao'] = posicao


    return jsonify(tabela_ano)


# =========================
# ROTA /campeao
# =========================

@app.route('/campeao')
def campeao():

    ano = request.args.get('ano', type=int)


    if not ano:

        return jsonify({
            'erro': 'Informe o ano'
        }), 400


    dados = obter_tabela()


    tabela_ano = [
        registro
        for registro in dados
        if registro['temporada'] == ano
    ]


    if not tabela_ano:

        return jsonify({
            'erro': 'Ano não encontrado'
        }), 404


    tabela_ano.sort(
        key=lambda x: (
            x['pontos'],
            x['saldo'],
            x['gols_pro']
        ),
        reverse=True
    )


    return jsonify(
        ordenar_campeao(tabela_ano[0])
    )


# =========================
# RUN
# =========================

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )