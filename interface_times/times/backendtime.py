import pandas as pd
from flask import Flask


df = pd.read_csv('campeonato-brasileiro-full.csv')

#7 média de pontos, para zona de rebaixamento@
def media_pontos_zona_rebaixamento():
    pontos_por_time = {}


    for _, row in df.iterrows():

        mandante = row['mandante']
        visitante = row['visitante']

        mandante_pontos = 0
        visitante_pontos = 0


        if row['mandante_Placar'] > row['visitante_Placar']:
            mandante_pontos = 3
            visitante_pontos = 0
        elif row['mandante_Placar'] < row['visitante_Placar']:
            mandante_pontos = 0
            visitante_pontos = 3
        else:
            mandante_pontos = 1
            visitante_pontos = 1


        if mandante not in pontos_por_time:
            pontos_por_time[mandante] = []
        pontos_por_time[mandante].append(mandante_pontos)

        if visitante not in pontos_por_time:
            pontos_por_time[visitante] = []
        pontos_por_time[visitante].append(visitante_pontos)


    media_pontos_por_time = {time: sum(pontos) / len(pontos) for time, pontos in pontos_por_time.items()}

    media_pontos_ordenada = sorted(media_pontos_por_time.items(), key=lambda x: x[1])
    zona_rebaixamento = media_pontos_ordenada[:4]

    pontos_zona_rebaixamento = [pontos for time, pontos in zona_rebaixamento]
    media_pontos_zona = sum(pontos_zona_rebaixamento) / len(pontos_zona_rebaixamento)

    # Exibindo o resultado
    print(f"\nMédia de pontos dos times na zona de rebaixamento: {media_pontos_zona:.2f} pontos")


# Carrega os dados do CSV
df = pd.read_csv('campeonato-brasileiro-full.csv')

def contar_goleadas(time):
    # Verifica se o time existe no DataFrame
    if time not in df['mandante'].unique() and time not in df['visitante'].unique():
        print(f'O time {time} não foi encontrado no dataset.')
        return

    # Goleadas - calculando quando o time tomou mais de 3 gols de diferença
    goleadas = 0
    for index, row in df.iterrows():
        if row['mandante'] == time:
            # Goleada sofrida jogando em casa
            if row['visitante_Placar'] - row['mandante_Placar'] > 3:
                goleadas += 1
        elif row['visitante'] == time:
            # Goleada sofrida jogando fora de casa
            if row['mandante_Placar'] - row['visitante_Placar'] > 3:
                goleadas += 1
    
    print(f'O {time} sofreu {goleadas} goleadas em toda a sua passagem na série A do Brasileirão.')

# Função para interagir com o usuário
def main():
    time = input('Selecione um time: ')
    contar_goleadas(time)

# Executa a função principal
if __name__ == "__main__":
    main()

def biggest_defeats():

    if not all(col in df.columns for col in ['mandante', 'visitante', 'mandante_Placar', 'visitante_Placar']):
        print("Error: Required columns not found in the DataFrame.")
        return

    goleadas_df = pd.DataFrame(columns=['Time', 'Adversário', 'Placar'])

    for index, row in df.iterrows():
      mandante_gols = row['mandante_Placar']
      visitante_gols = row['visitante_Placar']
      diferenca_gols_mandante = abs(mandante_gols - visitante_gols)

      if diferenca_gols_mandante >= 3:

          if mandante_gols > visitante_gols:
                goleadas_df = pd.concat([goleadas_df, pd.DataFrame({'Time': [row['visitante']], 'Adversário': [row['mandante']], 'Placar': [f"{visitante_gols}x{mandante_gols}"]})], ignore_index=True)
          else:
              goleadas_df = pd.concat([goleadas_df, pd.DataFrame({'Time': [row['mandante']], 'Adversário': [row['visitante']], 'Placar': [f"{mandante_gols}x{visitante_gols}"]})], ignore_index=True)


    print(goleadas_df)


#17@

def quantidade_goleadas():
  goleadas = 0
  for _, row in df.iterrows():
     if abs(row['mandante_Placar'] - row['visitante_Placar']) >= 3:
            goleadas += 1

 #print(f"\nQuantidade de goleadas no campeonato: {goleadas}")

#26 times_que_mais_fizeram_gols

def times_que_mais_fizeram_gols():
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
    print("\nTimes que mais fizeram gols:")
    for time, gols in gols_ordenados:
        print(f"{time}: {gols} gols")



#30

#33
'''def tecnicos_com_mais_partidas():
    partidas_por_tecnico = {}
    for _, row in df.iterrows():
        # Contabilizando partidas do técnico do mandante
        tecnico_mandante = row['tecnico_mandante']
        if tecnico_mandante not in partidas_por_tecnico:
            partidas_por_tecnico[tecnico_mandante] = 0
        partidas_por_tecnico[tecnico_mandante] += 1

        # Contabilizando partidas do técnico do visitante
        tecnico_visitante = row['tecnico_visitante']
        if tecnico_visitante not in partidas_por_tecnico:
            partidas_por_tecnico[tecnico_visitante] = 0
        partidas_por_tecnico[tecnico_visitante] += 1

    # Ordenando os técnicos pelo número de partidas em ordem decrescente
    partidas_ordenadas = sorted(partidas_por_tecnico.items(), key=lambda x: x[1], reverse=True)

    print("\nTécnicos com mais partidas:")
    for tecnico, partidas in partidas_ordenadas:
        print(f"{tecnico}: {partidas} partidas")'''




#regioes vitorias
sul = ['PR', 'SC', 'RS']
norte = ['AM','RR', 'AC', 'RO', 'PA', 'AP', 'TO']
centro_oeste = ['MS', 'MT', 'GO']
sudeste = ['SP','RJ','ES','MG']
nordeste = ['BA','PE','AL','SG','PA', 'RN','CE','MA']

def vitorias_por_regiao():
  msul = df['mandante_Estado'].isin(sul)
  mnorte = df['mandante_Estado'].isin(norte)
  mcentro_oeste = df['mandante_Estado'].isin(centro_oeste)
  msudeste = df['mandante_Estado'].isin(sudeste)
  mnordeste = df['mandante_Estado'].isin(nordeste)

  vsul = df['visitante_Estado'].isin(sul)
  vnorte = df['visitante_Estado'].isin(norte)
  vcentro_oeste = df['visitante_Estado'].isin(centro_oeste)
  vsudeste = df['visitante_Estado'].isin(sudeste)
  vnordeste = df['visitante_Estado'].isin(nordeste)

  # Filter for games where the home team from 'sul' won
  sulv = df[(msul) & (df['mandante_Placar'] > df['visitante_Placar'])].shape[0] + df[(vsul) & (df['visitante_Placar'] > df['mandante_Placar'])].shape[0]
  print(f'A região sul teve {sulv} vitórias')
  nortev = df[(mnorte) & (df['mandante_Placar'] > df['visitante_Placar'])].shape[0] + df[(vnorte) & (df['visitante_Placar'] > df['mandante_Placar'])].shape[0]
  print(f'A região norte teve {nortev} vitórias')
  nordestev = df[(mnordeste) & (df['mandante_Placar'] > df['visitante_Placar'])].shape[0] + df[(vnordeste) & (df['visitante_Placar'] > df['mandante_Placar'])].shape[0]
  print(f'A região nordeste teve {nordestev} vitórias')
  sudestev = df[(msudeste) & (df['mandante_Placar'] > df['visitante_Placar'])].shape[0] + df[(vsudeste) & (df['visitante_Placar'] > df['mandante_Placar'])].shape[0]
  print(f'A região sudeste teve {sudestev} vitórias')
  centrooestev = df[(mcentro_oeste) & (df['mandante_Placar'] > df['visitante_Placar'])].shape[0] + df[(vcentro_oeste) & (df['visitante_Placar'] > df['mandante_Placar'])].shape[0]
vitorias_por_regiao()


def regiao(mandante_estado):
    if mandante_estado in ['PR', 'SC', 'RS']:
        return 'sul'
    elif mandante_estado in ['AM', 'RR', 'AC', 'RO', 'PA', 'AP', 'TO']:
        return 'norte'
    elif mandante_estado in ['MS', 'MT', 'GO']:
        return 'centro_oeste'
    elif mandante_estado in ['SP', 'RJ', 'ES', 'MG']:
        return 'sudeste'
    elif mandante_estado in ['BA', 'PE', 'AL', 'SG', 'PA', 'RN', 'CE', 'MA']:
        return 'nordeste'


# Aplicando a função 'regiao' tanto na coluna 'mandante_Estado' quanto na coluna 'visitante_Estado'
#df['mandante_Estado'] = df['mandante_Regiao'].apply(regiao)
#print(df.head(30))
#df['visitante_Regiao'] = df['visitante_Estado'].apply(regiao)

#caçar time regiao
def caca():
    global time_sul, time_norte, time_nordeste, time_sudeste, time_centro_oeste

    time_sul = df[(df['mandante_Regiao'] == 'sul') & (df['visitante_Regiao'] == 'sul')]

    time_norte = df[(df['mandante_Regiao'] == 'norte') & (df['visitante_Regiao'] == 'norte')]

    time_nordeste = df[(df['mandante_Regiao'] == 'nordeste') & (df['visitante_Regiao'] == 'nordeste')]

    time_sudeste = df[(df['mandante_Regiao'] == 'sudeste') & (df['visitante_Regiao'] == 'sudeste')]

    time_centro_oeste = df[(df['mandante_Regiao'] == 'centro_oeste') & (df['visitante_Regiao'] == 'centro_oeste')]

def tcmgr():
  global df  # Declare df as global to modify the global DataFrame
  df = df[(df['mandante'] == 'mandante_Regiao') & (df['mandante_Placar'] == "sul")]
  print(df.head(30))

