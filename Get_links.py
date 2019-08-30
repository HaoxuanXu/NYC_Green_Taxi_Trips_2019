import requests
import pandas as pd
from bs4 import BeautifulSoup


year_range = ['2019']
url = "https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

def get_links(year_range, url, link_list = []):
    page = requests.get(url, headers = headers)
    print(page.status_code)

    soup = BeautifulSoup(page.content, 'html.parser')

    for year in year_range:
        html = soup.find('div', attrs={'class':'faq-answers', 'id':'faq{}'.format(year)})
        a_tags = html.find_all('a')
        for tag in a_tags:
            link_list.append(tag['href'])
    link_list = [link for link in link_list if not ('fhv' in link)]
    green_taxi_link = [link for link in link_list if ('green' in link)]
    green_taxi_data_links = pd.DataFrame(green_taxi_link, columns = ['Taxi Data Links'])
    return green_taxi_data_links


green_taxi_data_links = get_links(year_range, url)


green_taxi_data_links.to_csv('../NYC_Taxi_Trips/data/Links/NYC_Green_taxi_Data_Link.csv', index = False)