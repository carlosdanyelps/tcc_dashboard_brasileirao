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
from funcoes.confronto import confrontos
from timemain import comparar_times

from sqlalchemy import text
from db.db import engine
from db.db import SessionLocal
from db.models import CampeonatoBrasileiro


from flask import Flask, jsonify, request
from flask_cors import CORS

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

from sqlalchemy import text
from db.db import engine, SessionLocal

# ============================================================
# DATASET DE TIMES / ESCUDOS
# ============================================================
# MANTIDO POR ENQUANTO.
# Futuramente será migrado para PostgreSQL.

from escudos.cor import cor, bordaCor

# IMPORTANTE:
# mantenha aqui o import da função escudo que seu projeto
# já utiliza atualmente.
#
# Exemplo:
# from escudos.escudo import escudo

# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def executar_query(query, params=None):
    """
    Executa SELECT no PostgreSQL e retorna lista de dicionários.
    """

    with engine.connect() as conn:

        resultado = conn.execute(
            text(query),
            params or {}
        )

        return [
            dict(row._mapping)
            for row in resultado
        ]


def executar_scalar(query, params=None):
    """
    Executa uma query que retorna apenas um valor.
    """

    with engine.connect() as conn:

        resultado = conn.execute(
            text(query),
            params or {}
        )

        return resultado.scalar()


# ============================================================
# TABELA DE CLASSIFICAÇÃO
# ============================================================

def montar_tabela(ano, rodada=None):
    """
    Monta a classificação diretamente do PostgreSQL.

    Não utiliza Pandas.
    """

    # --------------------------------------------------------
    # Se foi informada uma rodada, somente jogos até ela.
    # --------------------------------------------------------

    filtro_rodada = ""

    params = {
        "ano": ano
    }

    if rodada is not None:

        filtro_rodada = """
            AND CAST(rodata_corrigida AS INTEGER) <= :rodada
        """

        params["rodada"] = rodada

    query = f"""
        WITH partidas AS (

            SELECT DISTINCT ON (id)
                id,
                mandante,
                visitante,
                mandante_placar,
                visitante_placar,
                vencedor,
                temporada_corrigida,
                rodata_corrigida

            FROM campeonato_brasileiro

            WHERE temporada_corrigida = :ano
              AND mandante IS NOT NULL
              AND visitante IS NOT NULL
              AND mandante_placar IS NOT NULL
              AND visitante_placar IS NOT NULL

            ORDER BY id
        ),

        jogos AS (

            SELECT
                mandante AS time,
                mandante_placar AS gols_pro,
                visitante_placar AS gols_contra,

                CASE
                    WHEN mandante_placar > visitante_placar
                        THEN 3
                    WHEN mandante_placar = visitante_placar
                        THEN 1
                    ELSE 0
                END AS pontos,

                CASE
                    WHEN mandante_placar > visitante_placar
                        THEN 1
                    ELSE 0
                END AS vitorias,

                CASE
                    WHEN mandante_placar = visitante_placar
                        THEN 1
                    ELSE 0
                END AS empates,

                CASE
                    WHEN mandante_placar < visitante_placar
                        THEN 1
                    ELSE 0
                END AS derrotas

            FROM partidas

            WHERE 1 = 1
            {filtro_rodada}

            UNION ALL

            SELECT
                visitante AS time,
                visitante_placar AS gols_pro,
                mandante_placar AS gols_contra,

                CASE
                    WHEN visitante_placar > mandante_placar
                        THEN 3
                    WHEN visitante_placar = mandante_placar
                        THEN 1
                    ELSE 0
                END AS pontos,

                CASE
                    WHEN visitante_placar > mandante_placar
                        THEN 1
                    ELSE 0
                END AS vitorias,

                CASE
                    WHEN visitante_placar = mandante_placar
                        THEN 1
                    ELSE 0
                END AS empates,

                CASE
                    WHEN visitante_placar < mandante_placar
                        THEN 1
                    ELSE 0
                END AS derrotas

            FROM partidas

            WHERE 1 = 1
            {filtro_rodada}
        )

        SELECT

            ROW_NUMBER() OVER (
                ORDER BY
                    SUM(pontos) DESC,
                    SUM(gols_pro - gols_contra) DESC,
                    SUM(gols_pro) DESC,
                    SUM(vitorias) DESC,
                    time ASC
            ) AS posicao,

            time,

            COUNT(*) AS jogos,

            SUM(vitorias) AS vitorias,

            SUM(empates) AS empates,

            SUM(derrotas) AS derrotas,

            SUM(gols_pro) AS gols_pro,

            SUM(gols_contra) AS gols_contra,

            SUM(gols_pro - gols_contra) AS saldo_gols,

            SUM(pontos) AS pontos

        FROM jogos

        GROUP BY time

        ORDER BY
            pontos DESC,
            saldo_gols DESC,
            gols_pro DESC,
            vitorias DESC,
            time ASC
    """

    return executar_query(query, params)


# ============================================================
# /TABELA
# ============================================================

@app.route('/tabela', methods=['GET'])
def get_tabela():

    ano = request.args.get('ano', type=int)
    time = request.args.get('time')

    # --------------------------------------------------------
    # SEM FILTROS
    # Retorna campeões de todas as temporadas.
    # --------------------------------------------------------

    if not ano and not time:

        query = """
            WITH partidas AS (

                SELECT DISTINCT ON (id)
                    id,
                    mandante,
                    visitante,
                    mandante_placar,
                    visitante_placar,
                    temporada_corrigida

                FROM campeonato_brasileiro

                WHERE temporada_corrigida IS NOT NULL
                  AND mandante IS NOT NULL
                  AND visitante IS NOT NULL

                ORDER BY id
            ),

            jogos AS (

                SELECT
                    temporada_corrigida AS ano,
                    mandante AS time,

                    CASE
                        WHEN mandante_placar > visitante_placar
                            THEN 3
                        WHEN mandante_placar = visitante_placar
                            THEN 1
                        ELSE 0
                    END AS pontos,

                    CASE
                        WHEN mandante_placar > visitante_placar
                            THEN 1
                        ELSE 0
                    END AS vitorias,

                    mandante_placar AS gols_pro,
                    visitante_placar AS gols_contra

                FROM partidas

                UNION ALL

                SELECT
                    temporada_corrigida AS ano,
                    visitante AS time,

                    CASE
                        WHEN visitante_placar > mandante_placar
                            THEN 3
                        WHEN visitante_placar = mandante_placar
                            THEN 1
                        ELSE 0
                    END AS pontos,

                    CASE
                        WHEN visitante_placar > mandante_placar
                            THEN 1
                        ELSE 0
                    END AS vitorias,

                    visitante_placar AS gols_pro,
                    mandante_placar AS gols_contra

                FROM partidas
            ),

            classificacao AS (

                SELECT

                    ano,
                    time,

                    SUM(pontos) AS pontos,
                    SUM(vitorias) AS vitorias,
                    SUM(gols_pro) AS gols_pro,
                    SUM(gols_pro - gols_contra) AS saldo_gols

                FROM jogos

                GROUP BY ano, time
            ),

            ranking AS (

                SELECT

                    ano,
                    time,
                    pontos,
                    vitorias,
                    gols_pro,
                    saldo_gols,

                    ROW_NUMBER() OVER (
                        PARTITION BY ano
                        ORDER BY
                            pontos DESC,
                            vitorias DESC,
                            saldo_gols DESC,
                            gols_pro DESC,
                            time ASC
                    ) AS posicao

                FROM classificacao
            )

            SELECT
                ano,
                time,
                pontos,
                vitorias,
                saldo_gols,
                gols_pro

            FROM ranking

            WHERE posicao = 1

            ORDER BY ano
        """

        campeoes = executar_query(query)

        return jsonify({
            'Campeoes todas temporadas': campeoes
        })

    # --------------------------------------------------------
    # ANO + TIME
    # --------------------------------------------------------

    if ano and time:

        tabela = montar_tabela(ano)

        registro = next(
            (
                item
                for item in tabela
                if item["time"].lower() == time.lower()
            ),
            None
        )

        if registro is None:

            return jsonify({
                'erro': 'Time ou ano não encontrado'
            }), 404

        return jsonify([registro])

    # --------------------------------------------------------
    # SOMENTE ANO
    # --------------------------------------------------------

    if ano:

        tabela = montar_tabela(ano)

        if not tabela:

            return jsonify({
                'erro': 'Ano não encontrado'
            }), 404

        return jsonify(tabela)

    return jsonify({
        'erro': (
            'Parâmetros inválidos. '
            'Use /tabela?ano=2003 '
            'ou /tabela?time=Flamengo&ano=2003'
        )
    }), 400


# ============================================================
# /TABELA/RODADA
# ============================================================

@app.route('/tabela/rodada', methods=['GET'])
def get_tabela_rodada():

    ano = request.args.get('ano', type=int)
    rodada = request.args.get('rodada', type=int)

    if not ano:

        return jsonify({
            'erro': 'Informe o ano'
        }), 400

    # Se nenhuma rodada for informada,
    # retorna a última rodada disponível.

    if rodada is None:

        rodada = executar_scalar(
            """
            SELECT MAX(
                CAST(rodata_corrigida AS INTEGER)
            )

            FROM campeonato_brasileiro

            WHERE temporada_corrigida = :ano
            """,
            {
                "ano": ano
            }
        )

        if rodada is None:

            return jsonify({
                'erro': f'Ano {ano} não encontrado'
            }), 404

    tabela = montar_tabela(
        ano,
        rodada
    )

    if not tabela:

        return jsonify({
            'erro': f'Ano {ano} não encontrado'
        }), 404

    return jsonify(tabela)


# ============================================================
# /TIMEMAIN
# ============================================================

@app.route('/timemain')
def timemain():

    time = request.args.get('time')

    if not time:

        return jsonify({
            'erro': 'Time não especificado'
        }), 400

    # --------------------------------------------------------
    # Estatísticas gerais do clube
    # --------------------------------------------------------

    query = """
        WITH partidas AS (

            SELECT DISTINCT ON (id)

                id,
                mandante,
                visitante,
                mandante_placar,
                visitante_placar,
                vencedor,
                temporada_corrigida

            FROM campeonato_brasileiro

            WHERE
                mandante = :time
                OR visitante = :time

            ORDER BY id
        )

        SELECT

            COUNT(*) AS jogos,

            SUM(
                CASE
                    WHEN mandante = :time
                         AND mandante_placar > visitante_placar
                        THEN 1

                    WHEN visitante = :time
                         AND visitante_placar > mandante_placar
                        THEN 1

                    ELSE 0
                END
            ) AS vitorias,

            SUM(
                CASE
                    WHEN mandante = :time
                         AND mandante_placar = visitante_placar
                        THEN 1

                    WHEN visitante = :time
                         AND visitante_placar = mandante_placar
                        THEN 1

                    ELSE 0
                END
            ) AS empates,

            SUM(
                CASE
                    WHEN mandante = :time
                         AND mandante_placar < visitante_placar
                        THEN 1

                    WHEN visitante = :time
                         AND visitante_placar < mandante_placar
                        THEN 1

                    ELSE 0
                END
            ) AS derrotas,

            SUM(
                CASE
                    WHEN mandante = :time
                        THEN mandante_placar
                    WHEN visitante = :time
                        THEN visitante_placar
                    ELSE 0
                END
            ) AS gols_marcados,

            SUM(
                CASE
                    WHEN mandante = :time
                        THEN visitante_placar
                    WHEN visitante = :time
                        THEN mandante_placar
                    ELSE 0
                END
            ) AS gols_sofridos

        FROM partidas
    """

    dados = executar_query(
        query,
        {"time": time}
    )

    if not dados:

        return jsonify({
            'erro': 'Time não encontrado'
        }), 404

    resultado = dados[0]

    # --------------------------------------------------------
    # Campeonatos vencidos
    # --------------------------------------------------------

    campeonatos = executar_query(
        """
        WITH classificacao AS (

            SELECT
                temporada_corrigida AS ano,
                mandante AS time,

                CASE
                    WHEN mandante_placar > visitante_placar
                        THEN 3
                    WHEN mandante_placar = visitante_placar
                        THEN 1
                    ELSE 0
                END AS pontos

            FROM (
                SELECT DISTINCT ON (id)
                    id,
                    mandante,
                    visitante,
                    mandante_placar,
                    visitante_placar,
                    temporada_corrigida

                FROM campeonato_brasileiro

                WHERE temporada_corrigida IS NOT NULL

                ORDER BY id
            ) p

            UNION ALL

            SELECT
                temporada_corrigida AS ano,
                visitante AS time,

                CASE
                    WHEN visitante_placar > mandante_placar
                        THEN 3
                    WHEN visitante_placar = mandante_placar
                        THEN 1
                    ELSE 0
                END AS pontos

            FROM (
                SELECT DISTINCT ON (id)
                    id,
                    mandante,
                    visitante,
                    mandante_placar,
                    visitante_placar,
                    temporada_corrigida

                FROM campeonato_brasileiro

                WHERE temporada_corrigida IS NOT NULL

                ORDER BY id
            ) p
        ),

        total AS (

            SELECT
                ano,
                time,
                SUM(pontos) AS pontos

            FROM classificacao

            GROUP BY ano, time
        ),

        ranking AS (

            SELECT
                *,
                ROW_NUMBER() OVER (
                    PARTITION BY ano
                    ORDER BY pontos DESC
                ) AS posicao

            FROM total
        )

        SELECT ano

        FROM ranking

        WHERE posicao = 1
          AND LOWER(time) = LOWER(:time)

        ORDER BY ano
        """,
        {"time": time}
    )

    resultado["titulos"] = [
        item["ano"]
        for item in campeonatos
    ]

    return jsonify(resultado)


# ============================================================
# /PONTUACAO_TEMPORADA
# ============================================================

@app.route('/pontuacao_temporada')
def get_pontuacao_por_temporada():

    time = request.args.get('time')
    ano = request.args.get('ano')

    if not time:

        return jsonify({
            'erro': 'Time não especificado'
        }), 400

    query = """
        WITH partidas AS (

            SELECT DISTINCT ON (id)

                id,
                mandante,
                visitante,
                mandante_placar,
                visitante_placar,
                temporada_corrigida

            FROM campeonato_brasileiro

            WHERE temporada_corrigida IS NOT NULL
              AND (
                    mandante = :time
                    OR visitante = :time
              )

            ORDER BY id
        ),

        pontos AS (

            SELECT

                temporada_corrigida AS ano,

                CASE

                    WHEN mandante = :time
                         AND mandante_placar > visitante_placar
                        THEN 3

                    WHEN visitante = :time
                         AND visitante_placar > mandante_placar
                        THEN 3

                    WHEN mandante_placar = visitante_placar
                        THEN 1

                    ELSE 0

                END AS pontos

            FROM partidas
        )

        SELECT
            ano,
            SUM(pontos) AS pontos

        FROM pontos

        GROUP BY ano

        ORDER BY ano
    """

    registros = executar_query(
        query,
        {"time": time}
    )

    if not registros:

        return jsonify({
            'erro': 'Time não encontrado'
        }), 404

    pontos = {
        int(item["ano"]): int(item["pontos"])
        for item in registros
    }

    # --------------------------------------------------------
    # Uma temporada específica
    # --------------------------------------------------------

    if ano:

        try:
            ano = int(ano)

        except ValueError:

            return jsonify({
                'erro': 'Ano inválido'
            }), 400

        if ano not in pontos:

            return jsonify({
                'erro': (
                    f'Pontuação não encontrada '
                    f'para o ano {ano}'
                )
            }), 404

        return jsonify({
            'time': time,
            'ano': ano,
            'pontos': pontos[ano]
        })

    # --------------------------------------------------------
    # Todas as temporadas
    # --------------------------------------------------------

    return jsonify({
        'time': time,
        'pontos_por_temporada': pontos
    })


# ============================================================
# /ESTATISTICAS
# ============================================================

@app.route('/estatisticas')
def get_estatisticas():

    time = request.args.get('time')

    if not time:

        return jsonify({
            'erro': 'Time não especificado'
        }), 400

    query = """
        WITH partidas AS (

            SELECT DISTINCT ON (id)

                id,
                mandante,
                visitante,
                mandante_placar,
                visitante_placar

            FROM campeonato_brasileiro

            WHERE
                mandante = :time
                OR visitante = :time

            ORDER BY id
        ),

        dados AS (

            SELECT

                CASE
                    WHEN mandante = :time
                        THEN mandante_placar
                    ELSE visitante_placar
                END AS gols,

                CASE
                    WHEN mandante = :time
                        THEN visitante_placar
                    ELSE mandante_placar
                END AS gols_sofridos,

                CASE

                    WHEN mandante = :time
                         AND mandante_placar > visitante_placar
                        THEN 1

                    WHEN visitante = :time
                         AND visitante_placar > mandante_placar
                        THEN 1

                    ELSE 0

                END AS vitoria,

                CASE

                    WHEN mandante_placar = visitante_placar
                        THEN 1

                    ELSE 0

                END AS empate,

                CASE

                    WHEN mandante = :time
                         AND mandante_placar < visitante_placar
                        THEN 1

                    WHEN visitante = :time
                         AND visitante_placar < mandante_placar
                        THEN 1

                    ELSE 0

                END AS derrota

            FROM partidas
        )

        SELECT

            COUNT(*) AS jogos,

            AVG(gols) AS media_gols,

            AVG(vitoria) AS media_vitorias,

            AVG(derrota) AS media_derrotas,

            AVG(empate) AS media_empates

        FROM dados
    """

    dados = executar_query(
        query,
        {"time": time}
    )

    if not dados or dados[0]["jogos"] == 0:

        return jsonify({
            'erro': 'Time não encontrado'
        }), 404

    estatisticas = dados[0]

    return jsonify({

        'time': time,

        # ====================================================
        # ESCUDOS / CORES
        # CONTINUAM VINDO DO DATASET ANTIGO
        # ====================================================

        'cor': cor(time),
        'borderColor': bordaCor(time),

        # ====================================================
        # ESTATÍSTICAS
        # ====================================================

        'média_gols': float(
            estatisticas['media_gols'] or 0
        ),

        'média_vitórias': float(
            estatisticas['media_vitorias'] or 0
        ),

        'média_derrotas': float(
            estatisticas['media_derrotas'] or 0
        ),

        'média_empates': float(
            estatisticas['media_empates'] or 0
        )
    })


# ============================================================
# /COMP
# CONFRONTOS DIRETOS
# ============================================================

@app.route('/comp', methods=['GET'])
def comp():

    time1 = request.args.get('time1')
    time2 = request.args.get('time2')

    if not time1 or not time2:

        return jsonify({
            'erro': 'Informe time1 e time2'
        }), 400

    query = """
        SELECT

            COUNT(*) AS jogos,

            SUM(
                CASE

                    WHEN mandante = :time1
                         AND mandante_placar > visitante_placar
                        THEN 1

                    WHEN visitante = :time1
                         AND visitante_placar > mandante_placar
                        THEN 1

                    ELSE 0

                END
            ) AS vitorias_time1,

            SUM(
                CASE

                    WHEN mandante = :time2
                         AND mandante_placar > visitante_placar
                        THEN 1

                    WHEN visitante = :time2
                         AND visitante_placar > mandante_placar
                        THEN 1

                    ELSE 0

                END
            ) AS vitorias_time2,

            SUM(
                CASE
                    WHEN mandante_placar = visitante_placar
                        THEN 1
                    ELSE 0
                END
            ) AS empates,

            SUM(
                CASE
                    WHEN mandante = :time1
                        THEN mandante_placar
                    WHEN visitante = :time1
                        THEN visitante_placar
                    ELSE 0
                END
            ) AS gols_time1,

            SUM(
                CASE
                    WHEN mandante = :time2
                        THEN mandante_placar
                    WHEN visitante = :time2
                        THEN visitante_placar
                    ELSE 0
                END
            ) AS gols_time2

        FROM (

            SELECT DISTINCT ON (id)

                id,
                mandante,
                visitante,
                mandante_placar,
                visitante_placar

            FROM campeonato_brasileiro

            WHERE
                (
                    mandante = :time1
                    AND visitante = :time2
                )
                OR
                (
                    mandante = :time2
                    AND visitante = :time1
                )

            ORDER BY id

        ) partidas
    """

    resultado = executar_query(
        query,
        {
            "time1": time1,
            "time2": time2
        }
    )

    if not resultado:

        return jsonify({
            'erro': 'Nenhum confronto encontrado'
        }), 404

    dados = resultado[0]

    return jsonify({
        'time1': time1,
        'time2': time2,
        'jogos': int(dados['jogos'] or 0),
        'vitorias_time1': int(
            dados['vitorias_time1'] or 0
        ),
        'vitorias_time2': int(
            dados['vitorias_time2'] or 0
        ),
        'empates': int(
            dados['empates'] or 0
        ),
        'gols_time1': int(
            dados['gols_time1'] or 0
        ),
        'gols_time2': int(
            dados['gols_time2'] or 0
        )
    })


# ============================================================
# /COMP/GERAL
# COMPARAÇÃO GERAL
# ============================================================

@app.route('/comp/geral', methods=['GET'])
def comp_geral():

    time1 = request.args.get('time1')
    time2 = request.args.get('time2')

    if not time1 or not time2:

        return jsonify({
            'erro': 'Informe time1 e time2'
        }), 400

    query = """
        WITH partidas AS (

            SELECT DISTINCT ON (id)

                id,
                mandante,
                visitante,
                mandante_placar,
                visitante_placar

            FROM campeonato_brasileiro

            WHERE
                mandante IN (:time1, :time2)
                OR visitante IN (:time1, :time2)

            ORDER BY id
        ),

        estatisticas AS (

            SELECT

                :time1 AS time,

                COUNT(*) AS jogos,

                SUM(
                    CASE

                        WHEN mandante = :time1
                             AND mandante_placar > visitante_placar
                            THEN 1

                        WHEN visitante = :time1
                             AND visitante_placar > mandante_placar
                            THEN 1

                        ELSE 0

                    END
                ) AS vitorias,

                SUM(
                    CASE
                        WHEN mandante_placar = visitante_placar
                            THEN 1
                        ELSE 0
                    END
                ) AS empates,

                SUM(
                    CASE

                        WHEN mandante = :time1
                             AND mandante_placar < visitante_placar
                            THEN 1

                        WHEN visitante = :time1
                             AND visitante_placar < mandante_placar
                            THEN 1

                        ELSE 0

                    END
                ) AS derrotas,

                SUM(
                    CASE
                        WHEN mandante = :time1
                            THEN mandante_placar
                        WHEN visitante = :time1
                            THEN visitante_placar
                        ELSE 0
                    END
                ) AS gols_marcados

            FROM partidas

            WHERE
                mandante = :time1
                OR visitante = :time1

            UNION ALL

            SELECT

                :time2 AS time,

                COUNT(*) AS jogos,

                SUM(
                    CASE

                        WHEN mandante = :time2
                             AND mandante_placar > visitante_placar
                            THEN 1

                        WHEN visitante = :time2
                             AND visitante_placar > mandante_placar
                            THEN 1

                        ELSE 0

                    END
                ) AS vitorias,

                SUM(
                    CASE
                        WHEN mandante_placar = visitante_placar
                            THEN 1
                        ELSE 0
                    END
                ) AS empates,

                SUM(
                    CASE

                        WHEN mandante = :time2
                             AND mandante_placar < visitante_placar
                            THEN 1

                        WHEN visitante = :time2
                             AND visitante_placar < mandante_placar
                            THEN 1

                        ELSE 0

                    END
                ) AS derrotas,

                SUM(
                    CASE
                        WHEN mandante = :time2
                            THEN mandante_placar
                        WHEN visitante = :time2
                            THEN visitante_placar
                        ELSE 0
                    END
                ) AS gols_marcados

            FROM partidas

            WHERE
                mandante = :time2
                OR visitante = :time2
        )

        SELECT *

        FROM estatisticas
    """

    resultado = executar_query(
        query,
        {
            "time1": time1,
            "time2": time2
        }
    )

    return jsonify(resultado)


# ============================================================
# TESTE DO BANCO
# ============================================================

@app.route('/teste-db', methods=['GET'])
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


# ============================================================
# RETORNAR TODOS OS DADOS DO BANCO
# ============================================================

@app.route('/dados-db', methods=['GET'])
def dados_db():

    query = """
        SELECT *
        FROM campeonato_brasileiro
        ORDER BY id
    """

    dados = executar_query(query)

    return jsonify(dados)


# ============================================================
# ESCUDO
# ============================================================
# NÃO MIGRAR AGORA.
# DEIXE SUA IMPLEMENTAÇÃO ATUAL AQUI.
#
# Exemplo:
#
# @app.route('/escudo/<int:id>')
# def get_escudo(id):
#     return escudo(id)
#
# ============================================================


if __name__ == '__main__':
    app.run(debug=True)

