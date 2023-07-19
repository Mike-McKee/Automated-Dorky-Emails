import requests
from bs4 import BeautifulSoup
import pymysql.cursors
import SECRET_PASSWORD

def update_url(url):
    """
    Removes anything that comes after the (.com) in https://dorkydata.com/dorky-blog

    Returns the following:
    ----------------------
        https://dorkydata.com
    """
    parts = url.split('/')
    return '/'.join(parts[:3])

def scraper(url):
    """
    Scrapes selected data from each blog post in the given url address.
    Intended to use with the following div class style --> class_="collection-item w-dyn-item w-col w-col-6"

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

def add_to_mysql(dict):
    """
    Accesses a MySQL database using pymysql library and inserts values from the parameter dictionary
    into the blog_items table.

    Parameter --> Dictionary
    -----------------------
    Intended to use a dictionary returned from the scraper() function above.
    """

    USERNAME = SECRET_PASSWORD.USERNAME
    PASSWORD = SECRET_PASSWORD.PASSWORD

    db = pymysql.connect(user=USERNAME, password=PASSWORD,
                             host='127.0.0.1',
                             database='dorky_blog_emails')
    
    # Establishes use of database connection that closes automatically once with statement is exited
    with db:
        # Creates a cursor that's automatically closed at end due to with statement
        with db.cursor() as cursor:

            # Iterates through every item in the parameter dicitionary
            for key in dict.keys():
                new_key = dict[key]
                
                # Removes any instance of ' in the string
                title = new_key['Title'].replace("'", "''")
                summary = new_key['Summary'].replace("'", "''")
                
                link = new_key['Link']
                date = new_key['Date']

                # SQL code within the f string
                sql = f"""
                INSERT INTO blog_items (id, title, summary, link, date)
                VALUES ({key},'{title}','{summary}','{link}','{date}')
                """
                
                # Runs the SQL code
                cursor.execute(sql)

            cursor.close()
        db.commit()

    return "DATA SUCCESSFULLY ADDED TO TABLE"

def main(url):
    return (add_to_mysql(scraper(url)))

print(main('https://www.dorkydata.com/dorky-blog'))
