"""
Here, I'm doing the following:
    -- Scraping website for blog data
    -- Accessing MySQL to find most recent date in column
    -- Using above date to scrap all data from posts after that date
    -- Finding index for last id in table to add number(s) to random table
"""

import requests
from bs4 import BeautifulSoup
import pymysql.cursors
from PASSWORD import SECRET_PASSWORD

def scraper(url):
    list_urls = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_list = soup.find_all('div', class_="collection-item w-dyn-item w-col w-col-6")

    #orders from oldest to newest
    content_list.reverse()
    
    for index, item in enumerate(content_list,start=1):
        #Using beautiful soup to find specific div classes within the one above
        date = item.find('div',class_="piece_date_style")
        summary = item.find('div',class_="piece_descr_style")
        title = item.find('div',class_="piece_name_style")
        link = item.find('a').get('href')
        list_urls[index] = {
                        'Title': title.text.strip(),
                        'Summary': summary.text.strip(),
                        'Link': update_url(url) + link,
                        'Date': date.text.strip()
                        }
            
    return list_urls

def access_mysql():
    USERNAME = SECRET_PASSWORD.USERNAME
    PASSWORD = SECRET_PASSWORD.PASSWORD

    db = pymysql.connect(user=USERNAME, password=PASSWORD,
                             host='127.0.0.1',
                             database='dorky_blog_emails')
    
    return db

def recent_date():
    db = access_mysql()

    with db:
        
        with db.cursor() as cursor:
            sql = """
            SELECT blog_post_date
            FROM blog_items
            ORDER BY blog_post_date DESC
            LIMIT 1
            """

            cursor.execute(sql)

            result = cursor.fetchone()
        
    return result

def change_time(date_):
    date_object = date_[0]
    
    return date_object.strftime('%B %d, %Y')

def main():
    return change_time(recent_date())

print(main())