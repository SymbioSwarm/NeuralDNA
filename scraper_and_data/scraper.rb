# A user needs to call three functions to download all of the data needed.
# (First get the table data by manually running the javascript in the console)
# First run get_and_write_url() to find the next url (I made a mistake here so this is why we have the next function call)
# Since I accidentily found the wrong url, you need to pull the information 
# from the url and create a new url that points to the genome sequence page.
# That function call is change_urls().
# Once you have all of the urls you need you can save the sequence files using
# get_genomes().

# Notes on the parameters of the function and how to run this:
# The "level" numbers correspond to the colors in the Plants-Species-Origins file
# level 0 = Green, level 1 = White, level 2 = Yellow, level 3 = Red, level 4 = Purple,
# level 5 = in the database but not in the list, level 6 = yellow with no region label

require 'open-uri';
require 'csv';

def get_next_link(url)
	file = open(url);
	contents = file.read;
	nurl = 'http://www.ncbi.nlm.nih.gov'
	if (contents =~ /(\/nuccore\/\d+\?report=fasta)/)
		nurl += $1
	else puts "no" end
	# puts contents;
	file.close();
	return nurl;
end

def save_file(url,id,level="0")
	file = open(url)
	contents = file.read;
	File.open("scraped_genomes/level_" + level + "/" + id, "w"){ |file|
		file.write(contents)
	}
	file.close();
end

def get_genomes(from=1,to=627,level="0",filename="scraped.csv")
	arr = CSV.read(filename)
	print "searching"
	(from...to).each do |i|
		if (arr[i][8] == level)
			print " found\n"
			if (arr[i][11] != nil && !File.exists?("scraped_genomes/level_" + level + "/" + arr[i][0]))
				save_file(arr[i][11],arr[i][0],level)
				puts ("done " + arr[i][0])
				print "sleeping "
				sleep(10)
			else
				print "nevermine"
			end
			print " continue"
			print " searching"
		end
	end
	print "\n finished"
end

def get_all_next_urls_from_csv(from=1,to=627,level="0",filename = "scraped.csv")
	arr = CSV.read(filename)
	print "searching"
	(from...to).each do |i|
		if (arr[i][8] == level)
			print " found\n"
			if (arr[i][10] == nil)
				link = get_next_link(arr[i][2])
				arr[i][10] = link
				puts ("done " + i.to_s)
				print "sleeping "
				sleep(10)
			else
				print "nevermind"
			end
			print " continue"
			print " searching"
		end
	end
	print "\n finished"
	return arr
end

# Oops...actually needed a different url. Lets change current url to new one
def change_urls(filename="scraped.csv",nfilename="new_scraped.csv")
	arr = CSV.read(filename)
	(0...arr.size).each do |i|
		if (arr[i][10] != nil && arr[i][11] == nil)
			if (arr[i][10] =~ /http:\/\/www\.ncbi\.nlm\.nih\.gov\/nuccore\/(\d+)\?report=fasta/)
				arr[i][11] = "http://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?val=" + $1 + "&db=nuccore&dopt=fasta&extrafeat=0&fmt_mask=0&maxplex=1&sendto=t&withmarkup=on&log$=seqview&maxdownloadsize=1000000"
			else
				puts "nope"
			end
		end
	end
	write_to_csv(arr,nfilename)
end

def write_to_csv(data,filename = "new_scraped.csv")
	CSV.open(filename, "wb") do |csv|
	  	data.each {|x| csv << x}
	end
end

def get_and_write_next_url(from = 1, to=627,level="0",filename = "scraped.csv", nfilename = "new_scraped.csv")
	arr = get_all_next_urls_from_csv(from,to,level,filename)
	write_to_csv(arr,nfilename)
end
# puts get_next_link('http://www.ncbi.nlm.nih.gov/genome/37072?genome_assembly_id=229804')