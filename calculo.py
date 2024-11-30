def calcular_numeros_sugeridos(historico, quantidade=20):
    """
    Combina todas as estratégias para calcular os números sugeridos.
    Retorna uma lista de números únicos em ordem crescente.
    """
    sugestoes = set()

    # Estratégia: Soma e Subtração dos últimos três números
    if len(historico) >= 3:
        ultimo, penultimo, antepenultimo = historico[-1], historico[-2], historico[-3]
        soma = ultimo + penultimo + antepenultimo
        subtracao = ultimo - penultimo - antepenultimo
        if 0 <= soma <= 36:
            sugestoes.add(soma)
        if 0 <= subtracao <= 36:
            sugestoes.add(subtracao)

    # Estratégia: Combinação dos dois últimos números com o último número que saiu
    if len(historico) >= 2:
        ultimo, penultimo = historico[-1], historico[-2]

        # Primeira soma: penúltimo + último
        soma1 = penultimo + ultimo
        if 0 <= soma1 <= 36:
            sugestoes.add(soma1)

        # Segunda soma: dígitos do último número
        soma2 = sum(map(int, str(ultimo)))
        if 0 <= soma2 <= 36:
            sugestoes.add(soma2)

        # Primeira subtração: último - penúltimo
        subtracao1 = ultimo - penultimo
        if 0 <= subtracao1 <= 36:
            sugestoes.add(subtracao1)

        # Segunda subtração: dígitos do último número
        digitos = list(map(int, str(ultimo)))
        if len(digitos) == 2:  # Apenas se houver dois dígitos
            subtracao2 = digitos[0] - digitos[1]
            if 0 <= subtracao2 <= 36:
                sugestoes.add(subtracao2)

    # Estratégia: Números espelhos
    for numero in historico[-3:]:
        if numero <= 36:
            # Espelhos de roleta (37 - número)
            espelho_roleta = 37 - numero
            if 0 <= espelho_roleta <= 36:
                sugestoes.add(espelho_roleta)

            # Espelhos baseados em troca de dígitos
            espelhos_digitais = {
                12: 21, 13: 31, 23: 32,
                21: 12, 31: 13, 32: 23
            }
            if numero in espelhos_digitais:
                sugestoes.add(espelhos_digitais[numero])

    # Estratégia: Números gêmeos
    gemeos = {11, 22, 33, 31, 13, 12, 21, 23, 32}
    for numero in gemeos:
        if numero <= 36:
            sugestoes.add(numero)

    # Estratégia: Vizinhos do tabuleiro
    vizinhos_tabuleiro = {
        0: [32, 26],
        1: [2, 4], 2: [1, 3], 3: [2, 6],
        4: [1, 5], 5: [4, 6], 6: [3, 5],
        7: [8, 10], 8: [7, 9], 9: [8, 12],
        10: [7, 11], 11: [10, 14], 12: [9, 13],
        13: [12, 16], 14: [11, 15], 15: [14, 18],
        16: [13, 19], 17: [18, 20], 18: [15, 17],
        19: [16, 22], 20: [17, 21], 21: [20, 24],
        22: [19, 23], 23: [22, 26], 24: [21, 25],
        25: [24, 28], 26: [23, 27], 27: [26, 30],
        28: [25, 29], 29: [28, 32], 30: [27, 31],
        31: [30, 34], 32: [29, 33], 33: [32, 36],
        34: [31, 35], 35: [34, 36], 36: [33, 35],
    }
    for numero in historico[-3:]:
        if numero in vizinhos_tabuleiro:
            sugestoes.update(vizinhos_tabuleiro[numero])

    # Estratégia: Vizinhos da roleta
    vizinhos_roleta = {
        0: [3, 26], 1: [20, 33], 2: [21, 25],
        3: [0, 35], 4: [19, 23], 5: [10, 24],
        6: [13, 27], 7: [12, 28], 8: [11, 29],
        9: [10, 30], 10: [5, 9], 11: [8, 30],
        12: [7, 28], 13: [6, 27], 14: [17, 34],
        15: [18, 32], 16: [19, 36], 17: [14, 31],
        18: [15, 32], 19: [4, 16], 20: [1, 33],
        21: [2, 25], 22: [23, 24], 23: [4, 22],
        24: [5, 22], 25: [2, 21], 26: [0, 3],
        27: [6, 13], 28: [7, 12], 29: [8, 11],
        30: [9, 11], 31: [17, 34], 32: [15, 18],
        33: [1, 20], 34: [14, 31], 35: [3, 36],
        36: [16, 35],
    }
    for numero in historico[-3:]:
        if numero in vizinhos_roleta:
            sugestoes.update(vizinhos_roleta[numero])

    # Retorna os números sugeridos ordenados, limitados à quantidade definida
    return sorted(sugestoes)[:quantidade]
