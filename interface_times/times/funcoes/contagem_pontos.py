from backendtime import *


#3 campeões
# Criar uma nova coluna para armazenar os pontos
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

# Exibir os campeões
print(campeoes)

