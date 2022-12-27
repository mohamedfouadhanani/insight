from matplotlib import pyplot as plt
import colorsys

from metrics import interclusters_distance, intraclusters_distance
from distances import manhattan, minimal_distance

def HSVToRGB(h, s, v): 
	(r, g, b) = colorsys.hsv_to_rgb(h, s, v) 
	return (r, g, b)
 
def get_distinct_colors(n): 
	huePartition = 1.0 / (n + 1) 
	return [HSVToRGB(huePartition * value, 1.0, 1.0) for value in range(0, n)]

def show_clusters(history, steps):
	start = len(history) - 1
	stop = start - steps
	
	for index in range(start, stop, -1):
		clusters = history[index]

		n_clusters = len(clusters)
		colors = get_distinct_colors(n_clusters)

		for color_index, cluster in enumerate(clusters):
			X = [x for x, y in cluster.points]
			Y = [y for x, y in cluster.points]
			
			color = colors[color_index]
			plt.scatter(X, Y, color=color, label=f"cluster with id {cluster.id}")
		

		plt.title("AGNES Clustering algorithm")
		plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
		plt.tight_layout()
		plt.show()

def show_metrics(history):
	figure, axis = plt.subplots(1, 2, figsize=(10, 4), dpi=100)
	figure.tight_layout(pad=5)

	intraclusters_distances = [(index, intraclusters_distance(clusters=clusters, p2p_distance_function=manhattan)) for index, clusters in history.items()]
	X = [index for index, _ in intraclusters_distances]
	Y = [distance for _, distance in intraclusters_distances]
	axis[0].plot(X, Y, color="tab:blue")
	axis[0].set_title("intra-clusters distances")
	axis[0].set_xlabel("iteration")
	axis[0].set_ylabel("distance")
	
	interclusters_distances = [(index, interclusters_distance(clusters=clusters, c2c_distance_function=minimal_distance(distance_function=manhattan))) for index, clusters in history.items()]
	X = [index for index, _ in interclusters_distances]
	Y = [distance for _, distance in interclusters_distances]
	axis[1].plot(X, Y, color="tab:orange")
	axis[1].set_title("mean inter-clusters distances")
	axis[1].set_xlabel("iteration")
	axis[1].set_ylabel("distance")

	plt.show()