import pandas as pd
df = pd.read_csv('campeonato-brasileiro-full.csv')

def comparacao_time():
    time1 = input('informe o time 1: ')
    time2 = input('Informe o time 2: ')
    vitorias = {time1: 0, time2: 0}
    gols = {time1: 0, time2: 0}
    jogos_encontrados = 0
    empates = 0

    for _, row in df.iterrows():
        mandante = row['mandante']
        visitante = row['visitante']
        gols_mandante = row['mandante_Placar']
        gols_visitante = row['visitante_Placar']

        # Confirma que jogo é entre os dois times
        if set([mandante, visitante]) == set([time1, time2]):
            jogos_encontrados += 1

            # Contabiliza gols corretamente
            gols[mandante] += gols_mandante
            gols[visitante] += gols_visitante

            # Conta vitórias
            if gols_mandante > gols_visitante:
                vitorias[mandante] += 1
            elif gols_visitante > gols_mandante:
                vitorias[visitante] += 1
            else:
                empates += 1

            
        if set([visitante, mandante ]) == set([time1, time2]):
            jogos_encontrados += 1

            # Contabiliza gols corretamente
            gols[mandante] += gols_mandante
            gols[visitante] += gols_visitante

            # Conta vitórias
            if gols_mandante > gols_visitante:
                vitorias[mandante] += 1
            elif gols_visitante > gols_mandante:
                vitorias[visitante] += 1
            else:
                empates += 1

    if jogos_encontrados == 0:
        print(f"Nenhum jogo encontrado entre {time1} e {time2}.")
        return

    print(f"Jogos entre {time1} e {time2}: {jogos_encontrados}")
    print(f"Vitórias de {time1}: {vitorias[time1]}")
    print(f"Vitórias de {time2}: {vitorias[time2]}")
    print(f"Gols de {time1}: {gols[time1]}")
    print(f"Gols de {time2}: {gols[time2]}")
    print(f"Empates {empates}")

    if vitorias[time1] > vitorias[time2]:
        print(f"{time1} venceu mais partidas.")
    elif vitorias[time2] > vitorias[time1]:
        print(f"{time2} venceu mais partidas.")
    else:
        print("Os dois times venceram a mesma quantidade de partidas.")

    if gols[time1] > gols[time2]:
        print(f"{time1} fez mais gols.")
    elif gols[time2] > gols[time1]:
        print(f"{time2} fez mais gols.")
    else:
        print("Os dois times marcaram a mesma quantidade de gols.")

comparacao_time()