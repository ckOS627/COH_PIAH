import re


def le_assinatura():
    '''A funcao le os valores dos tracos linguisticos do modelo e devolve uma assinatura a ser comparada com os textos fornecidos'''
    print("Bem-vindo ao detector automático de COH-PIAH.")
    print("Informe a assinatura típica de um aluno infectado:")

    wal = float(input("Entre o tamanho médio de palavra:"))
    ttr = float(input("Entre a relação Type-Token:"))
    hlr = float(input("Entre a Razão Hapax Legomana:"))
    sal = float(input("Entre o tamanho médio de sentença:"))
    sac = float(input("Entre a complexidade média da sentença:"))
    pal = float(input("Entre o tamanho medio de frase:"))

    return [wal, ttr, hlr, sal, sac, pal]


def le_textos():
    '''A funcao le todos os textos a serem comparados e devolve uma lista contendo cada texto como um elemento'''
    i = 1
    textos = []
    texto = input("Digite o texto " + str(i) + " (aperte enter para sair):")
    while texto:
        textos.append(texto)
        i += 1
        texto = input("Digite o texto " + str(i) + " (aperte enter para sair):")

    return textos


def separa_sentencas(texto):
    '''A funcao recebe um texto e devolve uma lista das sentencas dentro do texto'''
    sentencas = re.split(r'[.!?]+', texto)
    if sentencas and sentencas[-1] == '':
        del sentencas[-1]
    return sentencas


def separa_frases(sentenca):
    '''A funcao recebe uma sentenca e devolve uma lista das frases dentro da sentenca'''
    return re.split(r'[,:;]+', sentenca)


def separa_palavras(frase):
    '''A funcao recebe uma frase e devolve uma lista das palavras dentro da frase'''
    return frase.split()


def n_palavras_unicas(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras que aparecem uma unica vez'''
    freq = dict()
    unicas = 0
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            if freq[p] == 1:
                unicas -= 1
            freq[p] += 1
        else:
            freq[p] = 1
            unicas += 1

    return unicas


def n_palavras_diferentes(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras diferentes utilizadas'''
    freq = dict()
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            freq[p] += 1
        else:
            freq[p] = 1

    return len(freq)


# COMPLEMENTO

def compara_assinatura(as_a, as_b):
    '''Devolve o grau de similaridade entre duas assinaturas (menor = mais parecido)'''
    # Garante operar sobre o mesmo numero de traços
    n = min(len(as_a), len(as_b))
    if n == 0:
        return 0.0
    soma = 0.0
    for i in range(n):
        soma += abs(as_a[i] - as_b[i])
    return soma / n


def calcula_assinatura(texto):
    '''Calcula a assinatura do texto.
    Retorna [wal, ttr, hlr, sal, sac, pal] conforme especificacao.'''
    # Quebra em sentencas
    sentencas = separa_sentencas(texto)

    # Quebra cada sentenca em frases
    frases = []
    for s in sentencas:
        frases.extend(separa_frases(s))

    # Quebra cada frase em palavras
    palavras = []
    for f in frases:
        palavras.extend(separa_palavras(f))

    # Medidas base
    num_palavras = len(palavras) if palavras else 1  # evita divisao por zero
    num_sentencas = len(sentencas) if sentencas else 1
    num_frases = len(frases) if frases else 1

    # 1) Tamanho medio de palavra (conta caracteres das palavras)
    total_chars_palavras = sum(len(p) for p in palavras)
    wal = total_chars_palavras / num_palavras

    # 2) Relacao Type-Token
    ttr = n_palavras_diferentes(palavras) / num_palavras

    # 3) Razao Hapax Legomana
    hlr = n_palavras_unicas(palavras) / num_palavras

    # 4) Tamanho medio de sentenca (caracteres nas sentencas, sem os separadores — ja removidos)
    total_chars_sentencas = sum(len(s) for s in sentencas)
    sal = total_chars_sentencas / num_sentencas

    # 5) Complexidade de sentenca (numero de frases por sentenca)
    sac = num_frases / num_sentencas

    # 6) Tamanho medio de frase (caracteres nas frases, sem separadores)
    total_chars_frases = sum(len(f) for f in frases)
    pal = total_chars_frases / num_frases

    return [wal, ttr, hlr, sal, sac, pal]


def avalia_textos(textos, ass_cp):
    '''Devolve o indice (1..n) do texto mais provavelmente infectado (menor distancia).'''
    melhor_indice = 1
    melhor_dist = None

    for i, texto in enumerate(textos, start=1):
        assinatura_texto = calcula_assinatura(texto)
        dist = compara_assinatura(assinatura_texto, ass_cp)
        if melhor_dist is None or dist < melhor_dist:
            melhor_dist = dist
            melhor_indice = i

    return melhor_indice


if __name__ == "__main__":
    assinatura_cp = le_assinatura()
    textos = le_textos()
    infectado = avalia_textos(textos, assinatura_cp)
    print(f"\nO autor do texto {infectado} está infectado com COH-PIAH")
