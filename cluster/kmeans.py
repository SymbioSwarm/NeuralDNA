import time
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

random.seed()

# Reads a distance matrix (made in calculate_mums.rb) and return the labels of
# the distance matrix as well as the actual matrix
def read_distance_matrix(filename):
	lines = [line.rstrip('\n').split(",") for line in open(filename)]
	m = map(lambda x: x[1:],lines[1:])
	m = map(lambda x: map(lambda y: float(y),x),m)
	l = lines[0][1:]
	return l,m

# Make clusters given centers
# You add a node to a cluster if it is closest to the "center" of that cluster
# than any other "center" of the other clusters
def make_clusters(l,m,centers):
	clusters = []
	for c in centers:
		clusters.append([l[c]])
	for i in range(0,len(l)):
		if i not in centers:
			 min_c = 0
			 min_d = m[i][0]
			 for c in range(0,len(centers)):
			 	if (min_d > m[i][centers[c]]):
			 		min_c = c
			 		min_d = m[i][centers[c]]
			 clusters[min_c].append(l[i])
	return clusters

# Find a "center" of a cluster
# The center is defined as the node has the shortest average distance to
# all other nodes in the cluster
def find_center(arr,m,l):
	min_i = -1
	min_d = float("inf")
	if (len(arr) == 1):
		return arr[0]
	for i in range(0,len(arr)):
		t = 0
		for j in range(0,len(arr)):
			t += m[l.index(arr[i])][l.index(arr[j])]
		d = t/(len(arr)-1)
		if (d < min_d):
			min_d = d
			min_i = i
	return arr[min_i]

# Find new centers of all of the clusters (using find_center)
def find_centers(clusters,m,l):
	centers = []
	for cls in clusters:
		centers.append(l.index(find_center(cls,m,l)))
	return centers

# Select a random "center" for each of the regions
def get_rand_regions(l):
	centers = []
	lbs,mt = read_csv("../scraper_and_data/scraped.csv")
	ids = get_col(lbs,mt,"ID")
	regions = get_col(lbs,mt,"Region")
	h = {}
	for i in l:
		r = regions[ids.index(i)]
		h[r] = h.get(r,[])+[i]
	for k in h:
		ls = h[k]
		centers.append(l.index(ls[random.randint(0,len(h[k])-1)]))
	return centers

# Run the simplified kmeans algorithm on the data
def kmeans(l,m,k,n,rand=True):
	if rand:
		centers = random.sample(range(0,len(l)),k)
	else:
		centers = get_rand_regions(l)
	print centers
	for i in range(0,n):
		clusters = make_clusters(l,m,centers)
		centers = find_centers(clusters,m,l)
		print centers
	return clusters

# Reads a .csv file and returns the labels and the matrix
def read_csv(filename):
	lines = [line.rstrip('\n').split(",") for line in open(filename)]
	return lines[0],lines[1:len(lines)]

#Get a column from a given matrix
def get_col(labels,m,name):
	i = labels.index(name)
	return map(lambda x: x[i], m)

# Make a graph of the given clusters
def graph(clusters,m,l):
	lbs,mt = read_csv("../scraper_and_data/scraped.csv")
	ids = get_col(lbs,mt,"ID")
	regions = get_col(lbs,mt,"Region")
	region_set = list(set(regions))
	colors = ["blue","lime","red","darkorange","violet","deeppink","cyan","yellow","purple","lightseagreen"]
	G = nx.Graph()
	g_colors = []
	count = 1
	for cls in clusters:
		G = nx.Graph()
		g_colors = []
		for c in cls:
			G.add_node(c)
			g_colors.append(colors[region_set.index(regions[ids.index(c)])])
		for i in range(0,len(cls)):
			for j in range(i+1,len(cls)):
				G.add_edge(cls[i],cls[j])
		pos = nx.shell_layout(G)
		plt.subplot(5,2,count)
		count += 1
		nx.draw(G,pos,node_color=g_colors)
	plt.show()

# Read the distance matrix (CHANGE THIS TO USE A DIFFERENT MATRIX)
l,m = read_distance_matrix("pairwise_mums/level_0_1/Total_mums_length_distance.csv")
# Run kmeans and graph the given clusters
clusters = kmeans(l,m,10,10,False)
graph(clusters,m,l)