import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# reads the .csv file and returns the labels and the matrix
def read_csv(filename):
	lines = [line.rstrip('\n').split(",") for line in open(filename)]
	return lines[0],lines[1:len(lines)]

# Gets a column from a matrix
def get_col(labels,m,name):
	i = labels.index(name)
	return map(lambda x: x[i], m)

# Reads a upgma cluster file (created in upgma.rb)
def read_cluster(filename):
	lines = [line.rstrip('\n').split(" ") for line in open(filename)]
	return lines

# Read the scraped data file and upgma files
l,m = read_csv("../scraper_and_data/scraped.csv")
ids = get_col(l,m,"ID")
regions = get_col(l,m,"Region")
arr,_ = read_csv("pairwise_mums/level_0/Num_Mums_distance.csv")
arr = arr[1:]
edges = read_cluster("pairwise_mums/level_0/Num_Mums_upgma.txt")

# Set region colors
region_set = list(set(regions))
colors = ["blue","lime","red","darkorange","violet","deeppink","cyan","yellow","purple","lightseagreen"]

# Create a graph from the upgma file
G = nx.Graph()
g_colors = []
for node in arr:
    G.add_node(node)
    g_colors.append(colors[region_set.index(regions[ids.index(node)])])

# show each step of upgma
for edge in edges:
	G.clear()
	for i in range(0,len(edge)):
		for j in range(i+1,len(edge)):
			G.add_edge(edge[i],edge[j])
	plt.clf()
	nx.draw(G,node_color=g_colors)
	plt.show()
	time.sleep(0.1)
