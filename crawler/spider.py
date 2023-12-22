import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
response = requests.get("https://movie.douban.com/top250",headers=headers)
html = response.text
soup = BeautifulSoup(html,"html.parser")
all_titles = soup.findAll("span",attrs={"class":"title"})
for title in all_titles:
    title_string = title.string
    if "/" not in title_string:
        print(title_string)


# 定义数据收集函数
# 使用爬虫模块爬取最新的未上映电影信息
# ...
#
# 将电影信息保存至 MySQL 数据库
# ...
