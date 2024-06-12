import numpy as np
INF = 9999

def build_matrix(edges, num_nodes):
    graph = np.full((num_nodes, num_nodes), INF)

    for e in edges:
        # print(e)
        graph[e[0] - 1][e[1] - 1] = e[2]

    return graph

def floyd_warshall(graph):
    number_nodes = len(graph)

    for k in range(number_nodes):
        for i in range(number_nodes):
            for j in range(number_nodes):
                graph[i][j] = min(graph[i][j],graph[i][k] + graph[k][j])


'''
Entrada de exemplo

5
0 1 3 100 6
100 0 1 3 100
1 2 0 1 100
3 100 100 0 2
100 100 100 1 0
'''
