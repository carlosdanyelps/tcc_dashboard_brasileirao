from backendtime import *


def formacoes_mais_usadas():

    formacoes_mandante = df['formacao_mandante'].value_counts()

    formacoes_visitante = df['formacao_visitante'].value_counts()

    formacoes_totais = formacoes_mandante.add(formacoes_visitante, fill_value=0)

    formacoes_ordenadas = formacoes_totais.sort_values(ascending=False)

    print("\nFormações mais usadas:")
    for formacao, count in formacoes_ordenadas.items():
        print(f"{formacao}: {count} vezes")
