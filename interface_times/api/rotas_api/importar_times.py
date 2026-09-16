import csv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import text
from db.db import engine

# ============================================================
# CONFIGURAÇÕES
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "escudos",
    "dataset_times",
    "labels.csv"
)

IMG_DIR = os.path.join(
    BASE_DIR,
    "escudos",
    "dataset_times",
    "imagens"
)


# ============================================================
# IMPORTAÇÃO
# ============================================================

def importar_times():

    print("Iniciando importação dos times...")

    with open(
        CSV_PATH,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo_csv:

        leitor = csv.DictReader(arquivo_csv)

        registros = 0

        with engine.begin() as conn:

            for linha in leitor:

                id_time = int(linha["ID"])

                arquivo = linha["arquivo"]

                nome_time = linha["time"]

                cor = linha["cor"]

                borda_cor = linha["bordaCor"]

                caminho_imagem = os.path.join(
                    IMG_DIR,
                    arquivo
                )

                # --------------------------------------------
                # Verifica imagem
                # --------------------------------------------

                if not os.path.exists(caminho_imagem):

                    print(
                        f"⚠️ Imagem não encontrada: {arquivo}"
                    )

                    continue

                # --------------------------------------------
                # Lê imagem como bytes
                # --------------------------------------------

                with open(
                    caminho_imagem,
                    "rb"
                ) as imagem:

                    imagem_bytes = imagem.read()

                # --------------------------------------------
                # Insere / atualiza
                # --------------------------------------------

                conn.execute(
                    text("""
                        INSERT INTO times (
                            id,
                            arquivo,
                            time,
                            cor,
                            borda_cor,
                            imagem
                        )

                        VALUES (
                            :id,
                            :arquivo,
                            :time,
                            :cor,
                            :borda_cor,
                            :imagem
                        )

                        ON CONFLICT (id)

                        DO UPDATE SET

                            arquivo = EXCLUDED.arquivo,
                            time = EXCLUDED.time,
                            cor = EXCLUDED.cor,
                            borda_cor = EXCLUDED.borda_cor,
                            imagem = EXCLUDED.imagem
                    """),
                    {
                        "id": id_time,
                        "arquivo": arquivo,
                        "time": nome_time,
                        "cor": cor,
                        "borda_cor": borda_cor,
                        "imagem": imagem_bytes
                    }
                )

                registros += 1

                print(
                    f"✅ {id_time} - {nome_time}"
                )

    print()
    print(
        f"✅ Importação concluída: {registros} times"
    )


if __name__ == "__main__":
    importar_times()