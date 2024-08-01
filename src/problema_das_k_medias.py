import os
import numpy as np
import time as tempo
from itertools import combinations

# para aqueles vértices que não possuem ligação direta para algum dado outro vértice
# a distância estipulada entre eles será infinito.
INFINITO = np.inf

#O programa deverá acessar a pasta contendo os arquivos que possuem os dados dos grafos que serão processados
pasta_contendo_as_entradas = r"D:\\Faculdade\\Implementação Grafos\\Problema-dos-K-Centros-\\docs\\entradas"
pasta_contendo_as_respostas = r"D:\\Faculdade\\Implementação Grafos\\Problema-dos-K-Centros-\\docs\\resposta"

nome_arquivo_resposta = "resposta.txt"
#Com o caminho da pasta dos arquivos, o programa deverá ler cada arquivo sequencialmente
# A linha abaixo realiza a leitura de arquivo a arquivo 
for nome_do_arquivo in os.listdir(pasta_contendo_as_entradas):
    
    # Os arquivos disponibilizados estão no formato txt
    #primeiro deverá chegar se o fim do arquivo termina com .txt
    if nome_do_arquivo.endswith('.txt'):
        
        
        # A abertura do arquivo funcionára como um contador, pois devo também abrir o arquivo de resposta
        # e retirar o raio da solução para determinada instância
        conta_arquivos = 1

        #Aqui pego o nome do arquivo contendo as respostas e a pasta onde esse arquivo está e realizo
        # a abertura desse arquivo.
        caminho_do_arquivo_resposta = os.path.join(pasta_contendo_as_respostas,nome_arquivo_resposta)
        

        with open(caminho_do_arquivo_resposta,'r') as arquivo_resposta:
            #Lendo todas as linhas do arquivo resposta

            instrucoes_resposta = arquivo_resposta.readlines()

            #Pegando as respostas para uma determinada instancia
            resposta_da_instancia = instrucoes_resposta[conta_arquivos-1].split()

            #Pegando qual é a solucao daquela instancia
            raio_solucao = int(resposta_da_instancia[-1])

        #se positivo o caminho do arquivo a ser processado será a junção da pasta com o nome do arquivo
        caminho_do_arquivo = os.path.join(pasta_contendo_as_entradas,nome_do_arquivo)
        # o nome do arquivo processado deverá ser salvo para que, ao final, o programa grave os arquivos txt com os resultados do processamento 
        nome_do_grafo = f'grafo{caminho_do_arquivo}'
        
        # A operação abaixo realiza a leitura do arquivo para criar a estrutura do grafo
        # A primeira operação é a leitura da primeira linha para determinar o número de vértices,
        #  número de arestas e o número de clusters. Assim a matriz "grafo" é inicializada

        inicio = tempo.time()

        with open(caminho_do_arquivo,'r') as arquivo:
            instrucoes = arquivo.readline().split()
            n_vertices = int(instrucoes[0])
            n_arestas = int(instrucoes[1])
            n_clusters = int(instrucoes[2])
            
            # A criação da matriz deve ter n_vertices linhas e n_arestas colunas, sendo que à princípio
            #  todos os índices terão valor igual à constante "infinito" definida no início do arquivo
            grafo = np.full((n_vertices,n_vertices),INFINITO)
            
            # No bloco a seguir o restante das linhas (após a primeira) são processadas 
            # e o vértice de origem o vértice de destino e a distância entre eles é guardada na matriz "grafo"
            # Aqui deve-se inicializar a distância, ou seja, a posição da linha do vértice para ele mesmo como 0
            # E caso o vértice não possua aresta para um outro vértice o valor será infinito, como foi definido anteriormente
    
            for linha in arquivo:    
                origem_destino_distancia = linha.split()
                origem = int(origem_destino_distancia[0])-1
                destino = int(origem_destino_distancia[1])-1
                distancia = int(origem_destino_distancia[2])
                grafo[origem][destino] = distancia
                grafo[origem][origem] = 0    
            

    #Após a construção do grafo, via matriz, irei aplicar o algoritmo de Floyd-Warshall. 
    #Assim consigo as distância de todos para todos os vértices.

    # A estrutura inicilizada "matriz_distancia_iteracao_anterior" contém os as distância entre os vértices
    matriz_distancia_iteracao_anterior = grafo

    # De início a estrutura "matriz_com_caminhos_iteracao_anterior" guarda 
    # os vértices de destino para um determinado vértice de origem
    # Ela irá guardar os melhores caminhos iteração a iteração
    matriz_com_caminhos_iteracao_anterior = np.full((n_vertices,n_vertices),-1)

    
    # O código abaixo itera entre todos os vértice para todos os outros 
    # E descobre se existe caminho entre um vértice e outro.
    # Desta maneira, se a posição acessada na matriz é ele mesmo o valor será zero 
    # Se não existe caminho entre os pares de vértice, a distância será infinito
    # Caso exista a posição de destino será preenchida com o vértice de origem
    for origem in range(n_vertices):
        for destino in range(n_vertices):
            if(0 < matriz_distancia_iteracao_anterior[origem][destino] < INFINITO):
                matriz_com_caminhos_iteracao_anterior[origem][destino] = origem


    # Floyd-Warshall é um algoritmo de programação dinâmica. A distancia atual é calculada apenas com
    # os valores da interação anterior. Este algoritmo possui complexidade de n^3. Ou seja, para valores extremos 
    # Fica inviável o cálculo da matriz de distancias para todos os pares de vértices. Como estamos tratando de um problema de clusterização 
    # Faz sentido gastar um tempo para calcular de uma vez só a distância de todos para todos, pois, mais abaixo, iremos realizar a consulta dessas distâncias
    # para cada combinação de centróide.
    

    # Inicializando as matrizes necessárias para guardar os valores das iterações
    # Desta maneira, se a distância da iteração anterior for maior, o valor na matriz final deverá ser atualizado 
    # a operação abaixo inicializa as matrizes com zeros 
    matriz_distancias_iteracao_atual = np.zeros((n_vertices,n_vertices))
    matriz_caminhos_iteracao_atual = np.zeros((n_vertices,n_vertices))
    
    
    for intermediario in range(n_vertices):
        for origem in range (n_vertices):
            for destino in range(n_vertices):

                #A matriz Dk(i,j) é a melhor opção entre dois valores:
                # A condição abaixo verifica se a distancia da origem até o destino é menor ou igual do que a 
                # distância entre a origem e o destino considerando o intermediario realizando uma ponte entre esse par de vértices.
                
                # a soma abaixo
                # matriz_distancia_iteracao_anterior[origem][intermediario] + matriz_distancia_iteracao_anterior[intermediario][destino]
                # é a soma da distância entre a origem e o intermediário mais a distância entre o intermediário e o destino 
                
                if matriz_distancia_iteracao_anterior[origem][destino] <= matriz_distancia_iteracao_anterior[origem][intermediario] + matriz_distancia_iteracao_anterior[intermediario][destino]:
                    
                    # Caso a distância entre origem e destino é menor do que a distancia considerando o intermediario
                    # A matriz final é atualizada com os valores distancia(origem,destino)

                    matriz_distancias_iteracao_atual[origem][destino] = matriz_distancia_iteracao_anterior[origem][destino]
                    matriz_caminhos_iteracao_atual[origem][destino] = matriz_com_caminhos_iteracao_anterior[origem][destino]
                else:

                    # Caso o custo minimo da origem ate a distancia considerando o vértice intermediario seja menor
                    # Então a matriz das distancias e dos caminhos é atualizada com 
                    # A distancia sendo a soma entre matriz_distancia_iteracao_anterior[origem][intermediario] + matriz_distancia_iteracao_anterior[intermediario][destino]
                    # E o caminho é origem- intermediario - destino

                    matriz_distancias_iteracao_atual[origem][destino] = matriz_distancia_iteracao_anterior[origem][intermediario] + matriz_distancia_iteracao_anterior[intermediario][destino]
                    matriz_caminhos_iteracao_atual[origem][destino] = matriz_com_caminhos_iteracao_anterior[intermediario][destino]
                ## Após realizar o cálculos dos novos pesos e também determinar os melhores caminhos para a iteração atual
                # As matrizes devem ser atualizadas
        for origem in range(n_vertices):
            for destino in range(n_vertices):
                matriz_distancia_iteracao_anterior[origem][destino] = matriz_distancias_iteracao_atual[origem][destino]
                matriz_com_caminhos_iteracao_anterior[origem][destino] = matriz_caminhos_iteracao_atual[origem][destino]

    
    # Para saber a distancia do vértice i até o vértice j, ou seja, o seu custo, deve-se utilizar a matriz
    # matriz_caminhos_iteracao_atual. Esta matriz ao final do programa irá conter a distâncias de todos os vértices 
    # Um exemplo: Distância para ir do vértice 2 até o vértice 6:
    # distância = matriz_caminhos_iteracao_atual[2][6]

    # A proxima etapa do código consiste em realizar todas as combinações possíveis de n cluster em t numero de vértices.
    # Desta maneira, para um conjunto de 100 vértices, todas as combinações possíveis para 5 clusters resulta em 75.287.520 
    # de conjuntos possíveis
    
    numeros = list(range(n_vertices))
    melhor_combinacao = [0,0,0,0]
    raio_resposta = 0
    for combinacao in combinations(numeros,n_clusters):
        # A primeira combinação irá conter os centróides possíveis
        # O próximo passo é:
        # Com a lista dos centróides em mãos, devo adicionar os vértices que estão mais próximos deste centroide no cluster
        # Então:
        #transformando a tupla em uma lista
        centroides_selecionados = [elemento for elemento in combinacao]
        
        raio_clusters = [0 for elemento in centroides_selecionados]
        # Adicionando o valor 0 para inicializar o raio do cluster 
        # Iterando sobre os vértices 
        for vertice in range(n_vertices):
            # Por exemplo, para o vértice 1, devo saber qual a menor distância entre os centróides selecionados
            # Assim tenho que verificar cada distância em relação ao centróide e pegar a mínima
            distancia_minima = INFINITO

            # Entrando na lista dos centroides:
            for centroide in centroides_selecionados:
                # Aqui busco a distância do vértice atual para o centróide selecionado
                distancia_temporaria = matriz_distancias_iteracao_atual[centroide][vertice]
                # Se a distancia da iteração for menor do que a distancia minima 
                # A distancia minima é atualizada. O vértice tem que pertencer ao centro de menor distância!
                if distancia_temporaria <= distancia_minima:
                    distancia_minima = distancia_temporaria
                    centroide_do_vertice = centroide
                #A iteração se repete para todos os centros. 
                # Aquele centro que possui a menor distância em relação ao vértice é cluster desse vértice.
                
            # Após a iteração entre todos os centroides irei saber em qual cluster esse vértice pertence
            #Abaixo eu armazeno a posição do centróide selecionado para aquele vértice
            posicao_do_centroide_na_lista = centroides_selecionados.index(centroide_do_vertice)
            # Após encontrar a posição do centróide
            # Devo adicionar a distancia máxima, ou seja, o raio para daquele cluster na lista dos raios
            # Então sempre verifico se para o vértice em questão, a sua distância em relação ao centro é maior do que 
            # a distância de um outro vértice que ja foi processado, pois, ao final, quero apenas a distância do vértice mais afastado
            # do centro. 
            raio_temporario = distancia_minima
            if raio_clusters[posicao_do_centroide_na_lista] <= raio_temporario:
                raio_clusters[posicao_do_centroide_na_lista] = raio_temporario

        #Então após todo o processamento queremos saber apenas qual o maior raio dentre todos os clusters
        # Ou seja o maior valor dentro da lista raio_clusters.
        #ao final o raio da solução é o maior raio entre esses clusters
        maior_raio = max(raio_clusters)

        #Devo guardar a combinação para no final conferir qual foi a combinação que gerou o resultado mais próximo do
        #esperado
        #Aqui estou comparando a resposta do raio anterior com o raio atual
        if abs(raio_solucao - raio_resposta) > abs(raio_solucao - maior_raio):
            combinacao_resposta = centroides_selecionados
            raio_resposta = maior_raio
        
        #print(f'Arquivo: {nome_do_grafo}')
        #print(f'melhor combinacao: {combinacao_resposta}')
        #print(f'raio da combinacao: {raio_resposta}')

    fim = tempo.time()
    tempo_processamento = fim-inicio
    
    arquivo_resultado = os.path.join(pasta_contendo_as_respostas,nome_do_arquivo)
    texto_resposta = f"resposta do arquivo: {nome_do_arquivo}\nmelhor combinacao: {combinacao_resposta}\nraio da combinacao: {raio_resposta}\ntempo de processamento{tempo_processamento}\n"
    with open(arquivo_resultado,'a') as arquivo_resposta:
        arquivo_resposta.writelines(texto_resposta)
    
    




#   Protti, Fábio "Implementação em Python do algoritmo de Floyd-Warshall" YouTube.
#   Disponível em: https://www.youtube.com/watch?v=FzBs8BV2oHs. Acesso em: 25 jun. 2024.



# solução zenilton... determinar os clusters e armazenar a distância apenas dos maximos para cada centroide
# entao por exemplo... centroide como vertice 1 ... vertice 2 e 6 sao mais proximos, centroide como vertice 3... vertices 4 e 5 sao mais proximos
# centroide como vertice 7, vertices 8 é mais proximo.... 
# o raio daquele cluster é a maior distancia... por isso é interessante guardar apenas a maior distancia... entao ao final o raio da solução é o maior raio entre esses 3 clusters 
# após gerar outra combinação de vértices realizar o mesmo procedimento e retirar o raio da solução...
# após isso comparar com o raio da combinação anterior, aquele que for mais proximo do resultado é a combinação que fica