# wunderground-scraper
It is a simple wunderground history daily scraper. 

# Wunderground Scraper
###  wunderground history daily scraper for forecast
#### Develop by Drugo96

### About

The following project implements a daily weather forecast scraper from the wunderground website

### Requirements
- Python 3.7 or higher

### Instructions
Clone repository:
```
git clone https://github.com/Drugo96/wunderground-scraper.git
cd wunderground-scraper
```
Install dependency:
```
pip install -r requirements.txt
```
Run weather_scraper file with the correct with the correct parameters. The required parameters are the following three:
- airport: Airport ID used by wunderground
- states: Abbreviation of the country to which the code belongs
- years: Array of years you want to download

This is an example of how the script should be run:
```
python weather_scraper.py --airport LEVC --state ES --years 2018,2019
```
### Notes
To easily find the correct parameters to pass to the script, I suggest you search for the desired city on the 
wunderground website.
