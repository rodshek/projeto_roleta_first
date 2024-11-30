def criar_tabuleiro():
    """
    Cria a estrutura visual do tabuleiro.
    Adaptado para uso na interface web como referência.
    """
    numeros_roleta = [
        [None, 0, None],
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10, 11, 12],
        [13, 14, 15],
        [16, 17, 18],
        [19, 20, 21],
        [22, 23, 24],
        [25, 26, 27],
        [28, 29, 30],
        [31, 32, 33],
        [34, 35, 36]
    ]

    tabuleiro = []
    for linha in numeros_roleta:
        linha_formatada = []
        for numero in linha:
            if numero is None:
                linha_formatada.append("")
            else:
                cor = definir_cor(numero)
                linha_formatada.append((numero, cor))
        tabuleiro.append(linha_formatada)
    return tabuleiro


def definir_cor(numero):
    """
    Define a cor do número com base nas regras da roleta.
    """
    vermelhos = {1, 3, 5, 7, 9, 12, 14, 16,
                 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    pretos = {2, 4, 6, 8, 10, 11, 13, 15, 17,
              20, 22, 24, 26, 28, 29, 31, 33, 35}

    if numero == 0:
        return "green"
    elif numero in vermelhos:
        return "red"
    elif numero in pretos:
        return "black"
    return "unknown"


def atualizar_tabuleiro(tabuleiro, sugestoes):
    """
    Atualiza o estado visual do tabuleiro para destacar sugestões.
    """
    tabuleiro_destacado = []
    for linha in tabuleiro:
        linha_destacada = []
        for celula in linha:
            if isinstance(celula, tuple):
                numero, cor = celula
                if numero in sugestoes:
                    linha_destacada.append((numero, "yellow"))  # Destaque
                else:
                    linha_destacada.append((numero, cor))
            else:
                linha_destacada.append(celula)
        tabuleiro_destacado.append(linha_destacada)
    return tabuleiro_destacado
