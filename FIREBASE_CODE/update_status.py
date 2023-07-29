import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from SECRETS import database_url

def initialize_app():
    #Getting permission to access Firebase Realtime Database
    cred = credentials.Certificate("SECRETS/firebase_sdk_key.json")
    firebase_admin.initialize_app(cred,{'databaseURL':database_url.URL})

def update_status(*indexes: int):
    status_ref = db.reference('/status')
    updates = {}
    for index in indexes:
        updates[index] = {'ID': index, 'status':0}
    status_ref.update(updates)
    
if __name__ == '__main__':
    """To test the update_status() function"""
    initialize_app()
    # for i in range(1,32):
    #     update_status(i)
