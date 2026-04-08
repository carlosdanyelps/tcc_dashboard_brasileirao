from flask import Flask, request, jsonify
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes.ID import adicionar_ids


df = pd.read_csv('campeonato-brasileiro-full.csv')
df = adicionar_ids(df)

# Converter gols para número
df['mandante_Placar'] = pd.to_numeric(df['mandante_Placar'])
df['visitante_Placar'] = pd.to_numeric(df['visitante_Placar'])

# Criar coluna ANO a partir da data
df['data'] = pd.to_datetime(df['data'], dayfirst=True)
df['ano'] = df['data'].dt.year

app = Flask(__name__)

@app.route('/timemain/time_main', methods=['GET'])
def resumo_time():
    time = request.args.get('time')

    if not time:
        return jsonify({'error': 'Time não informado'}), 400

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
        'time': time,
        'ID': id_time,
        'vitorias': int(total_vitorias),
        'gols': int(total_gols),
        'titulos_brasileirao': int(titulos),
        'rebaixamentos': rebaixamentos,
        'URL escudo': f'http://localhost:5000/escudo/{id_time}'  # Exemplo de URL para escudo
    })


if __name__ == '__main__':
    app.run(debug=True)