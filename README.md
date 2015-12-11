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
