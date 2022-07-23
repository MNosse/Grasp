import sys
import random
import time

instance = sys.argv[1]
limite_tabu = int(sys.argv[2])
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

# GERAR SOLUCAO INICIAL
solucao_inicial = [0] * n
for i in range(0, m):
    while True:
        indice = random.randint(0, n - 1)
        if solucao_inicial[indice] != 1:
            solucao_inicial[indice] = 1
            break
        continue


# CALCULAR CUSTO DA SOLUCAO
def calcular_custo(solucao):
    resposta = 0
    for i in range(0, n):
        if solucao[i] == 1:
            for j in range(i + 1, n):
                if solucao[j] == 1:
                    resposta += matriz_custos[i][j]
    return resposta


# BUSCA TABU
def busca_tabu(solucao, limite_tabu, time_limit):
    time_limit = time.time() + time_limit
    solucao_base = solucao.copy()
    solucao_incumbente = solucao_base.copy()
    custo_solucao_incumbente = calcular_custo(solucao_incumbente)
    lista_tabu = [-limite_tabu] * n
    iteracao = 0
    print('Solucao: ' + str(solucao_incumbente)[1:-1] + ", Custo: " + str(calcular_custo(solucao_incumbente)))
    while time.time() < time_limit:
        iteracao += 1
        vizinhos = []
        for i in range(0, n):
            for j in range(i + 1, n):
                if solucao_base[i] != solucao_base[j]:
                    vizinho = solucao_base.copy()
                    vizinho[i] = abs(vizinho[i] - 1)
                    vizinho[j] = abs(vizinho[j] - 1)
                    elemento = [calcular_custo(vizinho), vizinho, i, j]
                    vizinhos.append(elemento)
        vizinhos = sorted(vizinhos, reverse=True)
        nova_solucao = []
        custo_solucao_base = calcular_custo(solucao_base)

        achou_solucao = False
        if vizinhos[0][0] > custo_solucao_incumbente:
            nova_solucao = vizinhos[0][1].copy()
            lista_tabu[vizinhos[0][2]] = iteracao
            lista_tabu[vizinhos[0][3]] = iteracao
            achou_solucao = True
        if not achou_solucao:
            for i in range(0, len(vizinhos)):
                if vizinhos[i][0] > custo_solucao_base:
                    if (iteracao > lista_tabu[vizinhos[i][2]] + limite_tabu and iteracao > lista_tabu[
                        vizinhos[i][3]] + limite_tabu):
                        nova_solucao = vizinhos[i][1].copy()
                        lista_tabu[vizinhos[i][2]] = iteracao
                        lista_tabu[vizinhos[i][3]] = iteracao
                        achou_solucao = True
                        break
                else:
                    break

        if not achou_solucao:
            for i in range(0, len(vizinhos)):
                if (iteracao > lista_tabu[vizinhos[i][2]] + limite_tabu and iteracao > lista_tabu[
                    vizinhos[i][3]] + limite_tabu):
                    nova_solucao = vizinhos[i][1]
                    lista_tabu[vizinhos[i][2]] = iteracao
                    lista_tabu[vizinhos[i][3]] = iteracao
                    achou_solucao = True
                    break
        if not achou_solucao:
            nova_solucao = vizinhos[0][1].copy()
            lista_tabu[vizinhos[0][2]] = iteracao
            lista_tabu[vizinhos[0][3]] = iteracao

        solucao_base = nova_solucao.copy()
        if calcular_custo(solucao_incumbente) < calcular_custo(solucao_base):
            solucao_incumbente = solucao_base.copy()
            custo_solucao_incumbente = calcular_custo(solucao_incumbente)
            print('Solucao: ' + str(solucao_incumbente)[1:-1] + ", Custo: " + str(
                custo_solucao_incumbente) + "\n")
    return solucao_incumbente


# REALIZAR BUSCA
solucao = busca_tabu(solucao_inicial, limite_tabu, time_limit)
print('---------------------SOLUCAO FINAL---------------------')
print('Solucao: ' + str(solucao)[1:-1] + ", Custo: " + str(calcular_custo(solucao)))