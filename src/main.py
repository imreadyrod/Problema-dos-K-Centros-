from read_file import read_graph_file
from floyd_warshall import build_matrix, floyd_warshall
from kmeans import kmeans
from brute_force import brute_force
import time
import pandas as pd

if __name__ == '__main__':
    list_files = [i for i in range(1, 41)]
    # data = {
    #     'Time': [],
    #     'Radius': [],
    # }

    for i in list_files:
        print(i)
        num_nodes, num_edges, k, edges = read_graph_file(f'src\entradas\pmed{i}.txt')
        graph = build_matrix(edges, num_nodes)
        floyd_warshall(graph)

        # execute kmeans
        start = time.time()
        # clusters, radius = kmeans(graph, k)
        clusters, radius = brute_force(graph, k)
        end = time.time()

        duration = end - start

        df = pd.read_csv('brute_force.csv')

        df.loc[len(df)] = {'Radius': radius, 'Time': duration}
        # data['Radius'].append(radius)
        # data['Time'].append(duration)

        df.to_csv('brute_force.csv', index=False)

    # df = pd.DataFrame(data)
    # df.to_csv('brute_force.csv', index=False)
