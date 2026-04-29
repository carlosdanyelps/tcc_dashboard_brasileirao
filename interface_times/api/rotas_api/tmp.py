from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# =========================
# CARREGAR DADOS
# =========================
df = pd.read_csv('campeonato-brasileiro-full.csv')

# =========================
# GARANTIR TIPOS
# =========================
df['mandante_Placar'] = pd.to_numeric(df['mandante_Placar'], errors='coerce')
df['visitante_Placar'] = pd.to_numeric(df['visitante_Placar'], errors='coerce')


# =========================
# FUNÇÃO: CLASSIFICAÇÃO
# =========================
def gerar_classificacao(df_filtrado):
    
    mandante = pd.DataFrame({
        'time': df_filtrado['mandante'],
        'gols_pro': df_filtrado['mandante_Placar'],
        'gols_contra': df_filtrado['visitante_Placar']
    })

    visitante = pd.DataFrame({
        'time': df_filtrado['visitante'],
        'gols_pro': df_filtrado['visitante_Placar'],
        'gols_contra': df_filtrado['mandante_Placar']
    })

    tabela = pd.concat([mandante, visitante], ignore_index=True)

    tabela['vitoria'] = (tabela['gols_pro'] > tabela['gols_contra']).astype(int)
    tabela['empate'] = (tabela['gols_pro'] == tabela['gols_contra']).astype(int)
    tabela['derrota'] = (tabela['gols_pro'] < tabela['gols_contra']).astype(int)

    tabela['pontos'] = tabela['vitoria'] * 3 + tabela['empate']

    classificacao = tabela.groupby('time').agg({
        'pontos': 'sum',
        'vitoria': 'sum',
        'empate': 'sum',
        'derrota': 'sum',
        'gols_pro': 'sum',
        'gols_contra': 'sum'
    }).reset_index()

    classificacao['saldo'] = classificacao['gols_pro'] - classificacao['gols_contra']

    classificacao = classificacao.sort_values(
        by=['pontos', 'vitoria', 'saldo', 'gols_pro'],
        ascending=[False, False, False, False]
    )

    classificacao['posicao'] = range(1, len(classificacao) + 1)

    return classificacao


# =========================
# FUNÇÃO: RODADA A RODADA
# =========================
def classificacao_por_rodada(df, temporada_desejada):
    
    df_temp = df[df['temporada_corrigida'] == temporada_desejada].copy()

    if df_temp.empty:
        return None

    df_temp = df_temp.sort_values(by=['rodata_corrigida'])

    rodadas = sorted(df_temp['rodata_corrigida'].dropna().unique())

    resultados = []

    for rodada in rodadas:
        
        df_rodada = df_temp[df_temp['rodata_corrigida'] <= rodada]

        classificacao = gerar_classificacao(df_rodada)
        classificacao['rodada'] = int(rodada)
        classificacao['temporada'] = int(temporada_desejada)

        resultados.append(classificacao)

    tabela_final = pd.concat(resultados, ignore_index=True)

    return tabela_final


# =========================
# ROTA PRINCIPAL
# =========================
@app.route('/classificacao', methods=['GET'])
def get_classificacao():
    
    temporada = request.args.get('temporada', type=int)

    if not temporada:
        return jsonify({'erro': 'Informe a temporada. Ex: /classificacao?temporada=2003'}), 400

    tabela = classificacao_por_rodada(df, temporada)

    if tabela is None:
        return jsonify({'erro': f'Temporada {temporada} não encontrada'}), 404

    return jsonify(tabela.to_dict(orient='records'))


# =========================
# RODAR API
# =========================
if __name__ == '__main__':
    app.run(debug=True)