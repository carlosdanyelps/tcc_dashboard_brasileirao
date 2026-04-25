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

# Calcular total de gols por time (mandante + visitante)
gols_mandante = df.groupby('mandante')['mandante_Placar'].sum()
gols_visitante = df.groupby('visitante')['visitante_Placar'].sum()
######=====================================================================#####
gols_por_time = gols_mandante.add(gols_visitante, fill_value=0).astype(int)

# Calcular pontos por partida
df['pontos_mandante'] = (df['mandante_Placar'] > df['visitante_Placar']) * 3 + (df['mandante_Placar'] == df['visitante_Placar']) * 1
df['pontos_visitante'] = (df['visitante_Placar'] > df['mandante_Placar']) * 3 + (df['mandante_Placar'] == df['visitante_Placar']) * 1

# Pontos totais por time (mandante + visitante, todas as temporadas)
pontos_mandante = df.groupby('mandante')['pontos_mandante'].sum()
pontos_visitante = df.groupby('visitante')['pontos_visitante'].sum()
pontos_geral = pontos_mandante.add(pontos_visitante, fill_value=0).astype(int)

# Classificação geral dos melhores times
classificacao_geral = pontos_geral.sort_values(ascending=False)

print('Classificação geral dos melhores times (todas as temporadas):')
print(classificacao_geral)

# Calcular vitórias, derrotas e empates
vitorias_mandante = df[df['mandante_Placar'] > df['visitante_Placar']].groupby('mandante').size()
vitorias_visitante = df[df['visitante_Placar'] > df['mandante_Placar']].groupby('visitante').size()
vitorias_por_time = vitorias_mandante.add(vitorias_visitante, fill_value=0).astype(int)

derrotas_mandante = df[df['mandante_Placar'] < df['visitante_Placar']].groupby('mandante').size()
derrotas_visitante = df[df['visitante_Placar'] < df['mandante_Placar']].groupby('visitante').size()
derrotas_por_time = derrotas_mandante.add(derrotas_visitante, fill_value=0).astype(int)

empates_mandante = df[df['mandante_Placar'] == df['visitante_Placar']].groupby('mandante').size()
empates_visitante = df[df['mandante_Placar'] == df['visitante_Placar']].groupby('visitante').size()
empates_por_time = empates_mandante.add(empates_visitante, fill_value=0).astype(int)


# Número de temporadas por time (contando apenas temporadas distintas em que participou)
df['ano'] = pd.to_datetime(df['data'], errors='coerce').dt.year
times_anos = pd.concat([
	df[['mandante', 'ano']].rename(columns={'mandante': 'time'}),
	df[['visitante', 'ano']].rename(columns={'visitante': 'time'})
])
anos_por_time = times_anos.drop_duplicates().groupby('time')['ano'].nunique()

# Calcular títulos por time
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
	classificacao.sort_values(['ano', 'pontos'], ascending=[True, False])
	.groupby('ano').first().reset_index()
)
titulos_por_time = campeoes['time'].value_counts().to_dict()

## Calcular rebaixamentos únicos por time
rebaixamentos_por_time = {}
for ano in classificacao['ano'].unique():
	class_ano = classificacao[classificacao['ano'] == ano].sort_values('pontos', ascending=False)
	rebaixados_ano = class_ano.tail(4)['time'].tolist()
	for time_name in rebaixados_ano:
		rebaixamentos_por_time.setdefault(time_name, []).append(int(ano))

# Função para contar rebaixamentos únicos (sequências de anos consecutivos contam como 1)
def contar_rebaixamentos_unicos(anos):
	if not anos:
		return 0
	anos = sorted(anos)
	count = 1
	for i in range(1, len(anos)):
		if anos[i] != anos[i-1] + 1:
			count += 1
	return count

rebaixamentos_unicos = {t: contar_rebaixamentos_unicos(rebaixamentos_por_time.get(t, [])) for t in pontos_geral.index}

# Mapear id dos times
todos_times = pd.concat([df["mandante"], df["visitante"]]).unique()
time_para_id = {time: i + 1 for i, time in enumerate(todos_times)}


# Montar DataFrame final com id e cor nas primeiras colunas
df_final = pd.DataFrame({
	'time': pontos_geral.index,
	'id': pontos_geral.index.map(lambda t: time_para_id.get(t, 0)),
	'cor': pontos_geral.index.map(cor),
	'pontos': pontos_geral,
	'vitorias': vitorias_por_time,
	'derrotas': derrotas_por_time,
	'empates': empates_por_time,
	'gols': gols_por_time,
	'titulos': pontos_geral.index.map(lambda t: titulos_por_time.get(t, 0)),
	'temporadas': anos_por_time,
	'rebaixamentos': pontos_geral.index.map(lambda t: rebaixamentos_unicos.get(t, 0))
})
df_final = df_final.fillna(0).astype({'time': str, 'id': int, 'pontos': int, 'vitorias': int, 'derrotas': int, 'empates': int, 'gols': int, 'titulos': int, 'temporadas': int, 'rebaixamentos': int})
df_final = df_final.sort_values('pontos', ascending=False)

print('\nResumo geral dos times:')
print(df_final)
######=====================================================================#####

app = Flask(__name__)
@app.route('/api/campanha', methods=['GET'])
def get_campanha():
	return jsonify(df_final.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
