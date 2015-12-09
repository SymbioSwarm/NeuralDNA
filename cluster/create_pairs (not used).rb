def read_file(filename)
	str = ""
	File.open(filename,"r"){|file|
		file.each_line do |line|
			str += line
		end
	}
	return str
end

def  make_pairs(levels = ["0"],folder="level0",up_to=300)
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
	(0...arr.size).each do |i|
		((i+1)...arr.size).each do |j|
			s1 = read_file(arr[i]).chomp()
			s2 = read_file(arr[j]).chomp()
			File.open(folder + "/" + names[i]+"_" + names[j],"w"){|file| file.write(s1+s2)}
		end
	end
end