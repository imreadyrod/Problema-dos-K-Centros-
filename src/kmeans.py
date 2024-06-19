import numpy as np
import random
import time

INF = 9999

def find_radius(graph, clusters):
    definitive_radius = 0
    for key, cluster in clusters.items():
        max_radius = 0
        for node in cluster:
            max_radius = max(graph[key][node], max_radius)
        definitive_radius = max(max_radius, definitive_radius)

    return definitive_radius


def update_centroids(graph, clusters):
    new_centroids = []
    for cluster in clusters.values():
        min_avg_dist = INF
        new_centroid = None
        for node in cluster:
            avg_dist = np.mean([graph[node][other] for other in cluster])
            if avg_dist < min_avg_dist:
                min_avg_dist = avg_dist
                new_centroid = node
        new_centroids.append(new_centroid)
    return new_centroids

def assign_clusters(graph, k, centroids):
    num_nodes = len(graph)
    clusters = {centroid: [] for centroid in centroids}

    for i in range(num_nodes):
        min_dist = INF
        clossest_centroid = None

        for j in range(k):
            if graph[i][centroids[j]] < min_dist:
                min_dist = graph[i][centroids[j]]
                clossest_centroid = centroids[j]
        clusters[clossest_centroid].append(i)

    return clusters

def kmeans(graph, k):
    num_nodes = len(graph)

    # incializa centroids
    centroids = random.sample(range(num_nodes), k)
    clusters = assign_clusters(graph, k, centroids)
    radius = find_radius(graph, clusters)

    best_clusters = clusters
    penalitys = 0
    while True:
        print(centroids)
        print(radius)
        new_centroids = update_centroids(graph, clusters)

        centroids = new_centroids
        clusters = assign_clusters(graph, k, centroids)
        new_radius = find_radius(graph, clusters)

        # stop the kmeans to loop infinity
        if new_radius >= radius:
            penalitys += 1
            if penalitys == k:
                break
        else:
            best_clusters = clusters
            radius = new_radius
        
    return best_clusters, radius

