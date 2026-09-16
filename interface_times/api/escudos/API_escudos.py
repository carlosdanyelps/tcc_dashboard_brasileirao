from io import BytesIO

from flask import send_file
from sqlalchemy import text

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.db import engine


def escudo(id):
    with engine.connect() as conn:
        resultado = conn.execute(
            text("""
                SELECT
                    arquivo,
                    imagem
                FROM times
                WHERE id = :id
                LIMIT 1
            """),
            {
                "id": id
            }
        ).mappings().first()

    if resultado is None:
        return {
            "erro": "ID não encontrado"
        }, 404

    imagem = resultado["imagem"]

    if imagem is None:
        return {
            "erro": "Imagem não encontrada"
        }, 404

    return send_file(
        BytesIO(imagem),
        mimetype="image/png",
        download_name=resultado["arquivo"]
    )