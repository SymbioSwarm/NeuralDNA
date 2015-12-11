# P.L.A.N.T.
## Plant Location Analysis of Nucleotide Traits
### Programs needed
Make sure you have ruby and python installed on your computer. Also make sure MUMmer is installed.
### Scraper and data
There are two parts to run the scraper. The first part is written in javascript.
Navigate to http://www.ncbi.nlm.nih.gov/genome/browse/?report=5 and follow the instructions in scraper\_and\_data/scraper.js to download the initial .csv.
Information was added to this scraped.csv by hand. This will be used for the next part of the scraper.
The second part of the scraper uses ruby. Open ruby top level in the scraper\_and\_data/ folder. First run
'''
get_and_write_url()
'''