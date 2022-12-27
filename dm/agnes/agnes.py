from copy import deepcopy

from dm.agnes.cluster import Cluster


class Agnes:
    def __init__(self, c2c_distance_function):
        self.c2c_distance_function = c2c_distance_function

    def __call__(self, dataset, verbose=False):
        # step 1: init phase       
        clusters = [Cluster(points=[point]) for point in dataset]
        self.update_distances(receiving_clusters=clusters, clusters=clusters, optimize=True)

        history = {}
        index = 0

        iteration = 1

        while True:
            if verbose:
                print(f"iteration {iteration}:")
                print(f"\tn_clusters: {len(clusters)}")

            n_clusters = len(clusters)

            updated_clusters = [Cluster(points=cluster.points, id=cluster.id, distances=cluster.distances) for cluster in clusters]
            history.update({n_clusters: clusters})
            clusters = updated_clusters
            
            if n_clusters == 1:
                break
            # steps 2, 3: find tuples (cluster_i, cluster_j) of clusters to be
            # merged
            # close clusters = (cluster_i, cluster_j)
            close_clusters = self.close_clusters(clusters)

            # steps 4, 5: merge clusters and remove duplicates
            receiving_clusters, away_clusters = self.merge_close_clusters(close_clusters)
            clusters = [cluster for cluster in clusters if cluster not in away_clusters]

            self.update_distances(receiving_clusters=receiving_clusters, clusters=clusters)

            iteration += 1
            index += 1

        return history
    
    def close_clusters(self, clusters):
        n_clusters = len(clusters)

        results = []
        minimal_distance = float("inf")

        for i in range(n_clusters):
            for j in range(i + 1, n_clusters):
                distance = clusters[i].distances[clusters[j].id]

                if distance < minimal_distance:
                    minimal_distance = distance
                    results = [(clusters[i], clusters[j])]
                    continue
                
                if distance == minimal_distance:
                    results.append((clusters[i], clusters[j]))

        return results

    def merge_close_clusters(self, close_clusters):
        away_clusters = []
        receiving_clusters = []

        skip = {}

        while True:
            if not close_clusters:
                break
            
            cluster_i, cluster_j = close_clusters.pop(0)

            if skip.get(cluster_i.id, False):
                continue
            
            if skip.get(cluster_j.id, False):
                continue
            
            cluster_i.merge(cluster_j)

            receiving_clusters.append(cluster_i)
            away_clusters.append(cluster_j)

            skip.update({ cluster_i.id: True })
            skip.update({ cluster_j.id: True })
        
        return receiving_clusters, away_clusters

    def update_distances(self, receiving_clusters, clusters, optimize=False):
        for i in range(len(receiving_clusters)):
            range_value = range(i + 1, len(clusters)) if optimize else range(len(clusters))

            for j in range_value:

                c_1 = receiving_clusters[i]
                c_2 = clusters[j]
                if c_1 == c_2:
                    continue

                distance = c_1.distance(c_2, self.c2c_distance_function)

                c_1.distances.update({
                    c_2.id: distance
                })

                c_2.distances.update({
                    c_1.id: distance
                })