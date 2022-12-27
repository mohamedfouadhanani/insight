import numpy as np

def similarity(point_1, point_2):  
    # result = sum([x_1 == x_2 for x_1, x_2 in zip(point_1, point_2)])
    # result = np.random.randint(0, 10)
    # result = 1
    result = np.sum(np.array(point_1) == np.array(point_2))
    
    return result

def minimal_distance(distance_function):
    def compute_distance(cluster_1, cluster_2):
        """computes the minimal distance between two clusters"""
        minimal_distance = float("+inf")

        for point_1 in cluster_1.points:
            for point_2 in cluster_2.points:
                distance = distance_function(point_1, point_2)

                if distance < minimal_distance:
                    minimal_distance = distance

        return minimal_distance
    
    return compute_distance

def maximal_distance(distance_function):
    def compute_distance(cluster_1, cluster_2):
        """computes the maximal distance between two clusters"""
        maximal_distance = float("-inf")

        for point_1 in cluster_1.points:
            for point_2 in cluster_2.points:
                distance = distance_function(point_1, point_2)

                if distance > maximal_distance:
                    maximal_distance = distance

        return maximal_distance
    
    return compute_distance

def mean_distance(distance_function):
    def compute_distance(cluster_1, cluster_2):
        """computes the mean distance between two clusters"""
        distance = 0

        for point_1 in cluster_1.points:
            for point_2 in cluster_2.points:
                distance += distance_function(point_1, point_2)
        
        distance /= len(cluster_1) * len(cluster_2)

        return distance
    
    return compute_distance
