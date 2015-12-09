load "../cluster/calculate_mums.rb"
require "shellwords"

def read_csv(filename)
	labels = []
	m = []
	count = 0
	File.open(filename,"r"){|file|
		file.each_line do |line|
			if (count == 0)
				labels = line.chomp.split(",")
			else
				m << line.chomp.split(",")
			end
			count += 1
		end
	}
	return labels,m
end

def get_row(name,labels,m)
	index = labels.index(name)
	if index == nil
		return nil
	end
	return m.map{|x| x[index]}
end

l,m = read_csv("../scraper_and_data/scraped.csv")
ids = get_row("ID",l,m)
regions = get_row("Region",l,m)
r_set = r.uniq - [nil]
f,m = find_files(["0","1"])
(0...f.size).each do |i|
	system ("cp " + f[i] + " region_collections/" + regions[ids.index(m[i])].shellescape + "/")
end

arr = []
(0...f.size).each do |i|
	if (regions[ids.index(m[i])] == "South/SE Asia")
		arr << m
	end
end