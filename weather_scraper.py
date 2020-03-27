from selenium import webdriver
import json
import pandas as pd
from datetime import datetime
import os
import argparse

##This method allows you to scrap daily weather forecasts from wunderweather website (table in page history)
def scraping_data(years, airport, state):
    driver = webdriver.Chrome("chromedriver.exe")

    if not os.path.exists('forecasts/'+airport):
        try:
            os.makedirs('forecasts/'+airport)
        except OSError:
            print(OSError.args)

    for year in years:
        for m in range(1,13):
            if (m == 11 or m == 9 or m == 4 or m == 6):
                for d in range(1, 31):
                    url = 'https://api.weather.com/v1/location/'+airport.upper()+':9:'+state.upper()+'/observations/historical.json?apiKey=6532d6454b8aa370768e63d6ba5a832e&units=e&startDate='+ str(year) + str(
                        m).zfill(2) + str(d).zfill(2)
                    driver.get(url)
                    t = json.loads(driver.find_element_by_tag_name('pre').text)
                    with open('forecasts/'+airport+'/forecasts_' + str(m).zfill(2) + '_' + str(d).zfill(2) + '_' + str(
                            year) + '.json', 'w') as json_file:
                        json.dump(t, json_file)

            if (m == 2):
                for d in range(1, 29):
                    url = 'https://api.weather.com/v1/location/' + airport.upper() + ':9:' + state.upper() + '/observations/historical.json?apiKey=6532d6454b8aa370768e63d6ba5a832e&units=e&startDate=' + str(
                        year) + str(m).zfill(2) + str(d).zfill(2)
                    driver.get(url)
                    t = json.loads(driver.find_element_by_tag_name('pre').text)
                    with open('forecasts/'+airport+'/forecasts_' + str(m).zfill(2) + '_' + str(d).zfill(2) + '_' + str(
                            year) + '.json', 'w') as json_file:
                        json.dump(t, json_file)

            elif (m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12):
                for d in range(1, 32):
                    url = 'https://api.weather.com/v1/location/' + airport.upper() + ':9:' + state.upper() + '/observations/historical.json?apiKey=6532d6454b8aa370768e63d6ba5a832e&units=e&startDate=' + str(
                        year) + str(m).zfill(2) + str(d).zfill(2)
                    driver.get(url)
                    t = json.loads(driver.find_element_by_tag_name('pre').text)
                    with open('forecasts/'+airport+'/forecasts_' + str(m).zfill(2) + '_' + str(d).zfill(2) + '_' + str(
                            year) + '.json', 'w') as json_file:
                        json.dump(t, json_file)

##Convert downloaded json into one csv file
def create_csv_data(years, airport, state):
    for year in years:
        data = json.load(open('forecasts/' + airport + '/forecasts_01_01_' + str(year) + '.json'))
        df = pd.DataFrame(data["observations"])
        for m in range(2,13):
            if (m == 11 or m == 9 or m == 4 or m == 6):
                for d in range(1, 31):
                 file = 'forecasts/'+airport+'/forecasts_' + str(m).zfill(2) + '_' + str(d).zfill(2) + '_' + str(
                                year) + '.json'
                 data = json.load(open(file))
                 df = df.append(pd.DataFrame(data["observations"]))
            if (m == 2):
                for d in range(1, 29):
                    file = 'forecasts/'+airport+'/forecasts_' + str(m).zfill(2) + '_' + str(d).zfill(2) + '_' + str(
                                year) + '.json'
                    data = json.load(open(file))
                    df = df.append(pd.DataFrame(data["observations"]))
            elif(m==1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12 ):
                for d in range(1, 32):
                    file = 'forecasts/'+airport+'/forecasts_' + str(m).zfill(2) + '_' + str(d).zfill(2) + '_' + str(
                                year) + '.json'
                    data = json.load(open(file))
                    df = df.append(pd.DataFrame(data["observations"]))

    ##Set the columns of the table to keep (in this case  (expire_time_gmt and temp)
    #new_df = df[['expire_time_gmt','temp']]
    new_df = df
    ##Format date column
    new_df['expire_time_gmt'] = new_df['expire_time_gmt'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%d-%m-%Y %H:%M:%S'))
    #Rename columns names
    #new_df.columns = ['Data', 'Temperatura']
    new_df.to_csv(r'Forecasts.csv', index=False, header=True)



def main():
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("--airport",  required=True, help="Airport ID")
    ap.add_argument("--state", required=True, help="State code")
    ap.add_argument("--years", required=True, help="Years array")
    args = vars(ap.parse_args())

    ## set wunderweather AIRPORT  ID and STATE
    airport = args['airport']
    state = args['state']

    ##Set array of year
    years = args['years'].split(',')

    ##Scraping dei dati
    print("Start scrapring data")
    scraping_data(years=years, airport= airport, state= state)
    print("\n End scrapring data")

    ##Parsing dei dati e conversione in svg
    print("\n Start to create csv file")
    create_csv_data(years=years, airport=airport, state=state)
    print("\n End to create csv file")

#Run main
if __name__ == '__main__':
    main()