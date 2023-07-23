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
from datetime import datetime

def access_mysql():
    USERNAME = SECRET_PASSWORD.USERNAME
    PASSWORD = SECRET_PASSWORD.PASSWORD

    db = pymysql.connect(user=USERNAME, password=PASSWORD,
                             host='127.0.0.1',
                             database='dorky_blog_emails')
    
    return db

def update_url(url):
    """
    Removes anything that comes after the (.com) in https://dorkydata.com/dorky-blog

    Returns the following:
    ----------------------
        https://dorkydata.com
    """
    parts = url.split('/')
    return '/'.join(parts[:3])

def highest_id_num():
    db = access_mysql()

    with db:

        with db.cursor() as cursor:
            sql = """
            SELECT id FROM blog_items
            ORDER BY id DESC
            LIMIT 1
            """

            cursor.execute(sql)

            result = cursor.fetchone()
    
    return result[0]

#Can make recent_date return a string instead of a datetime object
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
        
    return result[0]

def change_time(date_):
    # date_object = date_[0]
    date_object = datetime.strftime(date_, '%B %d, %Y')
    
    return date_object

def reverse_time(date_):
    """
    Takes string with the following format: 'July 17, 2023'

    And using datetime.strptime(), we turn the string into a datetime object with the
    same format.

    Then using datetime.strftime(), we turn the datetime object back into a string but with the
    following format: 2023-07-17
    """
    date_object = datetime.strptime(date_, '%B %d, %Y')
    new_date = date_object.strftime('%Y-%m-%d')


    return new_date

def is_date_greater(test_date, baseline):
    #baseline will be recent_date() function
    #test_date will be the date we want to know whether it's higher or lower

    test = datetime.strptime(test_date,'%B %d, %Y')
    base = datetime.strptime(change_time(baseline),'%B %d, %Y')

    if test > base:
        return True
    else:
        return False

def updated_scraper(url, start_date, index_start):
    """
    start_date shoud be: recent_date()
    index_start will be one number high than the greatest value in "id" column
    """

    dict_of_data = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_list = soup.find_all('div', class_="collection-item w-dyn-item w-col w-col-6")
    content_list.reverse()

    valid_items = []
    for item in content_list:
        date = item.find('div',class_="piece_date_style")

        clean_date = date.text.strip()

        test = is_date_greater(clean_date, recent_date())

        if test == True:
            valid_items.append(item)
    
    #So far, everything above works

    for index, item in enumerate(valid_items,start=index_start+1):
        date = item.find('div',class_="piece_date_style")
        summary = item.find('div',class_="piece_descr_style")
        title = item.find('div',class_="piece_name_style")
        link = item.find('a').get('href')

        dict_of_data[index] = {
                        'Title': title.text.strip(),
                        'Summary': summary.text.strip(),
                        'Link': update_url(url) + link,
                        'Date': date.text.strip()
                        }
        
    return dict_of_data

def insert_into_mysql(dict):
    db = access_mysql()

    with db:
        with db.cursor() as cursor:

            for key in dict.keys():
                new_key = dict[key]

                # Removes any instance of ' in the string
                title = new_key['Title'].replace("'", "''")
                summary = new_key['Summary'].replace("'", "''")
                
                link = new_key['Link']
                date = reverse_time(new_key['Date'])

                # SQL code within the f string
                sql = f"""
                INSERT INTO blog_items (id, title, summary, link, blog_post_date)
                VALUES ({key},'{title}','{summary}','{link}','{date}')
                """

                cursor.execute(sql)
            cursor.close()

        db.commit()
    
    print("====================DATA SUCCESSFULLY ADDED TO TABLE====================")


def main(url):
    data = updated_scraper(url,recent_date(),highest_id_num())

    return insert_into_mysql(data)



main('https://www.dorkydata.com/dorky-blog')

