import pymysql

# 连接数据库
def check_movie_exists(key_word):
    # 连接到数据库
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='douban')

    cursor = conn.cursor()

    # 查询数据库以查找电影
    cursor.execute("SELECT * FROM douban_moviesdata WHERE movie=%s", (key_word,))
    result = cursor.fetchone()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    # 如果找到电影，则返回True，否则返回False
    return result is not None
