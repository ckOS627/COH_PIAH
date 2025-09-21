# Detector de COH-PIAH (Detecção de Autoria)

Este projeto implementa um detector simples de similaridade de autoria textual. Ele compara a “assinatura” linguística de textos informados com uma assinatura de referência (de um autor infectado por COH-PIAH) e aponta qual texto está mais próximo dessa assinatura.


## Sumário
- O que é a assinatura linguística
- Como instalar/rodar
- Como usar (passo a passo e exemplos)
- Entradas e saídas
- Estrutura do projeto
- Explicação do código (trechos linha a linha)
- Fórmula de similaridade
- Limitações e melhorias sugeridas


## O que é a assinatura linguística
Usamos 6 traços:
1. wal (tamanho médio de palavra)
2. ttr (relação Type-Token)
3. hlr (razão Hapax Legomana)
4. sal (tamanho médio de sentença)
5. sac (complexidade de sentença = frases/sentença)
6. pal (tamanho médio de frase)

Quanto menor a média das diferenças absolutas entre os 6 traços do texto e os 6 traços da assinatura de referência, mais parecido (mais “infectado”) está o texto.


## Como instalar/rodar
Pré-requisitos:
- Python 3.7+ instalado e acessível no seu PATH (Windows, PowerShell).

No PowerShell (Windows):
1) Navegue até a pasta do arquivo (se já estiver em `C:\Users\claud`, ignore):
   - `cd C:\Users\claud`
2) Execute o programa:
   - `python .\coh_piah.py`


## Como usar (passo a passo)
1) Ao iniciar, o programa pedirá os 6 números da assinatura típica de um aluno infectado. Exemplo:
   - Entre o tamanho médio de palavra: 4.51
   - Entre a relação Type-Token: 0.693
   - Entre a Razão Hapax Legomana: 0.55
   - Entre o tamanho médio de sentença: 70.82
   - Entre a complexidade média da sentença: 1.82
   - Entre o tamanho medio de frase: 38.5

2) Em seguida, digite os textos, um por linha. Cada ENTER finaliza um texto e solicita o próximo. Para encerrar a entrada, pressione ENTER em branco.
   - Importante: cada “texto” é uma única linha (não cole parágrafos com quebras de linha).

3) O programa imprimirá qual texto (1..n) está mais parecido com a assinatura de referência:
   - `O autor do texto 2 está infectado com COH-PIAH`


## Entradas e saídas
- Entrada: 6 floats (assinatura de referência) + N linhas de texto.
- Saída: índice (1..N) do texto mais similar à assinatura de referência.


## Estrutura do projeto
- `coh_piah.py` — código principal do detector.


## Explicação do código (trechos linha a linha)
Abaixo estão os principais trechos do arquivo com comentários sobre o que cada parte faz.

### Leitura da assinatura
```python path=C:\Users\claud\coh_piah.py start=4
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
```
- Exibe instruções e coleta 6 valores via `input`, convertendo para `float`.
- Retorna a lista na ordem esperada: `[wal, ttr, hlr, sal, sac, pal]`.

### Leitura dos textos (um por linha)
```python path=C:\Users\claud\coh_piah.py start=19
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
```
- Lê N textos até o usuário enviar uma linha vazia.
- Cada linha retorna como um elemento da lista `textos`.

### Funções de separação (caixas-pretas do exercício)
```python path=C:\Users\claud\coh_piah.py start=32
def separa_sentencas(texto):
    '''A funcao recebe um texto e devolve uma lista das sentencas dentro do texto'''
    sentencas = re.split(r'[.!?]+', texto)
    if sentencas and sentencas[-1] == '':
        del sentencas[-1]
    return sentencas
```
- Divide por `. ! ?`, remove vazio final se existir.

```python path=C:\Users\claud\coh_piah.py start=40
def separa_frases(sentenca):
    '''A funcao recebe uma sentenca e devolve uma lista das frases dentro da sentenca'''
    return re.split(r'[,:;]+', sentenca)
```
- Divide cada sentença em frases por `, : ;`.

```python path=C:\Users\claud\coh_piah.py start=45
def separa_palavras(frase):
    '''A funcao recebe uma frase e devolve uma lista das palavras dentro da frase'''
    return frase.split()
```
- Divide por espaços.

### Contagem de palavras distintas e únicas
```python path=C:\Users\claud\coh_piah.py start=67
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
```
- Usa dicionário para contar quantos tipos (tokens distintos) existem, ignorando caixa.

```python path=C:\Users\claud\coh_piah.py start=50
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
```
- Conta especificamente as palavras com frequência 1 (hapax), ajustando o contador quando um termo deixa de ser único.

### Similaridade entre assinaturas
```python path=C:\Users\claud\coh_piah.py start=82
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
```
- Média das diferenças absolutas elemento a elemento (6 traços). Quanto menor, mais similar.

### Cálculo da assinatura de um texto
```python path=C:\Users\claud\coh_piah.py start=94
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
```
- Produz os 6 traços a partir das listas `sentencas`, `frases`, `palavras`.
- As contagens usam `len` das strings já sem os separadores.
- Proteções simples contra divisão por zero (casos patológicos).

### Escolha do texto mais “infectado”
```python path=C:\Users\claud\coh_piah.py start=139
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
```
- Itera sobre cada texto, calcula sua assinatura, compara com a referência e guarda o menor valor.

### Ponto de entrada (main)
```python path=C:\Users\claud\coh_piah.py start=154
if __name__ == "__main__":
    assinatura_cp = le_assinatura()
    textos = le_textos()
    infectado = avalia_textos(textos, assinatura_cp)
    print(f"\nO autor do texto {infectado} está infectado com COH-PIAH")
```
- Fluxo principal quando você executa o arquivo.


## Fórmula de similaridade
Sejam as assinaturas `A=[a1..a6]` e `B=[b1..b6]`:
```
similaridade = (|a1-b1| + |a2-b2| + ... + |a6-b6|) / 6
```
- Resultado menor indica maior proximidade entre as assinaturas.


## Limitações e melhorias
- Entrada de texto é por linha única (ENTER vazio encerra). Poderia aceitar múltiplas linhas por texto.
- Não há normalização de acentos/pontuação interna nas palavras; isso pode ser adicionado conforme necessidade.
- Proteções contra divisão por zero mantêm o programa estável, mas textos vazios não são casos de uso recomendados.


## Licença
Uso educacional/didático.
