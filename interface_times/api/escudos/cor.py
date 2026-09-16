from sqlalchemy import text

from db.db import engine


def buscar_time(nome):
    with engine.connect() as conn:
        resultado = conn.execute(
            text("""
                SELECT
                    id,
                    time,
                    cor,
                    borda_cor
                FROM times
                WHERE LOWER(time) = LOWER(:time)
                LIMIT 1
            """),
            {
                "time": nome
            }
        ).mappings().first()

    return resultado


def cor(time):
    resultado = buscar_time(time)

    if resultado is None:
        return "Cor não encontrada"

    return resultado["cor"]


def bordaCor(time):
    resultado = buscar_time(time)

    if resultado is None:
        return "BordaCor não encontrado"

    return resultado["borda_cor"]