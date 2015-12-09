# Cluster class holds all information about a cluster.
# Specifically it holds the id (num) of the clutser, the 
# height of the cluster (used in upgma), and the points
# that the cluster holds
class Cluster
	attr_accessor :num
	attr_accessor :indeces
	attr_accessor :height

	def initialize(num,indeces,height)
		@num = num
		@indeces = indeces
		@height = height
	end

	def distance(d,cluster,labels)
		sum = 0.0
		count = 0
		@indeces.each do |i|
			cluster.indeces.each do |j|
				sum += d[labels.index(i)][labels.index(j)]
				count += 1
			end
		end
		return sum/(cluster.indeces.size*@indeces.size)
	end
end

# Holds information about a graph:
# The nodes in the graph and the edges in the graph
class Graph
	attr_accessor :nodes
	attr_accessor :edges

	def initialize()
		@nodes = []
		@edges = {}
	end

	def addNode(n)
		@nodes << n
	end

	def addEdge(u,v,w)
		if (@edges[u] == nil)
			@edges[u] = []
		end
		if (@edges[v] == nil)
			@edges[v] = []
		end
		@edges[u] << [v,w]
		@edges[v] << [u,w]
	end

	def to_s()
		str = ""
		@nodes.each do |i|
			if (@edges[i] == nil)
				puts "ERROR"
			else
				@edges[i].each do |a|
					str += i.to_s+"->"+a[0].to_s+":"+('%.3f' % a[1])+"\n"
				end
			end
		end
		return str
	end
end

#This is used for rosalind homework only!!
def read_file(filename="upgma.in")
	count = 0
	d = []
	n = 0
	File.open(filename,"r"){|file|
		file.each_line {|line|
			if (count == 0)
				n = line.chomp.to_i
			else
				d << line.chomp.split(" ").map(&:to_f)
			end
			count += 1
		}
	}
	return n,d
end

# Crate a new distance matrix given the current clutsers
# Also return the labels of the distance matrix
def get_d_and_l(d,clusters,ls)
	labels = []
	d_new = []
	(0...clusters.size).each do |i|
		d_new[i] = []
		labels << clusters[i].num
		(0...clusters.size).each do |j|
			d_new[i][j] = clusters[i].distance(d,clusters[j],ls)
		end
	end
	return d_new,labels
end

# Find the smallest value (and its location) in the distance matrix
def find_smallest(d)
	min = d[1][0]
	min_row = 1
	min_col = 0
	(0...(d.size-1)).each do |col|
		((col+1)...d.size).each do |row|
			if (d[row][col] < min)
				min_row = row
				min_col = col
				min = d[row][col]
			end
		end
	end
	return min,min_row,min_col
end

#Runs the upgma algoritm on the distance matrix
def do_upgma(ls,d,n,max)
	order = []
	clusters = []
	graph = Graph.new()
	(0...n).each do |i|
		clusters << Cluster.new(ls[i],[ls[i]],0)
		graph.addNode(i)
	end
	count = max
	while (clusters.size > 1)
		currd,labels = get_d_and_l(d,clusters,ls)
		min,i,j = find_smallest(currd)
		height = min/2.0
		c_i = clusters[i]
		c_j = clusters[j]
		c_new = Cluster.new(count,(c_j.indeces+c_i.indeces).uniq,height)
		order << print_arr(c_new.indeces)
		clusters << c_new
		clusters.delete(c_i)
		clusters.delete(c_j)
		graph.addNode(c_new.num)
		graph.addEdge(c_new.num,c_j.num,c_new.height-c_j.height)
		graph.addEdge(c_new.num,c_i.num,c_new.height-c_i.height)
		count += 1
	end	
	return graph,order
end

# returns the arr in string form
def print_arr(arr)
	arr = arr.map{|x|x+1}
	arr = arr.map(&:to_s)
	return arr.join(" ")
end



# This used for rosalind homework only!!!
def do_all(filename="upgma.in")
	n,d = read_file(filename)
	g,order = do_things(d,n)
	str = g.to_s()
	File.open("upgma.out","w"){|file| file.write(str)}
	File.open("upgma_order.out","w"){|file| file.write(order.join("\n"))}
	puts str
	puts order
end

# Reads the given distance matrix in the given folder and outputs the clutsers
# in the order they appear
def read_distance_and_do_upgma(type="Num_Mums", folder="level_0")
	count = 0
	labels = []
	d = []
	File.open("pairwise_mums/"+folder+"/"+type+"_distance.csv","r"){|file|
		file.each_line {|line|
			if (count == 0)
				labels = line.chomp.split(",")
				labels = labels[1...labels.size].map(&:to_i)
			else
				temp = line.chomp.split(",").map(&:to_f)
				d << temp[1...temp.size]
			end
			count += 1
		}
	}
	max = labels.max
	
	graph,order = do_upgma(labels,d,labels.size,max)
	File.open("pairwise_mums/"+folder+"/"+type+"_upgma.txt","w"){|file|
		file.write(order.join("\n"))
	}
end