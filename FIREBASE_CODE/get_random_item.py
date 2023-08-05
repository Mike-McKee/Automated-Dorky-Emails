import sys
import os
import random

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from SECRETS import database_url
from time_functions import change_time
from update_status import update_status



def initialize_app():
    #Getting permission to access Firebase Realtime Database
    # cred = credentials.Certificate("SECRETS/firebase_sdk_key.json")
    cred = credentials.Certificate(os.path.join(script_dir,"SECRETS/firebase_sdk_key.json"))
    firebase_admin.initialize_app(cred,{'databaseURL':database_url.URL})

initialize_app()

def get_valid_keys(data):
    dict = {}
    for item in data:
        if item is not None:
            dict[item['ID']] = item['status']

    valid_keys = []
    for key in dict:
        if dict[key] == 1:
            valid_keys.append(key)

    return valid_keys

def reset_status(status_data):
    ref = db.reference('/status')
    key_list = []
    for item in status_data:
        if item is not None:
            key_list.append(item['ID'])

    for i in key_list:
        status_data = {'ID': i, 'status': 1}
        ref.update({
            i: status_data
        })

def get_random_item():

    ref = db.reference('/')
    user_ref = ref.child('status')
    new_user_ref = ref.child('item_id')
    
    #returns all valid keys and resets status if all equal 0
    while True:
        data = user_ref.get()
        valid_keys = get_valid_keys(data)

        if not valid_keys:
            reset_status(data)
        else:
            break
    
    num = random.randint(0,len(valid_keys)-1)
    chosen_id = str(valid_keys[num])
    
    return_item = new_user_ref.order_by_key().equal_to(chosen_id).get()
    
    item_key = next(iter(return_item))
    item_data = return_item[item_key]
    
    rand_item = [item_data['ID'],item_data['date'],item_data['link'],item_data['summary'],item_data['title']]

    update_status(rand_item[0])
    
    return rand_item

if __name__ == '__main__':
    print(get_random_item())