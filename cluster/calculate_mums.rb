#Finds all of the files that exist (in the different levels)
#Returns the names of the files (and their relative path)
#As well as the names (ids) of the genomes
def find_files(levels=["0"],up_to=300)
	arr = []
	names = []
	(0...up_to).each do |i|
		levels.each do |j|
			if (File.exists?("../scraper_and_data/scraped_genomes/level_" + j + "/"+i.to_s))
				arr << "../scraper_and_data/scraped_genomes/level_" + j + "/"+i.to_s
				names << i.to_s
			end
		end
	end
	return arr,names
end

# Finds the files that dont have any data in them
# This happened because some of the genomes were too large and so
# the scraper just labeled them as OUTPUT_TOO_BIG.
# Since there were only 4 total I just did not use them
def find_to_bigs(levels=["0"],up_to=300)
	arr,names = find_files(levels,up_to)
	to_bigs = []
	(0...arr.size).each do |i|
		File.open(arr[i],"r"){|file|
			file.each_line do |line|
				if (line.chomp == "OUTPUT_TOO_BIG")
					puts names[i]
					to_bigs << names[i]
				end
				break
			end
		}
	end
	return to_bigs
end

# Using mummer calculate all of the mums (maximal unique matches)
# for each pair of genomes
# We use this as a distance measure (See create_distance_matrix)
def calculate_mums(levels=["0"],folder="level_0",up_to=300)
	arr,names = find_files(levels,up_to)
	(0...arr.size).each do |i|
		((i+1)...arr.size).each do |j|
			if (!File.exists?("../cluster/pairwise_mums/"+ folder+"/"+names[i]+"_"+names[j]))
				system ("../../../../../MUMmer3.23/./mummer -mum " + arr[i] + " " + arr[j] + " > ../cluster/pairwise_mums/"+folder+"/" + names[i] + "_" + names[j])
			end
		end
	end

end

# Reads a mum file and returns the number of mums and the 
# added length of all the mums found.
def read_mum(filename)
	str = ""
	arr = []
	first = ""
	sum = 0
	File.open(filename,"r"){|file|
		file.each_line do |line|
			if line[0] == ">"
				first = line
			else
				temp = line.chomp.split(/\s+/).map(&:to_i)
				sum += temp[-1]
				arr << temp[-1]
			end
		end
	}

	return arr.size,sum
end

# Reads mum files and adds the information to the hash 
# (if it is not already in the hash)
def add_to_hash(h,levels=["0"],folder="level_0",up_to=300)
	_,names = find_files(levels,up_to)
	(0...names.size).each do |i|
		((i+1)...names.size).each do |j|
			if (h[names[i]+"_"+names[j]] == nil)
				x,y = read_mum("pairwise_mums/"+folder+"/"+names[i]+"_"+names[j])
				h[names[i]+"_"+names[j]] = [x,y]
			end
		end
	end
end

# Creates a .csv file that includes all of the information about
# the pair genomes from their mum files
def create_file(hash,folder="level_0",filename="mums.csv")
	str="ID1,ID2,Num_Mums,Total_mums_length\n"
	hash.each do |k,v|
		ids = k.split("_")
		str += ids[0]+","+ids[1]+","+v[0].to_s+","+v[1].to_s+"\n"
	end
	File.open("pairwise_mums/"+folder+"/"+filename,"w"){|file| file.write(str)}
end

# Reads a .csv file and returns it as a 2-dimensional array
def read_csv(filename,sep = ",")
	arr = []
	File.open(filename,"r"){|file|
		file.each_line do |line|
			arr << line.chomp.split(sep)
		end
	}
	return arr
end

#Remove any mum files that used a to_big file (see find_to_bigs for more info)
def remove_to_bigs(to_bigs,folder="level_0",filename="mums.csv",new_filename="new_mums.csv")
	arr = read_csv("pairwise_mums/"+folder+"/"+filename)
	n_arr = []
	arr.each do |a|
		if (to_bigs.index(a[0]) == nil && to_bigs.index(a[1]) == nil)
			n_arr << a
		else
			puts "removed " + a[0] + "_" + a[1]
		end
	end
	str = ""
	n_arr.each do |a|
		str += a.join(",")+"\n"
	end
	File.open("pairwise_mums/"+folder+"/"+new_filename,"w"){|file| file.write(str)}
end

def make_m_ints(m)
	return m.map{|x| x.map(&:to_i)}
end

# Since bigger numbers means that genomes are more similar, we are going to take the negatives
# To make the distance matrix work and add the max plus one.
def create_distance_matrix(type="Num_Mums",folder="level_0",filename="new_mums.csv")
	arr = read_csv("pairwise_mums/"+folder+"/"+filename)
	arr_i = make_m_ints(arr[1...arr.size])
	index = arr[0].index(type)
	firsts = arr_i.map{|x| x[0]}
	seconds = arr_i.map{|x| x[1]}
	ids = firsts+seconds
	ids.uniq!
	m = []
	(0...ids.size).each do |i|
		m[i] = []
		m[i][i] = 0
	end
	max = arr_i[0][index]
	arr_i.each do |x|
		if (max < x[index])
			max = x[index]
		end
		m[ids.index(x[1])][ids.index(x[0])] = -x[index]
		m[ids.index(x[0])][ids.index(x[1])] = -x[index]
	end
	m.map!{|x| x.map{|y| if (y != 0) then y+max+1 else y end}}

	save_matrix(ids,m,"pairwise_mums/"+folder+"/"+type+"_distance.csv")
end

#Saves the matrix in a .csv file
def save_matrix(labels,m,filename)
	str = "IDS,"+labels.map(&:to_s).join(",") + "\n"
	(0...m.size).each do |i|
		str += labels[i].to_s + "," + m[i].map(&:to_s).join(",") +"\n"
	end
	File.open(filename,"w"){|file| file.write(str)}
end