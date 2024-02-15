def difference(point_1, point_2):  
    result = sum([x_1 != x_2 for x_1, x_2 in zip(point_1, point_2)])
    
    return result

def minimal_distance(distance_function):
    def compute_distance(cluster_1, cluster_2):
        """computes the minimal distance between two clusters"""
        minimal_distance = float("+inf")

        for point_1 in cluster_1.points:
            for point_2 in cluster_2.points:
                distance = distance_function(point_1.sample, point_2.sample)

                if distance < minimal_distance:
                    minimal_distance = distance

        return minimal_distance
    
    return compute_distance