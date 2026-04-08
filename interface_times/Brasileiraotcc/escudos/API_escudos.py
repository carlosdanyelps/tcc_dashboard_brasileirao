from flask import Flask, send_file, abort
import pandas as pd
import os

app = Flask(__name__)

# caminho absoluto (evita erro de diretório)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(BASE_DIR, "dataset_times", "labels.csv")
img_path = os.path.join(BASE_DIR, "dataset_times", "imagens")

labels = pd.read_csv(csv_path)

# garante que ID é inteiro
labels["ID"] = labels["ID"].astype(int)

@app.route("/")
def home():
    return "API de escudos funcionando!"

@app.route("/escudo/<int:id>")
def escudo(id):

    # busca pelo ID
    linha = labels[labels["ID"] == id]

    if linha.empty:
        return {"erro": "ID não encontrado"}, 404

    arquivo = linha.iloc[0]["arquivo"]
    caminho = os.path.join(img_path, arquivo)

    if not os.path.exists(caminho):
        return {"erro": "Imagem não encontrada"}, 404

    return send_file(caminho)

app.run(debug=True)