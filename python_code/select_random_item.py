import pymysql.cursors
import random
from access_mysql import access_mysql
from time_functions import change_time

# Returns list of IDs from progress table where status is 1 (aka good to use)
def find_search_range():
    db = access_mysql()

    with db:
        with db.cursor() as cursor:
            sql = """
            SELECT id FROM progress
            WHERE status = 1
            """
            cursor.execute(sql)

            result = cursor.fetchall()

    available_items = []
    
    for item in result:
        available_items.append(item[0])

    return available_items

#return an integer
def pick_random_item(items):
    answer = random.randint(0,len(items)-1)
    return answer

def get_row_from_table(id):
    #id will be a random number generate form pick_random_item()
    db = access_mysql()
    with db:
        with db.cursor() as cursor:
            sql = f"""
            SELECT * FROM blog_items
            WHERE id = {id}
            """
        
            cursor.execute(sql)

            result = cursor.fetchone()
    
    id_num = result[0]
    title = result[1]
    summary = result[2]
    link = result[3]
    date = change_time(result[4])

    to_return = [id_num, title, summary, link, date]
    return to_return

def change_item_status(id):
    # id will be the random num from pick_random_item or the first item in to_return from get_row_from_table
    db = access_mysql()
    with db:
        with db.cursor() as cursor:
            sql = f"""
            UPDATE progress
            SET status = 0
            WHERE id = {id}
            """

            cursor.execute(sql)
        
        db.commit()

# Once all rows have status = 0, this function resets all values back to 1
def reset_status():
    db = access_mysql()
    with db:
        with db.cursor() as cursor:
            sql = """
            UPDATE progress
            SET status = 1
            """

            cursor.execute(sql)
        
        db.commit()

#We'll import this into the script that sends an email
def email_item():
    """
    Returns a random row from the blog_items table in MySQL
    
    Ex: [7, 'The Lazy (Yet Genius) Coder', '66 Days of Math and Programming -- Day 3', 'https://www.dorkydata.com/dorky-blog/the-lazy-yet-genius-coder', 'July 05, 2023']
    """
    search_range = find_search_range()
    
    #run when all rows have status = 0
    if search_range == []:
        #code to reset all values in status back to 1
        reset_status()

    num = pick_random_item(find_search_range())
    item = get_row_from_table(num)
    change_item_status(num)

    return item