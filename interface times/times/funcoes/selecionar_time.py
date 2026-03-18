
import pandas as pd


df = pd.read_csv('campeonato-brasileiro-full.csv')

def time():
  time = input('Selecione um time: ')
  print((df['mandante'] == time) | (df['visitante'] == time))
time()