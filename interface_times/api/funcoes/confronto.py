import pandas as pd
import sys
import os
from flask import Flask, jsonify, request
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify, request   
from funcoes.ID import adicionar_ids
from escudos.cor import cor

df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'campeonato-brasileiro-full.csv'))
df = adicionar_ids(df)

# Converter placares para numérico

df['mandante_Placar'] = pd.to_numeric(df['mandante_Placar'], errors='coerce')
df['visitante_Placar'] = pd.to_numeric(df['visitante_Placar'], errors='coerce')

#comparação de times, confronto direto, confronto direto por temporada

def confrontos(time1, time2):

    confronto_direto = df[
        ((df['mandante'] == time1) & (df['visitante'] == time2)) |
        ((df['visitante'] == time1) & (df['mandante'] == time2))
    ]

    numero_confrontos = confronto_direto.shape[0]

    vitorias_time1 = (
        confronto_direto[
            (confronto_direto['mandante'] == time1) &
            (confronto_direto['mandante_Placar'] > confronto_direto['visitante_Placar'])
        ].shape[0]
        +
        confronto_direto[
            (confronto_direto['visitante'] == time1) &
            (confronto_direto['visitante_Placar'] > confronto_direto['mandante_Placar'])
        ].shape[0]
    )

    vitorias_time1_mandante = confronto_direto[
        (confronto_direto['mandante'] == time1) &
        (confronto_direto['mandante_Placar'] > confronto_direto['visitante_Placar'])
    ].shape[0]

    gols_time1 = (
        confronto_direto[
            confronto_direto['mandante'] == time1
        ]['mandante_Placar'].sum()
        +
        confronto_direto[
            confronto_direto['visitante'] == time1
        ]['visitante_Placar'].sum()
    )

    vitorias_time2 = (
        confronto_direto[
            (confronto_direto['mandante'] == time2) &
            (confronto_direto['mandante_Placar'] > confronto_direto['visitante_Placar'])
        ].shape[0]
        +
        confronto_direto[
            (confronto_direto['visitante'] == time2) &
            (confronto_direto['visitante_Placar'] > confronto_direto['mandante_Placar'])
        ].shape[0]
    )

    vitorias_time2_mandante = confronto_direto[
        (confronto_direto['mandante'] == time2) &
        (confronto_direto['mandante_Placar'] > confronto_direto['visitante_Placar'])
    ].shape[0]

    gols_time2 = (
        confronto_direto[
            confronto_direto['mandante'] == time2
        ]['mandante_Placar'].sum()
        +
        confronto_direto[
            confronto_direto['visitante'] == time2
        ]['visitante_Placar'].sum()
    )

    empates = confronto_direto[
        confronto_direto['mandante_Placar'] ==
        confronto_direto['visitante_Placar']
    ].shape[0]

    return {
        'numero_confrontos': int(numero_confrontos),
        'gols_time1': int(gols_time1),
        'gols_time2': int(gols_time2),
        'vitorias_time1': int(vitorias_time1),
        'vitorias_time1_mandante': int(vitorias_time1_mandante),
        'vitorias_time2': int(vitorias_time2),
        'vitorias_time2_mandante': int(vitorias_time2_mandante),
        'empates': int(empates)
    }





app = Flask(__name__)
@app.route('/confronto', methods=['GET'])
def get_confronto():
	time1 = request.args.get('time1')
	time2 = request.args.get('time2')

	if not time1 or not time2:
		return jsonify({'erro': 'Parâmetros "time1" e "time2" são obrigatórios'}), 400
      
	resultado = confrontos(time1, time2)
	return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)


