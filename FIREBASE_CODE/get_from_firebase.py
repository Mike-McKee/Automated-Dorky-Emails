import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import SECRET_PASSWORD
import pymysql
from SECRETS import database_url
from time_functions import change_time

def get_data():
    #Getting permission to access Firebase Realtime Database
    cred = credentials.Certificate("SECRETS/firebase_sdk_key.json")
    firebase_admin.initialize_app(cred,{'databaseURL':database_url.URL})

    ref = db.reference('/')
    user_ref = ref.child('item_id')
    # status_ref = ref.child('status')
    data = user_ref.get()

    dict = {}
    for item in data:
        if item is not None:
            dict[item['ID']] = item
    
    return dict

db_data = get_data()
for key,value in db_data.items():
    print(key, value)
