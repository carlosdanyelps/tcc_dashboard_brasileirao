from flask import Flask, request, jsonify
import pandas as pd
#from partidas_rodadas import * 
df = pd.read_csv('campeonato-brasileiro-full.csv')
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
#gols(1)
@app.route('/API/gol', methods=['GET'])
def gol():
    time = request.args.get('time')
    if not time:
        return jsonify({'error': 'Time não fornecido'}), 400
    gols_feitos = (
    df.loc[df['mandante'] == time, "mandante_Placar"].sum()
    )
    return jsonify({
        'time': time,
        'gols_feitos': int(gols_feitos)
    })
@app.route('/API/med_gols_fet', methods=['GET'])
def med_gols_fet():
    time = request.args.get('time')
    if not time:
        return jsonify({'error': 'Time não fornecido'}), 400
    gols_fet = df.loc[df['mandante'] == time, "visitante_Placar"].mean() + df.loc[df['visitante'] == time, "mandante_Placar"].mean()
    return jsonify({
        'time': time,
        'Media_gols_sofridos': float(gols_fet)
    })

#media de gols levados(2)
@app.route('/API/med_gols_lev', methods=['GET'])
def med_gols_lev():
    time = request.args.get('time')
    if not time:
        return jsonify({'error': 'Time não fornecido'}), 400

    gols_sofridos = (
        df.loc[df['mandante'] == time, "visitante_Placar"].mean() +
        df.loc[df['visitante'] == time, "mandante_Placar"].mean()
    )

    return jsonify({
        'time': time,
        'Media_gols_sofridos': float(gols_sofridos)
    })
#gols levados(3)
@app.route('/API/gols_lev', methods=['GET'])
def gols_lev():
    time = request.args.get('time')
    if not time:
        return jsonify({'error': 'Time não fornecido'}), 400

    gols_sofridos = (
        df.loc[df['mandante'] == time, "visitante_Placar"].sum() +
        df.loc[df['visitante'] == time, "mandante_Placar"].sum()
    )

    return jsonify({
        'time': time,
        'total_gols_sofridos': int(gols_sofridos)
    })
#derrota(4)
@app.route('/API/derrota', methods=['GET'])
def derrota():
    time = request.args.get('time')
    if not time:
        return jsonify({'error': 'Time nao fornecido'}), 400
       
    derrota = df[(df['mandante'] == time) & (df["mandante_Placar"] < df["visitante_Placar"])].shape[0] + df[(df['visitante']== time) & (df["visitante_Placar"] < df["mandante_Placar"])].shape[0]

    return jsonify({
        'time': time,
        'tota_derrotas': derrota
     })
#vitoria(5)
@app.route('/API/vitoria', methods=['GET'])
def vitoria():
    time = request.args.get('time')
    if not time:
        return jsonify({'error': 'Time nao fornecido'}), 400
       
    vitoria = df[(df['mandante'] == time) & (df["mandante_Placar"] > df["visitante_Placar"])].shape[0] + df[(df['visitante'] == time) & (df["visitante_Placar"] > df["mandante_Placar"])].shape[0]

    return jsonify({
        'time': time,
        'tota_vitoria': vitoria
     })
#empate(6)
@app.route('/API/empate', methods=['GET'])
def empate():
    time = request.args.get('time')
    if not time:
        return jsonify({'error': 'Time nao fornecido'}), 400
       
    empate = df[(df['mandante'] == time) & (df["mandante_Placar"] == df["visitante_Placar"])].shape[0] + df[(df['visitante']== time) & (df["visitante_Placar"] == df["mandante_Placar"])].shape[0]

    return jsonify({
        'time': time,
        'tota_vitoria': empate
     })
#media de vitoria/derrota/empate(7)
@app.route('/API/med_vit', methods=['GET'])
def med_vit():
    time = request.args.get('time')
    if not time:
        return jsonify({'error': 'Time nao fornecido'}), 400
    
    jogos = df[(df['mandante'] == time) | (df['visitante'] == time)].shape[0]   
    med_vit = (df[(df['mandante'] == time) & (df["mandante_Placar"] > df["visitante_Placar"])].shape[0] + df[(df['visitante']== time) & (df["visitante_Placar"] > df["mandante_Placar"])].shape[0]) / jogos
    mid_der = (df[(df['mandante'] == time) & (df["mandante_Placar"] < df["visitante_Placar"])].shape[0] + df[(df['visitante']== time) & (df["visitante_Placar"] < df["mandante_Placar"])].shape[0]) / jogos
    mid_emp = (df[(df['mandante'] == time) & (df["mandante_Placar"] == df["visitante_Placar"])].shape[0] + df[(df['visitante']== time) & (df["visitante_Placar"] == df["mandante_Placar"])].shape[0]) / jogos

    return jsonify({
        'time': time,
        'media_vitoria': med_vit,
        'media_derrota': mid_der,
        'media_empate': mid_emp,

     })
#media de pontos por rebaixamento(8)
@app.route('/API/mpdr', methods=['GET'])
def mpdr():
    # Inicializa o dicionário de pontos
    pontos_por_time = {}

    # Itera sobre as linhas do DataFrame
    for _, row in df.iterrows():
        mandante = row['mandante']
        visitante = row['visitante']

        mandante_pontos = 0
        visitante_pontos = 0

        # Determina os pontos baseados no resultado da partida
        if row['mandante_Placar'] > row['visitante_Placar']:
            mandante_pontos = 3
            visitante_pontos = 0
        elif row['mandante_Placar'] < row['visitante_Placar']:
            mandante_pontos = 0
            visitante_pontos = 3
        else:
            mandante_pontos = 1
            visitante_pontos = 1

        # Armazena os pontos do mandante
        if mandante not in pontos_por_time:
            pontos_por_time[mandante] = []
        pontos_por_time[mandante].append(mandante_pontos)

        # Armazena os pontos do visitante
        if visitante not in pontos_por_time:
            pontos_por_time[visitante] = []
        pontos_por_time[visitante].append(visitante_pontos)

    # Calcula a média de pontos por time
    media_pontos_por_time = {time: sum(pontos) / len(pontos) for time, pontos in pontos_por_time.items()}

    # Ordena os times com base na média de pontos
    media_pontos_ordenada = sorted(media_pontos_por_time.items(), key=lambda x: x[1])

    # Calcula a média de pontos da zona de rebaixamento (últimos 4 times)
    zona_rebaixamento = media_pontos_ordenada[:4]  # Os últimos 4 times
    pontos_zona_rebaixamento = [pontos for _, pontos in zona_rebaixamento]
    media_pontos_zona = sum(pontos_zona_rebaixamento) / len(pontos_zona_rebaixamento)

    # Adiciona a comparação da média de pontos de cada time com a zona de rebaixamento
    comparacao_pontos = {}
    for time, media_pontos in media_pontos_por_time.items():
        comparacao_pontos[time] = {
            'media_pontos_time': round(media_pontos, 2),
            'media_pontos_zona_rebaixamento': round(media_pontos_zona, 2),
            'acima_ou_abaixo': 'acima' if media_pontos > media_pontos_zona else 'abaixo'
        }

    return jsonify(comparacao_pontos)

#formações mais usadas(9)
@app.route('/API/fmu', methods=['GET'])
def fmu():
    formacoes_mandante = df['formacao_mandante'].value_counts()
    formacoes_visitante = df['formacao_visitante'].value_counts()
    formacoes_totais = formacoes_mandante.add(formacoes_visitante, fill_value=0)
    formacoes_ordenadas = formacoes_totais.sort_values(ascending=False)

    # Converte para lista de tuplas ordenadas
    formacoes_lista = list(formacoes_ordenadas.items())

    return jsonify({'formações': formacoes_lista})
### API dos campeos(10)
df['pontos_mandante'] = 0
df['pontos_visitante'] = 0

# Atribuir pontos: 3 pontos para vitória e 1 ponto para empate
for index, jogo in df.iterrows():
    if jogo['vencedor'] == jogo['mandante']:
        df.at[index, 'pontos_mandante'] = 3
        df.at[index, 'pontos_visitante'] = 0
    elif jogo['vencedor'] == jogo['visitante']:
        df.at[index, 'pontos_mandante'] = 0
        df.at[index, 'pontos_visitante'] = 3
    else:  # Empate
        df.at[index, 'pontos_mandante'] = 1
        df.at[index, 'pontos_visitante'] = 1

# Agrupar por ano e time, somando os pontos

df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
df['data'] = pd.to_datetime(df['data'])  # Convert 'data' column to datetime
df['ano'] = df['data'].dt.year 

# Criar um DataFrame com pontos dos mandantes
pontos_mandantes = df.groupby(['ano', 'mandante'])['pontos_mandante'].sum().reset_index()

# Criar um DataFrame com pontos dos visitantes
pontos_visitantes = df.groupby(['ano', 'visitante'])['pontos_visitante'].sum().reset_index()

# Renomear as colunas para facilitar a concatenação
pontos_mandantes.rename(columns={'mandante': 'time', 'pontos_mandante': 'pontos'}, inplace=True)

pontos_visitantes.rename(columns={'visitante': 'time', 'pontos_visitante': 'pontos'}, inplace=True)

# Combinar os pontos dos mandantes e visitantes
pontos_totais = pd.concat([pontos_mandantes, pontos_visitantes])

# Agrupar novamente para somar os pontos por time e ano
pontos_totais = pontos_totais.groupby(['ano', 'time'])['pontos'].sum().reset_index()

# Identificar o campeão de cada ano
campeoes = pontos_totais.loc[pontos_totais.groupby('ano')['pontos'].idxmax()]

### API dos campeos
@app.route('/API/campeoes_A', methods = ['GET'])
def campeoes_A():
    campeoes_json = campeoes.to_dict(orient='records')  
    return jsonify({
        'Campeões': campeoes_json
    })

@app.route('/API/goleadas', methods = ['GET'])
def goleadas():
    time = request.args.get('time')
    if not time:
        return jsonify({'error': 'Time nao fornecido'}), 400
    goleadas = 0
    for _, row in df.iterrows():
         if abs(row['mandante_Placar'] - row['visitante_Placar']) >= 3:
            goleadas += 1
    return jsonify({
         'Quantidade de goleadas no campeonato:': goleadas
    })
@app.route('/API/tmfg', methods = ['GET'])
def tmfg():
    gols_por_time = {}

    for _, row in df.iterrows():
        mandante = row['mandante']
        gols_mandante = row['mandante_Placar']
        if mandante not in gols_por_time:
            gols_por_time[mandante] = 0
        gols_por_time[mandante] += gols_mandante

        visitante = row['visitante']
        gols_visitante = row['visitante_Placar']
        if visitante not in gols_por_time:
            gols_por_time[visitante] = 0
        gols_por_time[visitante] += gols_visitante

    gols_ordenados = sorted(gols_por_time.items(), key=lambda x: x[1], reverse=True)

    return jsonify({
        'os times que mais fizeram gols são': gols_ordenados
    })

@app.route('/API/media-goleadas', methods=['GET'])
def media_goleadas():
     time = request.args.get('time')
     if not time:
        return jsonify({'error': 'Time nao fornecido'}), 400
     total_goleadas = 0
     total_partidas = 0

     for _, row in df.iterrows():
        diferenca = abs(row['mandante_Placar'] - row['visitante_Placar'])
        if diferenca >= 3:
            total_goleadas += 1
        total_partidas += 1
     if total_partidas > 0:
        media_goleadas = total_goleadas / total_partidas
     else:
        media_goleadas = 0  

     print(f"\nMédia de goleadas: {media_goleadas:.2f}")

     return jsonify({
        'media_de_goleadas': round(media_goleadas, 2)
    })

################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################

@app.route('/API/partidarodada', methods=['GET'])
def partidarodada():
    ano = int(request.args.get('ano'))
    time1 = request.args.get('time')
    df_ano = df[df['data'].dt.year == ano]
    pontos_rodada = pd.DataFrame(columns=[ time1])
    for rodada in df_ano['rodata'].unique():
        jogos_rodada = df_ano[df_ano['rodata'] == rodada]
        situ = ''    
        for _, jogo in jogos_rodada.iterrows():
            if jogo['vencedor'] == time1:
                situ = 'vitoria'
            elif jogo['mandante'] == time1 and jogo['mandante_Placar'] < jogo['visitante_Placar']:
                situ = 'derrota'    
            elif jogo['visitante'] == time1 and jogo['mandante_Placar'] > jogo['visitante_Placar']:
                situ = 'derrota'
            elif jogo['mandante'] == time1 and jogo['mandante_Placar'] == jogo['visitante_Placar']:
             situ = 'empate'
            elif jogo['visitante'] == time1 and jogo['mandante_Placar'] == jogo['visitante_Placar']:
                  situ = 'empate'
           # else:      TENTAR MAIS TARDE 'TIME NÃO PRESENTE NA SÉRIE A' 
               # if jogo['vencedor'] != time1 or jogo['mandante'] != time1 or jogo['visitante'] != time1:
               #     situ = 'Time nao presente na serie A'

        nova_linha = pd.DataFrame([{
            'ano': ano,
            'Rodada': rodada,
            time1: situ 
        }])
        pontos_rodada = pd.concat([pontos_rodada, nova_linha], ignore_index=True)

    return jsonify(pontos_rodada.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)


