import pandas as pd
df = pd.read_csv('campeonato-brasileiro-full.csv')

df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
ano = int(input('Selecione o ano: '))
# Filtrar os dados para o ano
df_ano = df[df['data'].dt.year == ano]
# Definir os times
time1 = input('Selecione um time ')

# Criar um DataFrame para armazenar os pontos por rodada
pontos_rodada = pd.DataFrame(columns=['Rodada', time1])
# Iterar sobre as rodadas
for rodada in df_ano['rodata'].unique():
    # Filtrar os jogos da rodada
    jogos_rodada = df_ano[df_ano['rodata'] == rodada]

    # Inicializar pontos
    situ = ''    

    for _, jogo in jogos_rodada.iterrows():
        # Verificar vitória do time1
        if jogo['vencedor'] == time1:
            situ = 'vitória'
        elif jogo['mandante'] == time1 and jogo['mandante_Placar'] == jogo['visitante_Placar']:
            situ = 'empate'
        elif jogo['visitante'] == time1 and jogo['mandante_Placar'] == jogo['visitante_Placar']:
            situ = 'empate'
    # Verificar vitória do time2
    # Adicionar os pontos ao DataFrame (usando concat)
    nova_linha = pd.DataFrame([{
        'Rodada': rodada,
        time1: situ
    }])

    # Concatenar a nova linha com o DataFrame existente
    pontos_rodada = pd.concat([pontos_rodada, nova_linha], ignore_index=True)

# Exibir o DataFrame resultante
print(pontos_rodada)
