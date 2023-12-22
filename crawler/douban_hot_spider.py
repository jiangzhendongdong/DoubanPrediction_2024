import requests
import json
import time
import pandas as pd
import numpy as np


class douban(object):
    def __init__(self, url_root):
        self.page = 0
        self.url_root = url_root
        self.url = []
        self.movie_title = []
        self.movie_rate = []
        self.headers = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'},
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) '
                           'Chrome/17.0.963.12 Safari/535.11'},
            {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}
        ]

        # 定义一个函数catch_data，用于获取数据
    def catch_data(self):
        # 使用while循环，当条件为真时，执行循环体
        while True:
            # 设置requests模块的默认重试次数为5
            # requests.adapters.DEFAULT_RETRIES = 5
            # 创建一个session对象
            s = requests.session()
            # 关闭session对象保持连接
            s.keep_alive = False

            # 拼接url
            url_visit = self.url_root + '{}'.format(self.page * 20)
            # 随机等待5秒
            time.sleep(np.random.rand() * 5)
            # 发送get请求，获取json数据
            file = s.get(url_visit, headers=self.headers[self.page % len(self.headers)]).json()
            # 打印headers
            print(self.headers[self.page % len(self.headers)])
            # 页数加1
            self.page += 1
            # 获取item数量
            item_num = len(file['subjects'])
            # 如果item数量小于20，则跳出循环
            if item_num < 20:
                break
            # 遍历item
            for i in range(item_num):
                # 获取item的属性
                dict = file['subjects'][i]

                # 获取item的url
                urlname = dict['url']
                # 将url添加到url列表中
                self.url.append(urlname)

                # 获取item的标题
                title = dict['title']
                # 将标题添加到标题列表中
                self.movie_title.append(title)
                
                # 获取item的评分
                rate = dict['rate']
                # 将评分添加到评分列表中
                self.movie_rate.append(rate)

    # 定义extract函数，用于提取数据
    def extract(self):
        # 调用catch_data函数，获取数据
        self.catch_data()
        # 创建一个列表ticks，将当前时间添加到列表中
        ticks = [time.ctime()]
        # 将列表ticks转换为列表
        ticks = list(ticks)
        # 将列表ticks中的元素添加空字符串，直到列表长度等于url列表的长度
        ticks.extend([""] * (len(self.url) - len(ticks)))

        # 创建一个DataFrame，将列表ticks、self.movie_title、self.movie_rate、self.url中的元素添加到DataFrame中
        test = pd.DataFrame({'time': ticks, 'title': self.movie_title, 'rate': self.movie_rate, 'url': self.url})
        # 打印DataFrame
        print(test)
        # 创建一个字符串，将当前时间添加到字符串中，并使用正则表达式替换时间中的冒号，最后添加.csv后缀
        path = './douban_' + str(ticks[0]).replace(':', '-') + '.csv'
        # 将DataFrame保存为csv文件
        test.to_csv(path, encoding='utf-8-sig', index=False)
        # 返回保存文件的路径
        return path

def main():
    data = douban("https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=500"
                  "&page_start=")
    data.extract()

if __name__ == '__main__':
    main()


 # 这是一个关于电影信息的 JSON 对象，其中包含以下字段：

# 1. `episodes_info`：本电影的所有章节信息，目前为空字符串。
# 2. `rate`：本电影的评分，值为 "7.3"。
# 3. `cover_x`：本电影封面图片的水平尺寸，值为 2000。
# 4. `title`：本电影的标题，值为 "花月杀手"。
# 5. `url`：本电影的豆瓣页面链接，值为 "https://movie.douban.com/subject/26745332/"。
# 6. `playable`：本电影是否可播放，值为 False。
# 7. `cover`：本电影的封面图片链接，值为 "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2897460998.webp"。
# 8. `id`：本电影的 ID，值为 "26745332"。
# 9. `cover_y`：本电影封面图片的垂直尺寸，值为 3000。
# 10. `is_new`：本电影是否为最新电影，值为 False。

# 这个 JSON 对象表示一个电影的所有信息，包括评分、封面图片链接、标题等。