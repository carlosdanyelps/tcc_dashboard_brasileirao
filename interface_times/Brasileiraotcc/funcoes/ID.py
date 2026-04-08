import pandas as pd


df = pd.read_csv('campeonato-brasileiro-full.csv')

def adicionar_ids(df):
    todos_times = pd.concat([df["mandante"], df["visitante"]]).unique()
    time_para_id = {time: i + 1 for i, time in enumerate(todos_times)}

    df["mandante_id"] = df["mandante"].map(time_para_id)
    df["visitante_id"] = df["visitante"].map(time_para_id)

    return df

###############################
# campeoes ####################
###############################
df['mandante_Placar'] = pd.to_numeric(df['mandante_Placar'], errors='coerce')
df['visitante_Placar'] = pd.to_numeric(df['visitante_Placar'], errors='coerce')

# Pontos
df['pontos_m'] = (df['mandante_Placar'] > df['visitante_Placar']) * 3 + \
                 (df['mandante_Placar'] == df['visitante_Placar']) * 1

df['pontos_v'] = (df['visitante_Placar'] > df['mandante_Placar']) * 3 + \
                 (df['visitante_Placar'] == df['mandante_Placar']) * 1
                 
