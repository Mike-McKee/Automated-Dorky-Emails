import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from time_functions import change_time
from SECRETS import database_url
from datetime import datetime

import requests
from bs4 import BeautifulSoup

def initialize_app():
    #Getting permission to access Firebase Realtime Database
    cred = credentials.Certificate("SECRETS/firebase_sdk_key.json")
    firebase_admin.initialize_app(cred,{'databaseURL':database_url.URL})

initialize_app()

def get_last_item() -> dict:
    """
    Returns a dictionary containing all items in the highest indexed DB item
    
    Return Dictionary looks like this:

        {
            'Date': 'July 28, 2023',
            'Link': 'https://dorkydata.com/dorky-blog/my-most-important-blog-post-ever',
            'Summary': '66 Days of Math and Programming -- Day 26',
            'Title': 'My Most Important Blog Post Ever',
            'ID': '30'
        }
    """
    ref = db.reference('/item_id')
    get_items = ref.order_by_key().limit_to_last(1).get()

    item_key = list(get_items.keys())[0]
    new_dict = get_items[item_key]
    dict_items = {key: new_dict[key] for key in new_dict.keys()}
    dict_items['ID'] = int(item_key)
    return dict_items

def highest_id_num(last_item: dict):
    #Returns int or str????
    """Finds greatest Index num in database"""
    return last_item['ID']

def recent_date(last_item: dict):
    """Finds most recent date for any item in database"""
    return last_item['date']

def is_date_greater(test_date: str, baseline: str) -> bool:
    """
    Compares two dates to find which is higher.
    
    Args
    ----
        --> test_date is the one you want to know is higher or lower than another
        --> baseline is found using the recent_date() function
    """

    test = datetime.strptime(test_date,'%B %d, %Y')
    # base = datetime.strptime(change_time(baseline),'%B %d, %Y')
    base = datetime.strptime(baseline, '%B %d, %Y')

    if test > base:
        return True
    else:
        return False

def update_url(url) -> str:
    """
    Removes anything that comes after the (.com) in https://dorkydata.com/dorky-blog

    Returns the following:
    ----------------------
        https://dorkydata.com
    """
    parts = url.split('/')
    return '/'.join(parts[:3])

def scraper(url: str) -> dict:
    """
    Scraps all data from blog from the start_date on.

    Args
    ----
        --> url = https://www.dorkydata.com/dorky-blog
        --> start_date = recent_date()
        --> index_start = highest_id_num() + 1

    What's collected for every blog post
    ------------------------------------
        - Title
        - Summary
        - Link (url path only)
        - Date (in format: January 1st, 2023)

    Return value --> Dictionary
    ---------------------------
    In the format:

        { Unique id (int) : {   Title: (str)
                                Summary: (str)
                                Link: (str)
                                Date: (str) }}

    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_list = soup.find_all('div', class_="collection-item w-dyn-item w-col w-col-6")

    #orders from oldest to newest
    content_list.reverse()
    
    last_item = get_last_item()
    start_index = highest_id_num(last_item) + 1
    start_date = recent_date(last_item)

    valid_items = []
    for item in content_list:
        date = item.find('div',class_="piece_date_style")

        clean_date = date.text.strip()

        test = is_date_greater(clean_date, start_date)

        if test == True:
            valid_items.append(item)

    items_to_add = {}
    for index, item in enumerate(valid_items,start=start_index):
        #Using beautiful soup to find specific div classes within the one above
        date = item.find('div',class_="piece_date_style")
        summary = item.find('div',class_="piece_descr_style")
        title = item.find('div',class_="piece_name_style")
        link = item.find('a').get('href')
        items_to_add[index] = {
                        'ID': index,
                        'title': title.text.strip(),
                        'summary': summary.text.strip(),
                        'link': update_url(url) + link,
                        'date': date.text.strip()
                        }
            
    return items_to_add

def update_firebase(data: dict):
    ref = db.reference('/')
    item_ref = ref.child('item_id')
    status_ref = ref.child('status')

    all_items = scraper('https://dorkydata.com/dorky-blog')
    last_item = get_last_item()
    start_index = highest_id_num(last_item) + 1

    for key in all_items.keys():

        item_ref.update({
            key: all_items[key]
        })

        status_data = {'ID': key, 'status': 1}
        status_ref.update({
            key: status_data
        })

if __name__ == "__main__":
    data = scraper('https://dorkydata.com/dorky-blog')
    update_firebase(data)
    # print(get_last_item())