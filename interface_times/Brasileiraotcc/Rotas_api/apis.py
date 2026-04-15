from flask import Flask, jsonify, request
import sys
import os
# Permitir importar da pasta funcoes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Rotas_api.campeaosuporteapi import campeoes_geral
from funcoes.campeoes import tabela_ano
from Rotas_api.timemain import resumo_time
from escudos.API_escudos import escudo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/tabela', methods=['GET'])
def get_tabela():
    ano = request.args.get('ano')
    if not ano:
        return jsonify({
    'Campeoes todas temporadas': campeoes_geral.to_dict(orient='records')
})
    try:
        ano = int(ano)
    except:
        return jsonify({'erro': 'Ano inválido'}), 400

    tabela = tabela_ano(ano)

    return jsonify(tabela.to_dict(orient='records'))


###############################################################
############# TIME ESPECÍFICO - RESUMO COMPLETO #############
###############################################################
@app.route('/timemain')
def timemain():
    return resumo_time()

################################################################
############# ESCUDO #############
###############################################################
@app.route('/escudo/<int:id>')
def get_escudo(id):
    return escudo(id)

if __name__ == '__main__':
    app.run(debug=True)