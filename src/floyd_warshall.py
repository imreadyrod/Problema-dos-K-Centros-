import os

#O programa deverá acessar a pasta contendo os arquivos que possuem os dados dos grafos que serão processados
pasta_contendo_as_entradas = "D:\Faculdade\Implementação Grafos\Problema-dos-K-Centros-\docs"

#Com o caminho da pasta dos arquivos, o programa deverá ler cada arquivo sequencialmente 
for nome_do_arquivo in os.listdir(pasta_contendo_as_entradas):
    #primeiro deverá chegar se o fim do arquivo termina com .txt
    if nome_do_arquivo.endswith('.txt'):
        
        #se positivo o caminho do arquivo a ser processado será a junção da pasta com o nome do arquivo
        caminho_do_arquivo = os.path.join(pasta_contendo_as_entradas,nome_do_arquivo)
        nome_do_grafo = f'grafo{caminho_do_arquivo}'
        
        #realizar a leitura do arquivo para criar a estrutura do grafo
        with open(caminho_do_arquivo,'r') as arquivo:
            instrucoes = arquivo.readline().split(" ")
            n_vertices = instrucoes[0]
            n_arestas = instrucoes[1]
            n_clusters = instrucoes[2]
            grafo = [[]*n_vertices for vertice in range(n_vertices)]

            for linha in arquivo:    
                origem_destino_distancia = linha.split(" ")
                origem = origem_destino_distancia[0]
                destino = origem_destino_distancia[1]
                distancia = origem_destino_distancia[2]
                grafo[origem][destino] = distancia


    #Após a construção do grafo, via matriz. Irei aplicar o floyd-warshall. 
    #Assim consigo as distância de um vértice para todos os outros
    matriz_inicial = grafo

    #inicializando a matriz para realizar as iterações do método de floyd-warshall
    matriz_das_iterações = [[-1]*n_vertices for vertice in range(n_arestas)]
    # para aqueles vértices que não possuem ligação direta para algum dado outro vértice
    # a distância estipulada entre eles será infinito.
    INFINITO = 999999999999999999999
    
    for linha in range(n_vertices):
        for coluna in range(n_vertices):
            if(0 < matriz_inicial[linha][coluna] < INFINITO):
                matriz_das_iterações[linha][coluna] = linha



n = int(input())


D_ant = [[]*n for i in range(n)]
for i in range(n):
    linha = input().split(' ')
    linha = list(map(int,linha))
    D_ant[i] = (linha)


P_ant = [[-1]*n for i in range(n)]
#nenhum custo será maior que o maior custo vezes o numero de vertices do grafo
#aqui foi estipulado como 100
infty = 100
for i in range(n):
    for j in range(n):
        if(0 < D_ant[i][j] < infty):
            P_ant[i][j] = i


D = [[0]*n for i in range(n)]
P = [[0]*n for i in range(n)]


for k in range(n):
    for i in range(n):
        for j in range(n):
            if D_ant[i][j] <= D_ant[i][k] + D_ant[k][j]:
                D[i][j] = D_ant[i][j]
                P[i][j] = P_ant[i][j]
            else:
                D[i][j] = D_ant[i][k] +  D_ant[k][j]
                P[i][j] = P_ant[k][j]
    for i in range(n):
        for j in range(n):
            D_ant[i][j] = D[i][j]
            P_ant[i][j] = P[i][j]

print(D)
print(P)

for i in range(n):
    for j in range(n):
        print("Caminho ótimo de", i+1, "para",j+1)
        print("Custo: ", D[i][j])
        print("Trajeto: ", end='')
        C = [j+1]
        k = P[i][j]
        while k != -1:
            C.append(k+1)
            k = P[i][k]
        print(list(reversed(C)))
        print()


'''
Entrada de exemplo
5
0 1 3 100 6
100 0 1 3 100
1 2 0 1 100
3 100 100 0 2
100 100 100 1 0
'''
