import pandas as pd
df = pd.read_csv('campeonato-brasileiro-full.csv')


#2 média de vitória/derrotas/empates
def vitoria():
    time = input('Selecione um time: ')
    vitoria = df[(df['mandante'] == time) & (df["mandante_Placar"] > df["visitante_Placar"])].shape[0]
    print(f'O {time} venceu {vitoria} vezes em toda a sua passagem na série A do Brasileirão')


def derrota():
    time = input('Selecione um time: ')
    derrota = df[(df['mandante'] == time) & (df["mandante_Placar"] < df["visitante_Placar"])].shape[0] & df[(df['visitante']== time) & (df["visitante_Placar"] < df["mandante_Placar"])].shape[0]
    print(f'O {time} perdeu {derrota} vezes em toda a sua passagem na série A do Brasileirão')

def empate():
  time = input('Selecione um time:')
  empate = df[(df['mandante'] == time) & (df["mandante_Placar"] == df["visitante_Placar"])].shape[0] + df[(df['visitante']== time) & (df["visitante_Placar"] == df["mandante_Placar"])].shape[0]
  print(f'O {time} empatou {empate} vezes em toda a sua passagem na série A do Brasileirão')


def mediavde():
  time = input('Selecione um time:')
  #jogos agora recebe o número de jogos, e não a tupla da dimensão do DataFrame
  jogos = df[(df['mandante'] == time) | (df['visitante'] == time)].shape[0] # Changed & to | to count all games where the team was either 'mandante' or 'visitante'

  # adicionado parênteses para realizar a soma antes da divisão
  mid_vit = (df[(df['mandante'] == time) & (df["mandante_Placar"] > df["visitante_Placar"])].shape[0] + df[(df['visitante']== time) & (df["visitante_Placar"] > df["mandante_Placar"])].shape[0]) / jogos
  print(f'O {time} tem uma media de {mid_vit} vitórias em toda a sua passagem na série A do Brasileirão')

  # corrigido 'Visitante' para 'visitante' e adicionado parênteses para realizar a soma antes da divisão
  mid_der = (df[(df['mandante'] == time) & (df["mandante_Placar"] < df["visitante_Placar"])].shape[0] + df[(df['visitante']== time) & (df["visitante_Placar"] < df["mandante_Placar"])].shape[0]) / jogos
  print(f'O {time} tem uma media de {mid_der} derrotas em toda a sua passagem na série A do Brasileirão')

  # adicionado parênteses para realizar a soma antes da divisão
  mid_emp = (df[(df['mandante'] == time) & (df["mandante_Placar"] == df["visitante_Placar"])].shape[0] + df[(df['visitante']== time) & (df["visitante_Placar"] == df["mandante_Placar"])].shape[0]) / jogos
  print(f'O {time} tem uma media de {mid_emp} empates em toda a sua passagem na série A do Brasileirão')

#7 média de pontos, para zona de rebaixamento
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
media_pontos_zona_rebaixamento()