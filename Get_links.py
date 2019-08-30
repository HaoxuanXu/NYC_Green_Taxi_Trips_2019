import requests
import pandas as pd
from bs4 import BeautifulSoup


year_range = ['2019']
url = "https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

def get_data_links(year_range, url, link_list = []):
    page = requests.get(url, headers = headers)
    if page.status_code == 200:
        print('Connection Established...')

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


green_taxi_data_links = get_data_links(year_range, url)


green_taxi_data_links.to_csv('../NYC_Green_Taxi_Trips_2019/data/Links/NYC_Green_taxi_Data_Link.csv', index = False)


def get_documentation_links(url, prefix):
    page = requests.get(url, headers=headers)
    if page.status_code == 200:
        print("Connection Established...")

    soup = BeautifulSoup(page.content, 'html.parser')
    tags_list = []
    for tags in soup.find_all('ul')[-3:-1]:
        tags_list.append(tags.find_all('li'))
    tags = [item for list_ in tags_list for item in list_]
    documentation_links = [a_tags.find('a')['href'] for a_tags in tags]
    aws_links = [link for link in documentation_links if ('amazonaws' in link)]
    doc_links = [link for link in documentation_links if not ('amazonaws' in link)]
    doc_links = [prefix+link for link in doc_links]

    return aws_links, doc_links

aws_links, doc_links = get_documentation_links(url=url, prefix='www1.nyc.gov')
aws_links = pd.DataFrame(aws_links, columns = ['Document Links'])
doc_links = pd.DataFrame(doc_links, columns=['Document Links'])
aws_links.to_csv('../NYC_Green_Taxi_Trips_2019/data/Links/Tabular Documentation Links.csv', index=False)
doc_links.to_csv('../NYC_Green_Taxi_Trips_2019/data/Links/Data Dictionary and Reference Links.csv', index=False)