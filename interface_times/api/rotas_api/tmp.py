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

# limpar dados
df = df.dropna(subset=['mandante_Placar', 'visitante_Placar'])

# cache
cache = {}

def classificacao_por_rodada(df, ano_desejado):

    if ano_desejado in cache:
        return cache[ano_desejado]

    df_temp = df[df['temporada_corrigida'] == ano_desejado].copy()

    if df_temp.empty:
        return None

    col_rodada = 'rodata_corrigida' if 'rodata_corrigida' in df.columns else 'rodata'

    df_temp = df_temp.sort_values(by=[col_rodada])
    rodadas = sorted(df_temp[col_rodada].dropna().unique())

    resultados = []

    for rodada in rodadas:
        df_rodada = df_temp[df_temp[col_rodada] <= rodada]

        classificacao = gerar_classificacao(df_rodada)
        classificacao['rodada'] = int(rodada)
        classificacao['temporada'] = int(ano_desejado)

        resultados.append(classificacao)

    tabela_final = pd.concat(resultados, ignore_index=True)

    cache[ano_desejado] = tabela_final

    return tabela_final

# =========================
# ROTA PRINCIPAL
# =========================
@app.route('/classificacao', methods=['GET'])
def get_classificacao():
    
    ano = request.args.get('ano', type=int)

    if not ano:
        return jsonify({'erro': 'Informe o ano. Ex: /classificacao?ano=2003'}), 400

    tabela = classificacao_por_rodada(df, ano)

    if tabela is None:
        return jsonify({'erro': f'Ano {ano} não encontrado'}), 404

    return jsonify(tabela.to_dict(orient='records'))


# =========================
# RODAR API
# =========================
if __name__ == '__main__':
    app.run(debug=True)