from backendtime import *

def tecnicos_com_mais_partidas():
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
        print(f"{tecnico}: {partidas} partidas")

tecnicos_com_mais_partidas()