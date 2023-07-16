import requests
from bs4 import BeautifulSoup
import pprint

def update_url(url):
    parts = url.split('/')
    return '/'.join(parts[:3])

def scraper(url):
    list_urls = {}
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content_list = soup.find_all('div', class_="collection-item w-dyn-item w-col w-col-6")

        for item in content_list:
            date = item.find('div',class_="piece_date_style")
            summary = item.find('div',class_="piece_descr_style")
            title = item.find('div',class_="piece_name_style")
            link = item.find('a').get('href')
            # print(date.text.strip(), title.text.strip(), summary.text.strip(),update_url(url) + link, sep=' ')
            for j in range(1,len(content_list) + 1):
                list_urls[j] = {
                                'Title': title.text.strip(),
                                'Summary': summary.text.strip(),
                                'Link': update_url(url) + link,
                                'Date': date.text.strip()
                                }
                
        return pprint.pprint(list_urls)
            
    else:
        return "No Data"
    
print(scraper('https://www.dorkydata.com/dorky-blog'))
