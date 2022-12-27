from itertools import product

class Configuration:
    def __init__(self, dataset, c2c_distance_functions):
        self.dataset = [dataset]
        self.c2c_distance_functions = c2c_distance_functions

    def possible_combinations(self):
        result = product(self.dataset, self.c2c_distance_functions)
        result = list(result)
        
        return result