from flask import Flask, jsonify, request
import sys
import os
# Permitir importar da pasta funcoes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Rotas_api.campeaosuporteapi import campeoes_geral
from funcoes.campeoes import tabela_ano

app = Flask(__name__)


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

if __name__ == '__main__':
    app.run(debug=True)