import pymysql

def get_audience_from_database(movie_title):
    # 连接到数据库
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='douban')
    cursor = conn.cursor()

    # 创建一个游标对象，以便在数据库中执行SQL命令
    cursor.execute("SELECT audience FROM pre_movies WHERE movie_title = %s", (movie_title,))

    # 获取查询结果
    result = cursor.fetchone()

    # 如果查询结果存在，则返回audience，否则返回None
    if result:
        return result[0]
    else:
        return None


