import pandas as pd
from flask import Flask

df = pd.read_csv('campeonato-brasileiro-full.csv')

#17@

def quantidade_goleadas():
  goleadas = 0
  for _, row in df.iterrows():
     if abs(row['mandante_Placar'] - row['visitante_Placar']) >= 3:
            goleadas += 1

  print(f"\nQuantidade de goleadas no campeonato: {goleadas}")

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

