import pandas as pd
import os

# Lista de arquivos CSV a corrigir (adicione outros caminhos se necessário)
CSV_PATHS = [
    os.path.join(os.path.dirname(__file__), 'campeonato-brasileiro-full.csv'),
    os.path.join(os.path.dirname(__file__), '../Rotas_api/campeonato-brasileiro-full.csv'),
]

def preencher_rodata(row):
    # Tenta usar a coluna rodata principal
    if pd.notna(row['rodata']):
        return row['rodata']
    # Tenta usar colunas auxiliares
    for col in ['rodata_final', 'rodata_calculada', 'rodata_x', 'rodata_y']:
        if col in row and pd.notna(row[col]):
            return row[col]
    return None

def corrigir_temporada(row):
    # Corrige a temporada 2020/2021 por data
    data = pd.to_datetime(row['data'], errors='coerce')
    if pd.isna(data):
        return row['ano_civil']
    inicio_2020 = pd.Timestamp('2020-08-08')
    fim_2020 = pd.Timestamp('2021-02-25')
    if inicio_2020 <= data <= fim_2020:
        return 2020
    if data > fim_2020:
        return 2021
    return row['ano_civil']

def corrigir_csv(path):
    print(f'Corrigindo: {path}')
    df = pd.read_csv(path)
    # Preencher rodata
    df['rodata_corrigida'] = df.apply(preencher_rodata, axis=1)
    # Corrigir temporada
    if 'ano_civil' not in df.columns:
        df['ano_civil'] = pd.to_datetime(df['data'], errors='coerce').dt.year
    df['temporada_corrigida'] = df.apply(corrigir_temporada, axis=1)
    # Atualizar colunas principais
    df['rodata'] = df['rodata_corrigida']
    df['temporada'] = df['temporada_corrigida']
    # Remover duplicatas por partida_id, data, mandante, visitante
    if 'partida_id' in df.columns:
        df = df.drop_duplicates(subset=['partida_id', 'data', 'mandante', 'visitante'])
    else:
        df = df.drop_duplicates(subset=['data', 'mandante', 'visitante'])
    # Salvar sobrescrevendo
    df.to_csv(path, index=False)
    print(f'Arquivo corrigido e salvo: {path}')

if __name__ == '__main__':
    for csv_path in CSV_PATHS:
        if os.path.exists(csv_path):
            corrigir_csv(csv_path)
        else:
            print(f'Arquivo não encontrado: {csv_path}')
