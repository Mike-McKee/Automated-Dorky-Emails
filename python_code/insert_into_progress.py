import pymysql.cursors
from PASSWORD import SECRET_PASSWORD

def access_mysql():
    USERNAME = SECRET_PASSWORD.USERNAME
    PASSWORD = SECRET_PASSWORD.PASSWORD

    db = pymysql.connect(user=USERNAME, password=PASSWORD,
                             host='127.0.0.1',
                             database='dorky_blog_emails')
    
    return db

def get_id_nums_in_blog_items():
    db = access_mysql()

    with db:
        with db.cursor() as cursor:
            sql = """
            SELECT id FROM blog_items
            """

            cursor.execute(sql)
            result = cursor.fetchall()
    
    list_of_nums = []
    
    for item in result:
        list_of_nums.append(item[0])

    return list_of_nums

def get_id_nums_in_progress():
    db = access_mysql()

    with db:
        with db.cursor() as cursor:
            sql = """
            SELECT id FROM progress
            """

            cursor.execute(sql)
            result = cursor.fetchall()
    
    list_of_nums = []
    
    for item in result:
        list_of_nums.append(item[0])

    return list_of_nums

def finding_items_to_add():
    db = access_mysql()
    ids_in_progress = get_id_nums_in_progress()
    ids_in_blog_items = get_id_nums_in_blog_items()

    to_add = [i for i in ids_in_blog_items if i not in ids_in_progress]
    
    return to_add

def insert_into_table():
    db = access_mysql()
    values_to_add = finding_items_to_add()

    with db:
        with db.cursor() as cursor:
            for item in values_to_add:
                sql = f"""
                INSERT INTO progress (id, status)
                VALUES ({item},1)
                """
                cursor.execute(sql)
        db.commit()
    
    return "==================DATA SUCCESSFULLY INSERTED INTO progress TABLE=================="


print(insert_into_table())