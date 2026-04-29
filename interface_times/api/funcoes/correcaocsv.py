import pandas as pd

# =========================
# CARREGAR DADOS
# =========================
df = pd.read_csv('campeonato-brasileiro-full.csv')

# =========================
# GARANTIR DATETIME
# =========================
df['data'] = pd.to_datetime(df['data'], errors='coerce')

# =========================
# CRIAR ANO CIVIL BASEADO NA DATA
# =========================
df['ano_data'] = df['data'].dt.year

# =========================
# CORRIGIR TEMPORADA
# =========================
def corrigir_temporada(row):
    ano = row['ano_data']
    
    # manter anos problemáticos
    if ano in [2020, 2021]:
        return row['temporada']
    
    # corrigir anos normais
    if ano >= 2022:
        return ano
    
    # anos antigos (já estão corretos)
    return row['temporada']

df['temporada_corrigida'] = df.apply(corrigir_temporada, axis=1)

# =========================
# OPCIONAL: CORRIGIR COLUNA 'temporada' TAMBÉM
# =========================
df['temporada'] = df['temporada_corrigida']

# =========================
# REMOVER COLUNA AUXILIAR
# =========================
df.drop(columns=['ano_data'], inplace=True)

# =========================
# SALVAR NOVO CSV
# =========================
df.to_csv('campeonato-brasileiro-corrigido.csv', index=False)

print("Correção concluída!")