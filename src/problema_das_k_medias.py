import os
import numpy as np
from itertools import combinations

# para aqueles vértices que não possuem ligação direta para algum dado outro vértice
# a distância estipulada entre eles será infinito.
INFINITO = 999999999999999999999999999999

#O programa deverá acessar a pasta contendo os arquivos que possuem os dados dos grafos que serão processados
pasta_contendo_as_entradas = "D:\Faculdade\Implementação Grafos\Problema-dos-K-Centros-\docs"

#Com o caminho da pasta dos arquivos, o programa deverá ler cada arquivo sequencialmente
# A linha abaixo realiza a leitura de arquivo a arquivo 
for nome_do_arquivo in os.listdir(pasta_contendo_as_entradas):
    # Os arquivos disponibilizados estão no formato txt
    #primeiro deverá chegar se o fim do arquivo termina com .txt
    if nome_do_arquivo.endswith('.txt'):
        
        #se positivo o caminho do arquivo a ser processado será a junção da pasta com o nome do arquivo
        caminho_do_arquivo = os.path.join(pasta_contendo_as_entradas,nome_do_arquivo)
        # o nome do arquivo processado deverá ser salvo para que, ao final, o programa grave os arquivos txt com os resultados do processamento 
        nome_do_grafo = f'grafo{caminho_do_arquivo}'
        
        # A operação abaixo realiza a leitura do arquivo para criar a estrutura do grafo
        # A primeira operação é a leitura da primeira linha para determinar o número de vértices,
        #  número de arestas e o número de clusters. Assim a matriz "grafo" é inicializada
        with open(caminho_do_arquivo,'r') as arquivo:
            instrucoes = arquivo.readline().split(" ")
            n_vertices = instrucoes[0]
            n_arestas = instrucoes[1]
            n_clusters = instrucoes[2]
            
            # A criação da matriz deve ter n_vertices linhas e n_arestas colunas, sendo que à princípio
            #  todos os índices terão valor igual à constante "infinito" definida no início do arquivo
            grafo = np.full((n_vertices,n_vertices),INFINITO)

            

            # No bloco a seguir o restante das linhas (após a primeira) são processadas 
            # e o vértice de origem o vértice de destino e a distância entre eles é guardada na matriz "grafo"
            # Aqui deve-se inicializar a distância, ou seja, a posição da linha do vértice para ele mesmo como 0
            # E caso o vértice não possua aresta para um outro vértice o valor será infinito, como foi definido anteriormente
    
            for linha in arquivo:    
                origem_destino_distancia = linha.split(" ")
                origem = origem_destino_distancia[0]
                destino = origem_destino_distancia[1]
                distancia = origem_destino_distancia[2]
                grafo[origem][destino] = distancia
                grafo[origem][origem] = 0


    #Após a construção do grafo, via matriz, irei aplicar o algoritmo de Floyd-Warshall. 
    #Assim consigo as distância de todos para todos os vértices.

    # A estrutura inicilizada "matriz_distancia_iteracao_anterior" contém os as distância entre os vértices
    matriz_distancia_iteracao_anterior = grafo

    # De início a estrutura "matriz_com_caminhos_iteracao_anterior" guarda 
    # os vértices de destino para um determinado vértice de origem
    # Ela irá guardar os melhores caminhos iteração a iteração
    matriz_com_caminhos_iteracao_anterior = [[-1]*n_vertices for vertice in range(n_arestas)]

    
    # O código abaixo itera entre todos os vértice para todos os outros 
    # E descobre se existe caminho entre um vértice e outro.
    # Desta maneira, se a posição acessada na matriz é ele mesmo o valor será zero 
    # Se não existe caminho entre os pares de vértice, a distância será infinito
    # Caso exista a posição de destino será preenchida com o vértice de origem
    for origem in range(n_vertices):
        for destino in range(n_vertices):
            if(0 < matriz_distancia_iteracao_anterior[origem][destino] < INFINITO):
                matriz_com_caminhos_iteracao_anterior[origem][destino] = origem


    # Inicializando as matrizes necessárias para guardar os valores das iterações
    # Desta maneira, se a distância da iteração anterior for maior, o valor na matriz final deverá ser atualizado 

    matriz_distancias_iteracao_atual = [[0]*n_vertices for vertice in range(n_vertices)]
    matriz_caminhos_iteracao_atual = [[0]*n_vertices for vertice in range(n_vertices)]

    for linha in range (n_vertices):
        for coluna in range(n_arestas):
            for iteracao in range(n_vertices):
                if matriz_distancia_iteracao_anterior[coluna][iteracao] <= matriz_distancia_iteracao_anterior[coluna][linha] + matriz_distancia_iteracao_anterior[linha][iteracao]:
                    matriz_distancias_iteracao_atual[coluna][iteracao] = matriz_distancia_iteracao_anterior[coluna][iteracao]
                    matriz_caminhos_iteracao_atual[coluna][iteracao] = matriz_caminhos_iteracao_atual[coluna][iteracao]
                else:
                    matriz_distancias_iteracao_atual[coluna][iteracao] = matriz_distancias_iteracao_atual[coluna][iteracao] + matriz_distancias_iteracao_atual[iteracao][coluna]
                    matriz_caminhos_iteracao_atual[coluna][iteracao] = matriz_com_caminhos_iteracao_anterior[linha][iteracao]
                ## Após realizar o cálculos dos novos pesos e também determinar os melhores caminhos para a iteração atual
                # As matrizes devem ser atualizadas
                for linha in range(n_vertices):
                    for coluna in range(n_vertices):
                        matriz_distancia_iteracao_anterior[linha][coluna] = matriz_distancias_iteracao_atual[linha][coluna]
                        matriz_com_caminhos_iteracao_anterior[linha][coluna] = matriz_caminhos_iteracao_atual[linha][coluna]
        
    
    # Para saber a distancia do vértice i até o vértice j, ou seja, o seu custo, deve-se utilizar a matriz
    # matriz_caminhos_iteracao_atual. Um exemplo: Distância para ir do vértice 2 até o vértice 6:
    # distância = matriz_caminhos_iteracao_atual[2][6]

    # Após completar o processamento do grafo teremos em mãos a matriz com a distância de todos vértices para todos os outros vértices.
    
    ############# POSSUI SOLUÇÃO MELHOR, EXPLICADA PELO PROFESSOR NO DIA 26/06 EM AULA######################################
    ############# DESCRIÇÃO NO FIM DO ARQUIVO ################################################################
    # O problema da K-média consiste em receber um conjunto de entrada e 
    # realizar subdivisões de acordo com o número de clusters .
    # Então, por exemplo, considerando o primeiro arquivo "Problema-dos-K-Centros-\docs\entradas\pmed1.txt"
    # A especificação é a seguinte:  vértices = 100; arestas = 200; nº de clusters = 5. 
    # A resposta esperada, que pode ser encontrada em "Problema-dos-K-Centros-\docs\resposta\resposta.txt" , 
    # Determina que o conjunto irá possuir 5 clusters e o raio para cada cluster é 127.
    # Ou seja, devo realizar a verificação de todas as combinações possíveis de 5 em 100. 
    # Após ter em mãos todas as combinações, irei realizar a seguinte operação.
    # Tomando um conjunto aleatório das combinações. Este conjunto terá 20 vértices. 
    # Dentro dos 20 vértices, 1 deles deverá ser o centro. Porém, qual centro sera o determinante para que o raio seja 127?
    # Dito isto, terei que variar o centro dentro do subconjunto e verificar qual vértice centroíde retorna como raio o valor de 127.
    # O raio é a distância do centro até o elemento mais distante daquele cluster.
    # Sendo assim, caso eu realize a subdivisão e não encontre o valor de 127 para todos os possíveis centróides deste subconjunto
    # Esse conjunto será descartado. E o próximo será processado como se fosse uma fila

    # Sendo assim, o próximo passo é realizar todas as combinações possíveis guardar todos os conjuntos possíveis em uma estrutura do tipo fila 
     






#   Protti, Fábio "Implementação em Python do algoritmo de Floyd-Warshall" YouTube.
#   Disponível em: https://www.youtube.com/watch?v=FzBs8BV2oHs. Acesso em: 25 jun. 2024.



# solução zenilton... determinar os clusters e armazenar a distância apenas dos maximos para cada centroide
# entao por exemplo... centroide como vertice 1 ... vertice 2 e 6 sao mais proximos, centroide como vertice 3... vertices 4 e 5 sao mais proximos
# centroide como vertice 7, vertices 8 é mais proximo.... 
# o raio daquele cluster é a maior distancia... por isso é interessante guardar apenas a maior distancia... entao ao final o raio da solução é o maior raio entre esses 3 clusters 
# após gerar outra combinação de vértices realizar o mesmo procedimento e retirar o raio da solução...
# após isso 
