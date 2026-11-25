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
from funcoes.confronto import confrontos
from timemain import comparar_times
from rotas_api.football_data import FootballDataError, get_current_season_data

df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'campeonato-brasileiro-full.csv'))


app = Flask(__name__)
CORS(app)


def obter_partidas_validas():
    partidas = df.copy()
    partidas['_temporada'] = pd.to_numeric(partidas['temporada_corrigida'], errors='coerce')
    id_partida = pd.to_numeric(partidas['partida_id'], errors='coerce')
    id_registro = pd.to_numeric(partidas['ID'], errors='coerce')
    partidas['_id_partida'] = id_partida.fillna(id_registro)
    partidas['_gols_mandante'] = pd.to_numeric(partidas['mandante_Placar'], errors='coerce')
    partidas['_gols_visitante'] = pd.to_numeric(partidas['visitante_Placar'], errors='coerce')
    partidas = partidas.dropna(
        subset=[
            '_temporada',
            '_id_partida',
            '_gols_mandante',
            '_gols_visitante',
            'mandante',
            'visitante',
        ]
    )
    return partidas.drop_duplicates(
        subset=['_temporada', '_id_partida'],
        keep='first',
    )


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


@app.route('/jogadores-tecnicos', methods=['GET'])
def get_jogadores_tecnicos():
    temporada = request.args.get('temporada', type=int)
    partidas = df.drop_duplicates(subset='ID', keep='first').copy()
    partidas['_temporada'] = pd.to_numeric(partidas['temporada_corrigida'], errors='coerce')
    partidas = partidas[partidas['_temporada'] >= 2014]
    temporadas_disponiveis = sorted(partidas['_temporada'].dropna().astype(int).unique().tolist())

    if temporada is not None and temporada not in temporadas_disponiveis:
        return jsonify({'erro': 'Temporada indisponível para estatísticas individuais'}), 404

    if temporada is not None:
        partidas = partidas[partidas['_temporada'] == temporada]

    partidas['_gols_mandante'] = pd.to_numeric(partidas['mandante_Placar'], errors='coerce')
    partidas['_gols_visitante'] = pd.to_numeric(partidas['visitante_Placar'], errors='coerce')
    partidas = partidas.dropna(subset=['_gols_mandante', '_gols_visitante'])

    gols = df.copy()
    gols['_temporada'] = pd.to_numeric(gols['temporada_corrigida'], errors='coerce')
    gols = gols[gols['_temporada'] >= 2014]
    if temporada is not None:
        gols = gols[gols['_temporada'] == temporada]

    gols['_atleta'] = gols['atleta'].fillna('').astype(str).str.strip()
    gols['_tipo_de_gol'] = gols['tipo_de_gol'].fillna('').astype(str).str.strip().str.casefold()
    gols['_clube'] = gols['clube'].fillna('').astype(str).str.strip()
    clube_valido = ~gols['_clube'].str.fullmatch(r'\d+')
    gols['_clube_validado'] = gols['_clube'].where(clube_valido, '')
    gols = gols[(gols['_atleta'] != '') & (gols['_tipo_de_gol'] != 'gol contra')]

    gols_por_jogador = (
        gols.groupby('_atleta')
        .agg(gols=('_atleta', 'size'))
        .reset_index()
        .rename(columns={'_atleta': 'jogador'})
    )
    clubes_por_jogador = (
        gols.groupby('_atleta')['_clube_validado']
        .agg(lambda clubes: sorted(clubes[clubes != ''].unique().tolist()))
        .reset_index()
        .rename(columns={'_atleta': 'jogador', '_clube_validado': 'clubes'})
    )
    artilheiros = (
        gols_por_jogador.merge(clubes_por_jogador, on='jogador')
        .sort_values(['gols', 'jogador'], ascending=[False, True])
        .head(10)
    )

    mandantes = partidas[
        ['tecnico_mandante', 'mandante', '_gols_mandante', '_gols_visitante']
    ].rename(columns={
        'tecnico_mandante': 'tecnico',
        'mandante': 'clube',
        '_gols_mandante': 'gols_feitos',
        '_gols_visitante': 'gols_sofridos',
    })
    visitantes = partidas[
        ['tecnico_visitante', 'visitante', '_gols_visitante', '_gols_mandante']
    ].rename(columns={
        'tecnico_visitante': 'tecnico',
        'visitante': 'clube',
        '_gols_visitante': 'gols_feitos',
        '_gols_mandante': 'gols_sofridos',
    })
    atuacoes = pd.concat([mandantes, visitantes], ignore_index=True)
    atuacoes['tecnico'] = atuacoes['tecnico'].fillna('').astype(str).str.strip()
    atuacoes = atuacoes[atuacoes['tecnico'] != '']
    atuacoes['vitorias'] = (atuacoes['gols_feitos'] > atuacoes['gols_sofridos']).astype(int)
    atuacoes['derrotas'] = (atuacoes['gols_feitos'] < atuacoes['gols_sofridos']).astype(int)
    atuacoes['empates'] = (atuacoes['gols_feitos'] == atuacoes['gols_sofridos']).astype(int)
    tecnicos = (
        atuacoes.groupby('tecnico')
        .agg(
            vitorias=('vitorias', 'sum'),
            derrotas=('derrotas', 'sum'),
            empates=('empates', 'sum'),
            partidas=('tecnico', 'size'),
            clubes=('clube', lambda clubes: sorted(clubes.dropna().astype(str).unique().tolist())),
        )
        .reset_index()
    )
    tecnicos['aproveitamento'] = (
        (tecnicos['vitorias'] * 3 + tecnicos['empates']) / (tecnicos['partidas'] * 3) * 100
    ).round(1)
    tecnicos = tecnicos.sort_values(
        ['vitorias', 'partidas', 'tecnico'],
        ascending=[False, False, True],
    )

    nomes_mandante = partidas['tecnico_mandante'].fillna('').astype(str).str.strip()
    nomes_visitante = partidas['tecnico_visitante'].fillna('').astype(str).str.strip()
    resumo = {
        'partidas': int(len(partidas)),
        'partidas_com_tecnico': int(((nomes_mandante != '') | (nomes_visitante != '')).sum()),
        'partidas_com_ambos_tecnicos': int(((nomes_mandante != '') & (nomes_visitante != '')).sum()),
        'gols_creditados': int(len(gols)),
        'jogadores': int(gols['_atleta'].nunique()),
        'tecnicos': int(tecnicos['tecnico'].nunique()),
    }

    return jsonify({
        'temporada': temporada,
        'temporadas_disponiveis': temporadas_disponiveis,
        'resumo': resumo,
        'artilheiros': artilheiros.to_dict(orient='records'),
        'tecnicos': tecnicos.to_dict(orient='records'),
    })


@app.route('/confronto-direto/opcoes', methods=['GET'])
def get_opcoes_confronto_direto():
    partidas = obter_partidas_validas()
    times = sorted(
        set(partidas['mandante'].astype(str))
        | set(partidas['visitante'].astype(str))
    )
    temporadas = sorted(partidas['_temporada'].astype(int).unique().tolist())
    return jsonify({'times': times, 'temporadas': temporadas})


@app.route('/confronto-direto', methods=['GET'])
def get_confronto_direto():
    time1 = request.args.get('time1', '').strip()
    time2 = request.args.get('time2', '').strip()
    temporada = request.args.get('temporada', type=int)

    if not time1 or not time2:
        return jsonify({'erro': 'Informe os dois times para comparar'}), 400
    if time1 == time2:
        return jsonify({'erro': 'Selecione dois times diferentes'}), 400

    partidas = obter_partidas_validas()
    times_validos = set(partidas['mandante'].astype(str)) | set(partidas['visitante'].astype(str))
    if time1 not in times_validos or time2 not in times_validos:
        return jsonify({'erro': 'Um ou mais times não foram encontrados'}), 404

    confronto = partidas[
        (
            (partidas['mandante'] == time1)
            & (partidas['visitante'] == time2)
        )
        | (
            (partidas['mandante'] == time2)
            & (partidas['visitante'] == time1)
        )
    ].copy()
    temporadas_confronto = sorted(
        confronto['_temporada'].astype(int).unique().tolist()
    )

    if temporada is not None:
        confronto = confronto[confronto['_temporada'] == temporada]

    time1_mandante = confronto['mandante'] == time1
    time1_gols = (
        confronto.loc[time1_mandante, '_gols_mandante'].sum()
        + confronto.loc[~time1_mandante, '_gols_visitante'].sum()
    )
    time2_gols = (
        confronto.loc[time1_mandante, '_gols_visitante'].sum()
        + confronto.loc[~time1_mandante, '_gols_mandante'].sum()
    )
    vitorias_time1 = (
        (
            time1_mandante
            & (confronto['_gols_mandante'] > confronto['_gols_visitante'])
        )
        | (
            ~time1_mandante
            & (confronto['_gols_visitante'] > confronto['_gols_mandante'])
        )
    ).sum()
    vitorias_time2 = (
        (
            time1_mandante
            & (confronto['_gols_mandante'] < confronto['_gols_visitante'])
        )
        | (
            ~time1_mandante
            & (confronto['_gols_visitante'] < confronto['_gols_mandante'])
        )
    ).sum()
    empates = (
        confronto['_gols_mandante'] == confronto['_gols_visitante']
    ).sum()
    total_partidas = len(confronto)
    total_gols = int(time1_gols + time2_gols)

    historico = confronto.sort_values(
        ['_temporada', 'data', 'rodata'],
        ascending=[False, False, False],
        na_position='last',
    )
    partidas = []
    for _, partida in historico.iterrows():
        gols_mandante = int(partida['_gols_mandante'])
        gols_visitante = int(partida['_gols_visitante'])
        rodada = pd.to_numeric(partida['rodata'], errors='coerce')
        partidas.append({
            'temporada': int(partida['_temporada']),
            'data': str(partida['data']) if pd.notna(partida['data']) else '',
            'rodada': int(rodada) if pd.notna(rodada) else None,
            'mandante': str(partida['mandante']),
            'visitante': str(partida['visitante']),
            'gols_mandante': gols_mandante,
            'gols_visitante': gols_visitante,
            'vencedor': (
                str(partida['mandante'])
                if gols_mandante > gols_visitante
                else str(partida['visitante'])
                if gols_visitante > gols_mandante
                else None
            ),
        })

    return jsonify({
        'time1': time1,
        'time2': time2,
        'temporada': temporada,
        'temporadas_disponiveis': temporadas_confronto,
        'resumo': {
            'partidas': total_partidas,
            'vitorias_time1': int(vitorias_time1),
            'vitorias_time2': int(vitorias_time2),
            'empates': int(empates),
            'gols_time1': int(time1_gols),
            'gols_time2': int(time2_gols),
            'total_gols': total_gols,
            'media_gols': round(total_gols / total_partidas, 2) if total_partidas else 0,
        },
        'partidas_detalhadas': partidas,
    })

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

@app.route('/timemain/time_main')
def timemain_times():
    return resumo_time()

################################################################
############# ESCUDO #############
###############################################################
@app.route('/escudo/<int:id>')
def get_escudo(id):
    return escudo(id)

@app.route('/football-data/brasileirao', methods=['GET'])
def get_brasileirao_atual():
    try:
        return jsonify(get_current_season_data())
    except FootballDataError as error:
        return jsonify({'erro': str(error)}), error.status_code

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

if __name__ == '__main__':
    app.run(debug=True)