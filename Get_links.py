import requests
import pandas as pd
from bs4 import BeautifulSoup


year_range = ['2019']
url = "https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page"

def get_links(year_range, url, link_list = []):
    page = requests.get(url)
    print(page.status_code)

    soup = BeautifulSoup(page.content, 'html.parser')

    for year in year_range:
        html = soup.find('div', attrs={'class':'faq-answers', 'id':'faq{}'.format(year)})
        a_tags = html.find_all('a')
        for tag in a_tags:
            link_list.append(tag['href'])
    link_list = [link for link in link_list if not ('fhv' in link)]
    yellow_taxi_link = [link for link in link_list if ('yellow' in link)]
    green_taxi_link = [link for link in link_list if ('green' in link)]
    yellow_taxi_data_links = pd.DataFrame(yellow_taxi_link, columns = ['Taxi Data Links'])
    green_taxi_data_links = pd.DataFrame(green_taxi_link, columns = ['Taxi Data Links'])
    return yellow_taxi_data_links, green_taxi_data_links


yellow_taxi_data_links, green_taxi_data_links = get_links(year_range, url)

yellow_taxi_data_links.to_csv('../NYC_Taxi_Trips/data/Links/NYC_Yellow_Taxi_Data_Link.csv', index = False)
green_taxi_data_links.to_csv('../NYC_Taxi_Trips/data/Links/NYC_Green_taxi_Data_Link.csv', index = False)