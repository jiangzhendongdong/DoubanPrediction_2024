import pymysql

# 连接数据库
conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='douban')

# 编写查询语句
sql = "SELECT * FROM douban_moviesdata;"

# 执行查询语句
cursor = conn.cursor()
cursor.execute(sql)

# 导出结果为SQL文件
result = cursor.fetchall()
with open('output.sql', 'w',encoding='utf-8') as f:
    for row in result:
        f.write(str(row) + '\n')

# 关闭连接
cursor.close()
conn.close()