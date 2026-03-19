import pandas as pd
df = pd.read_csv('campeonato-brasileiro-full.csv')

def desempenho_time(df, time, ano):
    
    # Filtra jogos do time no ano
    df_ano = df[df["data"].dt.year == ano]
    jogos = df_ano[(df_ano["mandante"] == time) | (df_ano["visitante"] == time)]

    PJ = len(jogos)

    # vitórias do time
    VIT = (
        ((jogos["mandante"] == time) & (jogos["mandante_Placar"] > jogos["visitante_Placar"])) |
        ((jogos["visitante"] == time) & (jogos["visitante_Placar"] > jogos["mandante_Placar"]))
    ).sum()

    # empates
    E = (jogos["mandante_Placar"] == jogos["visitante_Placar"]).sum()

    # derrotas
    DER = PJ - VIT - E

    # gols marcados
    GM = (
        jogos.loc[jogos["mandante"] == time, "mandante_Placar"].sum() +
        jogos.loc[jogos["visitante"] == time, "visitante_Placar"].sum()
    )

    # gols sofridos
    GC = (
        jogos.loc[jogos["mandante"] == time, "visitante_Placar"].sum() +
        jogos.loc[jogos["visitante"] == time, "mandante_Placar"].sum()
    )

    SG = GM - GC

    # pontos (3 por vitória + 1 por empate)
    Pts = VIT * 3 + E * 1

    return {
        "Pts": Pts,
        "PJ": PJ,
        "VIT": VIT,
        "E": E,
        "DER": DER,
        "GM": GM,
        "GC": GC,
        "SG": SG
    }

def tabela_ano(df, ano):
    # pega todos os times que apareceram no ano
    df_ano = df[df["data"].dt.year == ano]
    times = pd.unique(df_ano[["mandante", "visitante"]].values.ravel())

    tabela = []
    for time in times:
        desempenho = desempenho_time(df, time, ano)
        desempenho["Time"] = time
        tabela.append(desempenho)

    tabela_df = pd.DataFrame(tabela)

    # organiza colunas e ordena por pontos, saldo, vitórias
    tabela_df = tabela_df[["Time", "Pts", "PJ", "VIT", "E", "DER", "GM", "GC", "SG"]]
    tabela_df = tabela_df.sort_values(by=["Pts", "SG", "VIT"], ascending=[False, False, False]).reset_index(drop=True)

    return tabela_df


def desempenho_time(df, time, ano):
    df_ano = df[df["data"].dt.year == ano]
    jogos = df_ano[(df_ano["mandante"] == time) | (df_ano["visitante"] == time)]

    PJ = len(jogos)

    VIT = (
        ((jogos["mandante"] == time) & (jogos["mandante_Placar"] > jogos["visitante_Placar"])) |
        ((jogos["visitante"] == time) & (jogos["visitante_Placar"] > jogos["mandante_Placar"]))
    ).sum()

    E = (jogos["mandante_Placar"] == jogos["visitante_Placar"]).sum()
    DER = PJ - VIT - E

    GM = (
        jogos.loc[jogos["mandante"] == time, "mandante_Placar"].sum() +
        jogos.loc[jogos["visitante"] == time, "visitante_Placar"].sum()
    )

    GC = (
        jogos.loc[jogos["mandante"] == time, "visitante_Placar"].sum() +
        jogos.loc[jogos["visitante"] == time, "mandante_Placar"].sum()
    )

    SG = GM - GC
    Pts = VIT * 3 + E

    return {"Pts": Pts, "PJ": PJ, "VIT": VIT, "E": E, "DER": DER, "GM": GM, "GC": GC, "SG": SG}
def tabela_ano(df, ano):
    df_ano = df[df["data"].dt.year == ano]
    times = pd.unique(df_ano[["mandante", "visitante"]].values.ravel())

    tabela = []
    for time in times:
        desempenho = desempenho_time(df, time, ano)
        desempenho["Time"] = time
        tabela.append(desempenho)

    tabela_df = pd.DataFrame(tabela)
    tabela_df = tabela_df[["Time", "Pts", "PJ", "VIT", "E", "DER", "GM", "GC", "SG"]]
    tabela_df = tabela_df.sort_values(by=["Pts", "SG", "VIT"], ascending=[False, False, False]).reset_index(drop=True)
    tabela_df["Pos"] = tabela_df.index + 1  # posição na tabela

    return tabela_df

def historico_time(df, time):
    anos = sorted(df[(df["mandante"] == time) | (df["visitante"] == time)]["data"].dt.year.unique())
    historico = []

    for ano in anos:
        tabela = tabela_ano(df, ano)
        linha_time = tabela[tabela["Time"] == time].iloc[0].to_dict()
        linha_time["Ano"] = ano
        historico.append(linha_time)

    historico_df = pd.DataFrame(historico)
    historico_df = historico_df[["Ano", "Pos", "Pts", "PJ", "VIT", "E", "DER", "GM", "GC", "SG"]]
    return historico_df

df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")

# Escolha do time e ano via input
time = input("Informe o nome do time: ").strip()
ano = int(input("Informe o ano (ex: 2022): "))

# Validação básica
if time not in df["mandante"].unique() and time not in df["visitante"].unique():
    print(f"Time '{time}' não encontrado no DataFrame.")
else:
    # Desempenho no ano
    print("\n--- DESEMPENHO DO TIME NO ANO ---")
    resumo = desempenho_time(df, time, ano)
    print(resumo)

    # Tabela do ano
    print("\n--- TABELA DO CAMPEONATO NO ANO ---")
    print(tabela_ano(df, ano))

    # Histórico completo
    print("\n--- HISTÓRICO DO TIME EM TODOS OS ANOS ---")
    print(historico_time(df, time))
