from flask import Flask, request, jsonify
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

df = pd.read_csv('campeonato-brasileiro-full.csv')
df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')
df['ano'] = df['data'].dt.year


