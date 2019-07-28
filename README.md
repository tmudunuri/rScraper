# Results Scraper

> The Results Scraper aims to automate consolidation of examination results and aid analysis by faculty members and college administrators. The script primarily serves all 200+ affiliated colleges of Visvesvaraya Technological University, Karnataka.

- This project is aimed at easing analysis of undergraduate examination results of students of VTU.
- The Python script scrapes the VTU results page for the desrired USN range.
- The results are stored as SQLite files which can be viewed, manipulated and analysed.

#### Python Libraries : Beautiful Soup, lxml, SQLite3, re, ssl

## **Instructions**

1. Install virtualenv via pip
`$ pip install virtualenv`
2. Navigate into the directory and activate Python Virtual Environment
`$ source /bin/activate`
3. Install required dependencies
`pip install -r requirements.txt`
4. Run rScraper.py
`python rScraper.py`

### Enter the Following Details :
1. `College Rgion and ID` - Refer VTU [College Codes](http://vtu.ac.in/affiliated-institutes/)
2. `Year` - Last 2 digits of year of enrollment. *Eg. 15 for 2015*
3. `Branch` - Branch code. *Eg. CS, IS, EC*
4. `Start USN` - Starting roll number.

#### Use [SQLite Browser](https://sqlitebrowser.org/) to view DB files.
