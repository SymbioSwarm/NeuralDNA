# P.L.A.N.T.
## Plant Location Analysis of Nucleotide Traits
### Programs needed
Make sure you have ruby and python installed on your computer. Also make sure MUMmer is installed.
### Scraper and data
There are two parts to run the scraper. The first part is written in javascript.
Navigate to http://www.ncbi.nlm.nih.gov/genome/browse/?report=5 and follow the instructions in scraper\_and\_data/scraper.js to download the initial .csv.
Information was added to this scraped.csv by hand. This will be used for the next part of the scraper.
The second part of the scraper uses ruby. Open ruby top level in the scraper\_and\_data/ folder. Load in scraper.rb and run
```
get_and_write_url()
```
After changing new\_scraped.csv to scraped.csv run
```
change_urls()
```
After changing new\_scraped.csv to scraped.csv run
```
get_genomes()
```
To find more information about changing the levels used and how many downloads to do at once look at scraper.rb for more options. **NOTE: Do _not_ download too many at once. Ther server will kick you out!**
### Clustering
Before calculating the mums change the line 47 in cluster/calculate\_mums.csv to the correct path to MUMmer on your computer. Open ruby top level in the cluster/ folder. Load in calculate\mums.csv and run
```
calculate_mums(["0","1"],"level_0_1")
```
This calculates all pairwise MUMs for all genomes in levels 0 and 1.
You can now create distance matrices using the MUMs. Run
```
create_distance_matrix("Num_Mums","level_0_1")
```
You can also replace "Num\_Mums" with "Total\_mums\_length".
To run kmeans and get a plot for the clutsers run the following via the command line (while in the clitser/ folder)
```
python kmeans.py
```
### Classification
