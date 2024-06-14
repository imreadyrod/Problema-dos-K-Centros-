import numpy as np
import random

INF = 9999

def kmeans(graph, k):
    num_nodes = len(graph)

    # incializa centroids
    centroids = random.sample(range(num_nodes), k)

    clusters = {i: [] for i in range(k)}

    for i in range(num_nodes):
        min_dist = INF
        clossest_centroid = None

        for j in range(k):
            if graph[i][centroids[j]] < min_dist:
                min_dist = graph[i][centroids[j]]
                clossest_centroid = j
        clusters[clossest_centroid].append(i)

    return clusters

