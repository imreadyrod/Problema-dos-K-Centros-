import numpy as np
import random

INF = 9999

def kmeans(graph, k):
    # incializa centroids
    centroids = [random.randint(0, len(graph)) for _ in range(k)]

    clusters = {}
    for c in centroids:
        clusters[c] = []
    print(clusters)

    for centroid in centroids:

        for node 

    for i, node in enumerate(graph):
        smaller = INF
        index = -1
        for j, c in enumerate(centroids):
            if node[c] < smaller:
                index = j
                smaller = node[c]
        
        clusters[centroids[index]].append({'node': i, 'dist': smaller})
        print(len(clusters))
    print(len(clusters))

    # for i, v in enumerate(graph):

    #     smaller = INF
    #     index = -1

    #     for j, c in enumerate(centroids):
    #         if v[c] < smaller:
    #             smaller = v[c]
    #             index = j

    #     clusters[index].append({'node': i, 'dist': smaller})
    
    # return np.sort(centroids, axis=1), np.sort(clusters, axis=1),
    return clusters

