import pymysql.cursors
from PASSWORD import SECRET_PASSWORD

def access_mysql():
    USERNAME = SECRET_PASSWORD.USERNAME
    PASSWORD = SECRET_PASSWORD.PASSWORD

    db = pymysql.connect(user=USERNAME, password=PASSWORD,
                             host='127.0.0.1',
                             database='dorky_blog_emails')
    
    return db

def create_table():

    db = access_mysql()

    with db:

        with db.cursor() as cursor:

            sql = """
            CREATE TABLE progress (
                id INT PRIMARY KEY,
                status TINYINT(1)
            )
            """

            cursor.execute(sql)

        db.commit()
    
    return "=========================SUCCESS========================="

print(create_table())