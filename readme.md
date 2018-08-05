# IPE Top Asset Manager PDF to CSV

This script downloads the [Top 400 Asset Managers from IPE][1] and converts it to a CSV file. 

Requirements:
* Python 3 (I used Anaconda 3)
* requests
* pdfminer
* unidecode

### How to use
1. You can directly use the csv file in the repo.

### How to use (if the pdf has been updated, and the csv hasn't)
1. `python -m pip install -r requirements.txt`
2. `python test.py`
3. output.csv should be updated

[1]: http://www.ipe.com/Uploads/k/x/x/Top-400-Ranking.pdf