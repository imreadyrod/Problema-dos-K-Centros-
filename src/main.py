from read_file import read_graph_file
from floyd_warshall import build_matrix, floyd_warshall
from kmeans import kmeans

if __name__ == '__main__':
    num_nodes, num_edges, k, edges = read_graph_file('src\entradas\pmed1.txt')
    graph = build_matrix(edges, num_nodes)
    floyd_warshall(graph)
    clusters = kmeans(graph, k)

    for key, cluster in clusters.items():
        print(f'Cluster {key}: {cluster}')
