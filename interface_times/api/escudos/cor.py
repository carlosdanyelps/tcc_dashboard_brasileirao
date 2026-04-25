import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

cf = pd.read_csv(os.path.join(os.path.dirname(__file__), 'dataset_times/labels.csv'))

def cor(time):
    time_cor = {row['time']: row['cor'] for _, row in cf.iterrows()}
    return time_cor.get(time, 'Cor não encontrada')