import sys
import random
import time

instance = sys.argv[1]
probabilidade = float(sys.argv[2])
time_limit = float(sys.argv[3])
file = open(instance, 'r')

# TAMANHO CONJUNTO
n = 0
# TAMANHO SUBCONJUNTO
m = 0
# CUSTOS
matriz_custos = []

# LER INSTANCIA
first = True
for line in file.readlines():
    line = line.rstrip('\n')
    if first:
        n = int(line.split(' ')[0])
        m = int(line.split(' ')[1])
        first = False
        matriz_custos = [None] * n
        for i in range(0, n):
            matriz_custos[i] = linha = [0] * n
        continue
    matriz_custos[int(line.split(' ')[0])][int(line.split(' ')[1])] = (float(line.split(' ')[2]))
    matriz_custos[int(line.split(' ')[1])][int(line.split(' ')[0])] = (float(line.split(' ')[2]))

#CALCULAR CUSTO DA SOLUCAO
def calcular_custo(solucao):
    resposta = 0
    for i in range(0, n):
        if solucao[i] == 1:
            for j in range(i+1, n):
                if solucao[j] == 1:
                    resposta += matriz_custos[i][j]
    return resposta

# HEURISTICA CONSTRUTIVA
def heuristica_construtiva():
    # Calcula Custos De Cada Linha
    custos_por_linha = []
    for i in range(0, n):
        custos_por_linha.append(sum(matriz_custos[i]))

    # Gera Solucao
    solucao = [0] * n
    for i in range(0, m):
        valor_aleatorio = random.random()
        if valor_aleatorio <= probabilidade:
            indice_aleatorio = random.randint(0, n - 1)
            solucao[indice_aleatorio] = 1
            custos_por_linha[indice_aleatorio] = 0
        else:
            max_value = max(custos_por_linha)
            indice = custos_por_linha.index(max_value)
            solucao[indice] = 1
            custos_por_linha[indice] = 0
    return solucao

# GRASP
def grasp(time_limit):
    time_limit = time.time() + time_limit
    solucao_incumbente = [0] * n
    while time.time() < time_limit:
        nova_solucao = heuristica_construtiva()
        nova_solucao = busca_local_simples_primeira_melhora(nova_solucao)
        if calcular_custo(nova_solucao) > calcular_custo(solucao_incumbente):
            solucao_incumbente = nova_solucao.copy()
            print('Solucao: ' + str(solucao_incumbente)[1:-1] + ", Custo: " + str(calcular_custo(solucao_incumbente)))
    return solucao_incumbente

# BUSCA LOCAL SIMPLES PRIMEIRA MELHORA
def busca_local_simples_primeira_melhora(solucao):
    melhorou = True
    melhor_solucao = solucao.copy()
    melhor_custo = calcular_custo(melhor_solucao)
    while melhorou:
        melhorou = False
        print('Solucao: ' + str(melhor_solucao)[1:-1] + ", Custo: " + str(melhor_custo))
        for i in range(0, len(melhor_solucao)):
            for j in range(i + 1, len(melhor_solucao)):
                if melhor_solucao[i] != melhor_solucao[j]:
                    nova_solucao = melhor_solucao.copy()
                    nova_solucao[i] = abs(nova_solucao[i] - 1)
                    nova_solucao[j] = abs(nova_solucao[j] - 1)
                    novo_custo = calcular_custo(nova_solucao)
                    if novo_custo > melhor_custo:
                        melhorou = True
                        melhor_solucao = nova_solucao
                        melhor_custo = novo_custo
                        break
    return melhor_solucao

#REALIZAR BUSCA
solucao = grasp(time_limit)
print('---------------------SOLUCAO FINAL---------------------')
print('Solucao: '+str(solucao)[1:-1]+", Custo: "+str(calcular_custo(solucao)))