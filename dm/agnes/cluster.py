class Cluster:
	ID = 1
	def __init__(self, points=[], id=None, distances=None):
		self.id = id if id is not None else Cluster.ID
		self.points = points
		self.distances = {} if distances is None else distances

		Cluster.ID += 1 if id is None else 0
		
	def merge(self, cluster):
		self.points.extend(cluster.points)
	
	def distance(self, other, c2c_distance_function):
		result = c2c_distance_function(self, other)
		return result

	def __equals__(self, other):
		return self.id == other.id
	
	def __len__(self):
		return len(self.points)

	def __getitem__(self, index):
		return self.points[index]
	
	def __copy__(self):
		return Cluster(points=self.points.copy())

	def __repr__(self):
		cluster_points_string = ', '.join(map(str, self.points))
		return f"Cluster {self.id}: [{cluster_points_string}]"