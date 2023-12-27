import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import schedule
import time
import config
import pymysql
from datasql.get_audience_from_database import get_audience_from_database
from datasql.update_movie_id import update_movie_id

# https://movie.douban.com/coming?sortby=wish&sequence=desc
# 豆瓣即将上映电影
# 定义数据库连接配置
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'douban',
}

def crawl_data():
    def save_to_mysql(data_to_insert):
        # 建立数据库连接
        conn = pymysql.connect(**db_config)

        try:
            # 创建游标对象
            cursor = conn.cursor()
            # 查询pre_movies表中是否有数据
            sql_count = "SELECT COUNT(*) FROM pre_movies"
            cursor.execute(sql_count)
            result = cursor.fetchone()[0]

            if result == 0:
                # 数据库为空，直接插入新数据
                # 执行INSERT语句，将数据插入pre_movies表
                sql_insert = "INSERT INTO pre_movies (date, movie_title, genre, country, audience) VALUES (%s, %s, %s, %s, %s)"
                cursor.executemany(sql_insert, data_to_insert)
            else:
                # 数据库不为空，根据电影名字自动更新audience
                for data in data_to_insert:
                    date, movie_title, genre, country, audience = data
                    # 执行UPDATE语句，更新指定电影的audience
                    sql_update = "UPDATE pre_movies SET audience = %s WHERE movie_title = %s"
                    cursor.execute(sql_update, (audience, movie_title))

            # 提交事务
            conn.commit()

            # 输出提示信息
            print("已成功导入数据至pre_movies表")

        except Exception as e:
            # 发生异常时回滚事务
            conn.rollback()
            print("导入数据至pre_movies表出错：", str(e))

        finally:
            # 关闭游标和数据库连接
            cursor.close()
            conn.close()

    # 将爬取到的数据存储到列表中
    data_to_insert = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    cookies = {
        'Cookie': 'll="108288"; bid=up0rofOlT4o; __yadk_uid=6Piu6D9gQlgkP4gC3hgArFi0RunP6k5T; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=DDF215CC01DBBE41F222EC90538FB2D8A|49272204d8258e96190df0b4354e4dd2; __utma=30149280.1436538775.1618204010.1618204010.1618721534.2; __utmz=30149280.1618721534.2.2.utmcsr=qdan.me|utmccn=(not set)|utmcmd=(not set)|utmctr=(not provided); __utma=223695111.1097268048.1618204010.1618204010.1618721534.2; __utmz=223695111.1618721534.2.2.utmcsr=qdan.me|utmccn=(not set)|utmcmd=(not set)|utmctr=(not provided); _pk_ref.100001.4cf6=["","",1619498308,"https://m.douban.com/"]; _pk_ses.100001.4cf6=*; __gads=ID=711c888999a2e5f0-22dfaadf9dc7003c:T=1619498309:RT=1619498309:S=ALNI_MZFOiKjGCpwqqIx_9KalMsBejTvlA; _pk_id.100001.4cf6=144675c5bcfcfa6a.1618198911.4.1619498357.1618722649.; dbcl2="226186082:B5H3Q7prE2E"'
    }
    # 发送GET请求获取网页内容
    response = requests.get("https://movie.douban.com/coming?sortby=wish&sequence=desc", headers=headers,
                            cookies=cookies)
    html_content = response.text

    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(html_content, "html.parser")

    # 定位目标<div>标签
    div_tag = soup.find("div", class_="article")

    # 定位目标<table>标签
    table_tag = div_tag.find("table", class_="coming_list")

    # 定位目标<tr>标签列表
    tr_tags = table_tag.find_all("tr", class_="")

    trs = table_tag.find_all('tr')

    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) == 5:  # 确保找到了五个td元素
            date = tds[0].text.strip()
            movie_title = tds[1].find('a').text.strip()
            genre = tds[2].text.strip()
            country = tds[3].text.strip()
            audience = tds[4].text.strip()

            # 将数据添加到列表中
            data_to_insert.append((date, movie_title, genre, country, audience))


    print(data_to_insert)
    # 调用保存函数，将数据存入MySQL数据库
    save_to_mysql(data_to_insert)
    print("自动更新豆瓣未上映电影于", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "爬取并更新至数据库")

# schedule.every(12).hours.do(job)
schedule.every(1).minutes.do(crawl_data)

while True:
    schedule.run_pending()
    time.sleep(1)

