import pymysql.cursors
from PASSWORD import SECRET_PASSWORD

USERNAME = SECRET_PASSWORD.USERNAME
PASSWORD = SECRET_PASSWORD.PASSWORD

db = pymysql.connect(user=USERNAME, password=PASSWORD,
                             host='127.0.0.1',
                             database='dorky_blog_emails')
                            
with db:
    with db.cursor() as cursor:
        sql = """
            CREATE TABLE `blog_items` (
                id INT PRIMARY KEY,
                title VARCHAR(100),
                summary VARCHAR(1000),
                link VARCHAR(500),
                date DATE
            )
            """
        result = cursor.execute(sql)
        print(result)

        cursor.close()

    db.commit()