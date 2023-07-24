import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import SECRET_PASSWORD
import pymysql
from SECRETS import database_url
from time_functions import change_time  

def access_mysql():
    USERNAME = SECRET_PASSWORD.USERNAME
    PASSWORD = SECRET_PASSWORD.PASSWORD

    db = pymysql.connect(user=USERNAME, password=PASSWORD,
                             host='127.0.0.1',
                             database='dorky_blog_emails')
    
    return db

def get_sql_data():
    db = access_mysql()

    with db:
        with db.cursor() as cursor:
            sql = """SELECT * FROM blog_items"""

            cursor.execute(sql)

            result = cursor.fetchall()
    
    to_add = {}
    for index,item in enumerate(result,start=1):
        to_add[index] = {
            'ID': index,
            'title': item[1],
            'summary': item[2],
            'link': item[3],
            'date': change_time(item[4]),
        }         
    
    return to_add

def add_firebase():
    data = get_sql_data()
    #Getting permission to access Firebase Realtime Database
    cred = credentials.Certificate("SECRETS/firebase_sdk_key.json")
    firebase_admin.initialize_app(cred,{'databaseURL':database_url.URL})

    ref = db.reference('/')
    user_ref = ref.child('item_id')
    status_ref = ref.child('status')
    for key in data.keys():

        user_ref.update({
            key: data[key]
        })

        status_data = {'ID': key, 'status': 1}
        status_ref.update({
            key: status_data
        })

add_firebase()