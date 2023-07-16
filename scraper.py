import requests
from bs4 import BeautifulSoup
import pprint

def update_url(url):
    parts = url.split('/')
    return '/'.join(parts[:3])

def scraper(url):
    list_urls = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_list = soup.find_all('div', class_="collection-item w-dyn-item w-col w-col-6")

    num = [i for i in range(1,len(content_list) + 1)]

    #TODO: figure out how to order dictionary so that we start with the oldest blog posts first

    for item in content_list:
        date = item.find('div',class_="piece_date_style")
        summary = item.find('div',class_="piece_descr_style")
        title = item.find('div',class_="piece_name_style")
        link = item.find('a').get('href')
        list_urls[num[0]] = {
                        'Title': title.text.strip(),
                        'Summary': summary.text.strip(),
                        'Link': update_url(url) + link,
                        'Date': date.text.strip()
                        }
        num.pop(0)
            
    return pprint.pprint(list_urls)

def main(url):
    return scraper(url)

print(main('https://www.dorkydata.com/dorky-blog'))
