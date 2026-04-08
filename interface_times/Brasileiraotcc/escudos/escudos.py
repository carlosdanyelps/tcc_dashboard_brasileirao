import os
import csv
from PIL import Image

pasta_entrada = "escudos"
pasta_dataset = "dataset_times/imagens"

os.makedirs(pasta_dataset, exist_ok=True)

# MAPEAMENTO EXATO (sem erro)
mapeamento = {
    1: ("Guarani", "guarani.png"),
    2: ("Athletico-PR", "athletico-paranaense-footballlogos-org.png"),
    3: ("Flamengo", "flamengo-crf-footballlogos-org.png"),
    4: ("Goias", "goias-footballlogos-org.png"),
    5: ("Internacional", "sc-internacional-footballlogos-org.png"),
    6: ("Criciuma", "criciuma-footballlogos-org.png"),
    7: ("Juventude", "juventude-footballlogos-org.png"),
    8: ("Fortaleza", "fortaleza-footballlogos-org.png"),
    9: ("Cruzeiro", "cruzeiro-footballlogos-org.png"),
    10: ("Vitoria", "vitoria-footballlogos-org.png"),
    11: ("Santos", "santos-fc-footballlogos-org.png"),
    12: ("Corinthians", "corinthians-footballlogos-org.png"),
    13: ("Fluminense", "fluminense-footballlogos-org.png"),
    14: ("Atletico-MG", "atletico-mineiro-footballlogos-org.png"),
    15: ("Coritiba", "coritiba-footballlogos-org.png"),
    16: ("Gremio", "gremio-footballlogos-org.png"),
    17: ("Bahia", "bahia-footballlogos-org.png"),
    18: ("Figueirense", "figueirense.png"),
    19: ("Paysandu", "paysandu-footballlogos-org.png"),
    20: ("Ponte Preta", "ponte-preta.png"),
    21: ("Parana", "parana-clube-de-curitiba-pr-logo-png-transparent.png"),
    22: ("Sao Caetano", "Associação_Desportiva_São_Caetano.png"),
    23: ("Sao Paulo", "sao-paulo-spfc-footballlogos-org.png"),
    24: ("Vasco", "vasco-de-gama-footballlogos-org.png"),
    25: ("Botafogo-RJ", "botafogo-footballlogos-org.png"),
    26: ("Palmeiras", "palmeiras-footballlogos-org.png"),
    27: ("Brasiliense", "Brasiliense_Futebol_Clube.png"),
    28: ("Santa Cruz", "santa-cruz.png"),
    29: ("America-RN", "América_RN.png"),
    30: ("Sport", "sport-recife-footballlogos-org.png"),
    31: ("Nautico", "nautico.png"),
    32: ("Ipatinga", "IpatingaFC.png"),
    33: ("Portuguesa", "Portuguesa_de_Desportos.png"),
    34: ("Avai", "avai-fc-footballlogos-org.png"),
    35: ("Santo Andre", "Santo_Andre_escudo.png"),
    36: ("Barueri", "barueri-logo-png_seeklogo-16817.png"),
    37: ("Atletico-GO", "atletico-goianiense-footballlogos-org.png"),
    38: ("Ceara", "ceara-fc-footballlogos-org.png"),
    39: ("Gremio Prudente", "Grêmio_Prudente2019.png"),
    40: ("America-MG", "america-mineiro-footballlogos-org.png"),
    41: ("Chapecoense", "chapecoense-footballlogos-org.png"),
    42: ("Joinville", "Joinville-SC.png"),
    43: ("CSA", "csa.png"),
    44: ("Bragantino", "rb-bragantino-footballlogos-org.png"),
    45: ("Cuiaba", "cuiaba-footballlogos-org.png"),
}

labels = []

for id_time, (nome_time, arquivo) in mapeamento.items():

    caminho = os.path.join(pasta_entrada, arquivo)

    if not os.path.exists(caminho):
        print(f"❌ Arquivo NÃO existe: {arquivo}")
        continue

    img = Image.open(caminho)
    img = img.resize((224, 224))

    destino = os.path.join(pasta_dataset, arquivo)
    img.save(destino)

    labels.append([id_time, arquivo, nome_time])

# salvar CSV
with open("dataset_times/labels.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "arquivo", "time"])
    writer.writerows(labels)

print("✅ Dataset criado corretamente (sem erro de correspondência)")