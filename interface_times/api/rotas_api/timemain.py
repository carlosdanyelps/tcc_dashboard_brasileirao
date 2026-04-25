from flask import Flask, request, jsonify
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes.ID import adicionar_ids
from escudos.cor import cor

df = pd.read_csv('campeonato-brasileiro-full.csv')
df = adicionar_ids(df)

# Converter gols para número
df['mandante_Placar'] = pd.to_numeric(df['mandante_Placar'])
df['visitante_Placar'] = pd.to_numeric(df['visitante_Placar'])

# Criar coluna ANO a partir da data
df['data'] = pd.to_datetime(df['data'], dayfirst=True)
df['ano'] = df['data'].dt.year

# =====================
# CÁLCULOS PERMANENTES
# =====================
resultados = []
for _, row in df.iterrows():
    if row['mandante_Placar'] > row['visitante_Placar']:
        pontos_m, pontos_v = 3, 0
    elif row['mandante_Placar'] < row['visitante_Placar']:
        pontos_m, pontos_v = 0, 3
    else:
        pontos_m, pontos_v = 1, 1

    resultados.append([row['ano'], row['mandante'], pontos_m])
    resultados.append([row['ano'], row['visitante'], pontos_v])

classificacao = pd.DataFrame(resultados, columns=['ano', 'time', 'pontos'])
classificacao = classificacao.groupby(['ano', 'time'])['pontos'].sum().reset_index()

campeoes = (
    classificacao
    .sort_values(['ano', 'pontos'], ascending=[True, False])
    .groupby('ano')
    .first()
    .reset_index()
)
titulos_por_time = campeoes['time'].value_counts().to_dict()

rebaixamentos_por_time = {}
for ano in classificacao['ano'].unique():
    class_ano = classificacao[classificacao['ano'] == ano].sort_values('pontos', ascending=False)
    rebaixados_ano = class_ano.tail(4)['time'].tolist()
    for time_name in rebaixados_ano:
        rebaixamentos_por_time.setdefault(time_name, []).append(int(ano))

all_times = sorted(pd.unique(df[['mandante', 'visitante']].values.ravel('K')))

vitorias_mandante = (
    df[df['mandante_Placar'] > df['visitante_Placar']]
    .groupby('mandante')
    .size()
)
vitorias_visitante = (
    df[df['visitante_Placar'] > df['mandante_Placar']]
    .groupby('visitante')
    .size()
)
vitorias_por_time = vitorias_mandante.add(vitorias_visitante, fill_value=0).astype(int).to_dict()
derrotas_mandante = (
    df[df['mandante_Placar'] < df['visitante_Placar']]
    .groupby('mandante')
    .size()
)
derrotas_visitante = (
    df[df['visitante_Placar'] < df['mandante_Placar']]
    .groupby('visitante')
    .size()
)
derrotas_por_time = derrotas_mandante.add(derrotas_visitante, fill_value=0).astype(int).to_dict()

gols_mandante = df.groupby('mandante')['mandante_Placar'].sum()
gols_visitante = df.groupby('visitante')['visitante_Placar'].sum()
gols_por_time = gols_mandante.add(gols_visitante, fill_value=0).astype(int).to_dict()

app = Flask(__name__)


def get_time_id(time):
    id_time = df.loc[df['mandante'] == time, 'mandante_id']
    if id_time.empty:
        id_time = df.loc[df['visitante'] == time, 'visitante_id']
    return int(id_time.iloc[0]) if not id_time.empty else None


def build_time_summary(time):
    id_time = get_time_id(time)
    return {
        'ID': id_time,
        'time': time,
        'cor': cor(time),
        'vitorias': int(vitorias_por_time.get(time, 0)),
        'derrotas': int(derrotas_por_time.get(time, 0)),
        'gols': int(gols_por_time.get(time, 0)),
        'titulos_brasileirao': int(titulos_por_time.get(time, 0)),
        'rebaixamentos': rebaixamentos_por_time.get(time, []),
        'URL escudo': f'http://localhost:5000/escudo/{id_time}' if id_time is not None else None
    }


def get_all_teams_summary():
    return [build_time_summary(time) for time in all_times]


@app.route('/timemain/time_main', methods=['GET'])
def resumo_time():
    time = request.args.get('time')

    if not time:
        return jsonify(get_all_teams_summary())

    if time not in all_times:
        return jsonify({'error': 'Time não encontrado'}), 404

    # =====================
    # GOLS
    # =====================
    gols_mandante = df.loc[df['mandante'] == time, 'mandante_Placar'].sum()
    gols_visitante = df.loc[df['visitante'] == time, 'visitante_Placar'].sum()
    total_gols = gols_mandante + gols_visitante

    # =====================
    # VITÓRIAS
    # =====================
    vitorias_mandante = df[
        (df['mandante'] == time) &
        (df['mandante_Placar'] > df['visitante_Placar'])
    ].shape[0]

    vitorias_visitante = df[
        (df['visitante'] == time) &
        (df['visitante_Placar'] > df['mandante_Placar'])
    ].shape[0]

    total_vitorias = vitorias_mandante + vitorias_visitante
    #=======================
    # DERROTAS
    #=======================
    derrotas_mandante = df[
        (df['mandante'] == time) &
        (df['mandante_Placar'] < df['visitante_Placar'])
    ].shape[0]
    derrotas_visitante = df[
        (df['visitante'] == time) &
        (df['visitante_Placar'] < df['mandante_Placar'])
    ].shape[0]

    total_derrotas = derrotas_mandante + derrotas_visitante

    # =====================
    # TÍTULOS
    # =====================
    tabela = []

    for _, row in df.iterrows():
        if row['mandante_Placar'] > row['visitante_Placar']:
            pontos_m, pontos_v = 3, 0
        elif row['mandante_Placar'] < row['visitante_Placar']:
            pontos_m, pontos_v = 0, 3
        else:
            pontos_m, pontos_v = 1, 1

        tabela.append([row['ano'], row['mandante'], pontos_m])
        tabela.append([row['ano'], row['visitante'], pontos_v])

    tabela_df = pd.DataFrame(tabela, columns=['ano', 'time', 'pontos'])
    classificacao = tabela_df.groupby(['ano', 'time'])['pontos'].sum().reset_index()

    campeoes = (
        classificacao
        .sort_values(['ano', 'pontos'], ascending=[True, False])
        .groupby('ano')
        .first()
        .reset_index()
    )
    titulos = campeoes[campeoes['time'] == time].shape[0]

    # =====================
    # REBAIXAMENTOS
    # =====================
    rebaixamentos = []

    for ano in classificacao['ano'].unique():
        class_ano = classificacao[classificacao['ano'] == ano].sort_values('pontos', ascending=False)
        rebaixados_ano = class_ano.tail(4)['time'].tolist()  # últimos 4 colocados
        if time in rebaixados_ano:
            rebaixamentos.append(int(ano))
    id_time = df.loc[df['mandante'] == time, 'mandante_id']

    if id_time.empty:
        id_time = df.loc[df['visitante'] == time, 'visitante_id']

    id_time = int(id_time.iloc[0]) if not id_time.empty else None
    return jsonify({
        'ID': id_time,
        'time': time,
        'cor': cor(time),
        'gols': int(total_gols),
        'vitorias': int(total_vitorias),
        'derrotas': int(total_derrotas),
        'titulos_brasileirao': int(titulos),
        'rebaixamentos': rebaixamentos,
        'URL escudo': f'http://localhost:5000/escudo/{id_time}'  # Exemplo de URL para escudo
    })


if __name__ == '__main__':
    app.run(debug=True)