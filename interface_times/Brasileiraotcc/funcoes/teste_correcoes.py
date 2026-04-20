"""
SCRIPT DE TESTE - VALIDAÇÃO DAS CORREÇÕES
==========================================

Este script valida que as correções foram aplicadas corretamente
"""

import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

try:
    from interface_times.Brasileiraotcc.funcoes.campeoes import obter_campeao, obter_todos_campeoes, tabela_temporada
    print("✓ Funções de campeões carregadas com sucesso")
except Exception as e:
    print(f"✗ Erro ao carregar funções: {e}")
    sys.exit(1)

print("\n" + "=" * 80)
print("TESTE 1: VALIDAR MAPEAMENTO DE TEMPORADAS")
print("=" * 80)

# Carregar CSV
df = pd.read_csv('funcoes/campeonato-brasileiro-full.csv')
df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')
df['ano_civil'] = df['data'].dt.year

# Definir temporada (mesma lógica que em campeoes.py)
def definir_temporada(row):
    if pd.isna(row['rodata']):
        return row['ano_civil']
    
    rodata = row['rodata']
    ano_civil = row['ano_civil']
    
    if ano_civil == 2021 and rodata >= 28.0:
        return 2020
    if ano_civil == 2020 and 1.0 <= rodata <= 27.0:
        return 2020
    
    return ano_civil

df['temporada'] = df.apply(definir_temporada, axis=1)

# Verificar 2020/2021
dados_2020 = df[df['temporada'] == 2020]
print(f"\nTemporada 2020/2021:")
print(f"  - Total de registros: {len(dados_2020)}")
print(f"  - Registros com rodata: {len(dados_2020[dados_2020['rodata'].notna()])}")
print(f"  - Rodadas: {dados_2020['rodata'].min()} a {dados_2020['rodata'].max()}")
print(f"  - Data: {dados_2020['data'].min()} a {dados_2020['data'].max()}")

# Verificar que 2021 não existe como temporada separada
dados_2021_sep = df[df['temporada'] == 2021]
print(f"\nTemporada 2021 (separada):")
print(f"  - Registros: {len(dados_2021_sep)}")
if len(dados_2021_sep) > 0:
    print(f"  ⚠️ AVISO: Ainda há registros mapeados como temporada 2021!")
else:
    print(f"  ✓ OK: Nenhum registro como temporada 2021 (correto!)")

# Verificar anos normais
print(f"\nAlgumas temporadas normais:")
for ano in [2003, 2010, 2019, 2022]:
    dados_ano = df[df['temporada'] == ano]
    if len(dados_ano) > 0:
        print(f"  {ano}: {len(dados_ano)} registros, rodadas {dados_ano['rodata'].min()} a {dados_ano['rodata'].max()}")

print("\n" + "=" * 80)
print("TESTE 2: OBTER CAMPEÃO DE TEMPORADAS")
print("=" * 80)

# Testar 2020
try:
    campeao_2020 = obter_campeao(2020)
    if campeao_2020:
        print(f"\n✓ Campeão de 2020/2021:")
        print(f"  - Time: {campeao_2020['time']}")
        print(f"  - Pontos: {campeao_2020['pontos']}")
        print(f"  - Rodada Máxima: {campeao_2020['rodada_maxima']}")
    else:
        print(f"✗ Campeão 2020/2021 retornou None")
except Exception as e:
    print(f"✗ Erro ao obter campeão de 2020: {e}")

# Testar alguns outros anos
print(f"\n✓ Campeões de outros anos:")
try:
    todos_campeoes = obter_todos_campeoes()
    for camp in todos_campeoes[:5]:  # Mostrar primeiros 5
        print(f"  {int(camp['temporada'])}: {camp['time']} ({camp['pontos']} pts)")
    
    if len(todos_campeoes) > 5:
        print(f"  ... e mais {len(todos_campeoes) - 5} temporadas")
    
    print(f"\nTotal de temporadas: {len(todos_campeoes)}")
except Exception as e:
    print(f"✗ Erro ao obter todos os campeões: {e}")

print("\n" + "=" * 80)
print("TESTE 3: TABELA DE UMA TEMPORADA")
print("=" * 80)

# Testar tabela de 2020
try:
    tabela = tabela_temporada(2020)
    print(f"\n✓ Tabela da temporada 2020/2021:")
    print(f"  - Total de times: {len(tabela)}")
    print(f"  - Primeiro lugar: {tabela.iloc[0]['time']} ({tabela.iloc[0]['pontos']} pts)")
    if len(tabela) > 1:
        print(f"  - Segundo lugar: {tabela.iloc[1]['time']} ({tabela.iloc[1]['pontos']} pts)")
    if len(tabela) > 2:
        print(f"  - Terceiro lugar: {tabela.iloc[2]['time']} ({tabela.iloc[2]['pontos']} pts)")
except Exception as e:
    print(f"✗ Erro ao obter tabela: {e}")

print("\n" + "=" * 80)
print("TESTE 4: COMPARAR COM ANO ANTERIOR/POSTERIOR")
print("=" * 80)

# Comparar 2019 e 2020 e 2021
try:
    # 2019
    camp_2019 = obter_campeao(2019)
    if camp_2019:
        print(f"\n2019: {camp_2019['time']} ({camp_2019['pontos']} pts)")
    
    # 2020/2021
    camp_2020 = obter_campeao(2020)
    if camp_2020:
        print(f"2020/2021: {camp_2020['time']} ({camp_2020['pontos']} pts)")
    
    # 2022
    camp_2022 = obter_campeao(2022)
    if camp_2022:
        print(f"2022: {camp_2022['time']} ({camp_2022['pontos']} pts)")
    
except Exception as e:
    print(f"✗ Erro na comparação: {e}")

print("\n" + "=" * 80)
print("RESULTADO FINAL")
print("=" * 80)

# Resumo
try:
    todos_campeoes = obter_todos_campeoes()
    
    # Verificar se 2020 aparece
    tem_2020 = any(c['temporada'] == 2020 for c in todos_campeoes)
    tem_2021_sep = any(c['temporada'] == 2021 for c in todos_campeoes)
    
    print(f"\n✓ Verificações finais:")
    print(f"  - {len(todos_campeoes)} temporadas no total")
    print(f"  - Contém 2020/2021: {tem_2020}")
    print(f"  - Contém 2021 separado: {tem_2021_sep}")
    
    if tem_2020 and not tem_2021_sep:
        print(f"\n✅ TUDO CORRETO! A temporada 2020/2021 está sendo tratada como uma única temporada.")
    else:
        print(f"\n❌ PROBLEMA: A temporada 2020/2021 não está mapeada corretamente.")
        
except Exception as e:
    print(f"✗ Erro na verificação final: {e}")

print("\n" + "=" * 80)
