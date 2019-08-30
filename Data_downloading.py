import pandas as pd
import requests
from io import StringIO
import time

green_taxi_data_link = pd.read_csv('C:/Users/John Xu/Desktop/NYC_Taxi_Trips/data/Links/NYC_Green_taxi_Data_Link.csv')

green_taxi_2019_link = green_taxi_data_link[green_taxi_data_link.iloc[:,0].str.contains('2019')]


data_dict = {2019:green_taxi_2019_link}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}
def load_data(type, link_file, year, initial_iter=2):
    for link in link_file.iloc[:,0]:
        pd.read_csv(link).to_csv('../NYC_Taxi_Trips/data/Data/{} Data {}-{}.csv'.format(type, str(year), str(initial_iter)))
        print('Iteration '+str(initial_iter)+' for '+type+' is complete!')
        initial_iter += 1
        print('Process halting...')
        time.sleep(120)
        if initial_iter <= len(link_file):
            print('Begin Iteration '+str(initial_iter)+'...')
        else:
            print('Iteration for '+ type + ' Complete!!')


for keys, values in data_dict.items():
    load_data(type='Green Taxi', link_file=values, year = keys)



