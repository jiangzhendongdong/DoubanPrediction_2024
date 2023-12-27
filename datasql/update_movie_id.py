import pymysql

def update_movie_id():
    # 连接到数据库
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='douban')
    cursor = conn.cursor()

    # 设置id为0
    cursor.execute("SET @auto_id = 0;")
    conn.commit()

    # UPDATE 表名 set id = (@auto_id := @auto_id +1);
    cursor.execute("UPDATE pre_movies set id = (@auto_id := @auto_id +1);")
    conn.commit()

    # ALTER TABLE 表名 AUTO_INCREMENT = 1;
    cursor.execute("ALTER pre_movies line AUTO_INCREMENT = 1;")
    conn.commit()

    # 关闭数据库连接
    cursor.close()
    conn.close()