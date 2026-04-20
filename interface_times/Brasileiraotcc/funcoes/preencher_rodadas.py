import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# =========================
# CARREGAR DADOS
# =========================
df = pd.read_csv('campeonato-brasileiro-full.csv')

# =========================
# TRATAR DATAS
# =========================
import pandas as pd
import numpy as np

# =========================
# CARREGAR DADOS
# =========================
df = pd.read_csv('campeonato-brasileiro-full.csv')

# =========================
# TRATAR DATAS
# =========================
df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')
df['ano_civil'] = df['data'].dt.year

print("=" * 80)
print("PREENCHIMENTO DE RODADAS USANDO ORDEM REAL DOS JOGOS")
print("=" * 80)

# =========================
# DEFINIR TEMPORADAS CORRETAS
# =========================
def definir_temporada(data):
    if pd.isna(data):
        return np.nan

    # Temporada 2020 (08/08/2020 → 25/02/2021)
    if pd.to_datetime('2020-08-08') <= data <= pd.to_datetime('2021-02-25'):
        return 2020

    # Temporada 2021 (29/05/2021 → 09/12/2021)
    elif pd.to_datetime('2021-05-29') <= data <= pd.to_datetime('2021-12-09'):
        return 2021

    # Temporadas normais
    else:
        return data.year


df['temporada'] = df['data'].apply(definir_temporada)

# =========================
# ANÁLISE INICIAL
# =========================
print("\n1. SITUAÇÃO INICIAL:")
for temp in sorted(df['temporada'].dropna().unique()):
    df_temp = df[df['temporada'] == temp]
    total = len(df_temp)
    vazias = df_temp['rodata'].isna().sum()
    print(f"   Temporada {temp}: {total - vazias} preenchidas, {vazias} vazias (total {total})")

# =========================
# CALCULAR RODADAS POR ORDEM REAL
# =========================
df_preenchido = df.copy()
df_preenchido['rodata_calculada'] = np.nan

for temporada in sorted(df_preenchido['temporada'].dropna().unique()):
    
    df_temp = df_preenchido[df_preenchido['temporada'] == temporada].copy()
    
    # Ordenar por data
    df_temp = df_temp.sort_values(by=['data'])
    
    # Criar sequência de jogos
    df_temp['ordem_jogo'] = range(len(df_temp))
    
    # Cada 10 jogos = 1 rodada
    df_temp['rodata_calc'] = (df_temp['ordem_jogo'] // 10) + 1
    
    # Limitar a 38 rodadas
    df_temp['rodata_calc'] = df_temp['rodata_calc'].clip(upper=38)
    
    # Atualizar dataframe principal
    df_preenchido.loc[df_temp.index, 'rodata_calculada'] = df_temp['rodata_calc']

# =========================
# COMBINAR COM DADOS ORIGINAIS
# =========================
df_preenchido['rodata_final'] = df_preenchido['rodata']

mask = df_preenchido['rodata_final'].isna()
df_preenchido.loc[mask, 'rodata_final'] = df_preenchido.loc[mask, 'rodata_calculada']

# Substituir coluna final
df_preenchido['rodata'] = df_preenchido['rodata_final']

# =========================
# RESULTADOS
# =========================
print("\n2. RESULTADO FINAL:")
for temp in sorted(df_preenchido['temporada'].dropna().unique()):
    df_temp = df_preenchido[df_preenchido['temporada'] == temp]
    
    print(f"\n   Temporada {temp}:")
    print(f"      Jogos: {len(df_temp)}")
    print(f"      Rodadas: {df_temp['rodata'].min()} a {df_temp['rodata'].max()}")
    print(f"      Vazios restantes: {df_temp['rodata'].isna().sum()}")

# =========================
# ANÁLISE ESPECÍFICA 2020/2021
# =========================
print("\n" + "=" * 80)
print("ANÁLISE DA TEMPORADA 2020 (ATRAVESSANDO 2021)")
print("=" * 80)

df_2020 = df_preenchido[df_preenchido['temporada'] == 2020]

if len(df_2020) > 0:
    print(f"\nTotal de jogos: {len(df_2020)}")
    print(f"Rodadas: {df_2020['rodata'].min()} a {df_2020['rodata'].max()}")
    print(f"Data: {df_2020['data'].min()} até {df_2020['data'].max()}")

print("\n" + "=" * 80)
print("ANÁLISE DA TEMPORADA 2021")
print("=" * 80)

df_2021 = df_preenchido[df_preenchido['temporada'] == 2021]

if len(df_2021) > 0:
    print(f"\nTotal de jogos: {len(df_2021)}")
    print(f"Rodadas: {df_2021['rodata'].min()} a {df_2021['rodata'].max()}")
    print(f"Data: {df_2021['data'].min()} até {df_2021['data'].max()}")

# =========================
# SALVAR ARQUIVO FINAL
# =========================
df_preenchido.to_csv('campeonato-brasileiro-full_preenchido.csv', index=False)

print("\n✓ Arquivo salvo como: campeonato-brasileiro-full_preenchido.csv")