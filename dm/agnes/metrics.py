def intracluster_distance(cluster, p2p_distance_function):
    if not cluster:
        return float("+inf")
    
    n_points = len(cluster)

    distance = 0
    for i in range(n_points):
        for j in range(i + 1, n_points):
            distance += p2p_distance_function(cluster[i], cluster[j])

    return distance


def intraclusters_distance(clusters, p2p_distance_function):
    if not clusters:
        return float("+inf")

    distance = 0
    for cluster in clusters:
        distance += intracluster_distance(cluster=cluster, p2p_distance_function=p2p_distance_function)

    return distance

def interclusters_distance(clusters, c2c_distance_function):
    if not clusters:
        return float("+inf")

    n_clusters = len(clusters)

    distance = 0
    for i in range(n_clusters):
        for j in range(i + 1, n_clusters):
            distance += c2c_distance_function(clusters[i], clusters[j])
    
    distance = distance / n_clusters

    return distance

def total_intraclusters_distance(history, p2p_distance_function):
    if not history:
        return float("+inf")

    measure = 0

    for index, clusters in history.items():
        measure_i = intraclusters_distance(clusters, p2p_distance_function)
        measure += measure_i
    
    measure = measure / len(history)
    return measure

def total_interclusters_distance(history, c2c_distance_function):
    if not history:
        return float("+inf")

    measure = 0

    for index, clusters in history.items():
        measure_i = interclusters_distance(clusters, c2c_distance_function)
        measure += measure_i
    
    measure = measure / len(history)
    return measure