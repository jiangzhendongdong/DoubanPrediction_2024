from bs4 import BeautifulSoup
from crawler.before.manager import Manager
from crawler.before.downloader import *
from crawler.parser import *
from crawler.before.processor import *
import re
from crawler.TextAnalyse.NLP import SQLAnalyse, worldCloudCreate
import random
import time
import os
import math
import requests
from Prediction.prediction_main import *
import numpy as np

def fit(data_x, data_y):
    m = len(data_y)
    x_bar = np.mean(data_x)
    var = np.var(data_y)
    sum_yx = 0
    sum_x2 = 0
    for i in range(m):
        x = data_x[i]
        y = data_y[i]
        sum_yx += y * (x - x_bar)
        sum_x2 += x ** 2
    # 根据公式计算w
    w = sum_yx / (sum_x2 - m * (x_bar ** 2))
    if math.isnan(w) == True:
        w = '0'
    return w, var

def purge(dir, pattern):
    print(pattern)
    for f in os.listdir(dir):
        print(f)
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))

class Crawler(object):
    movie_id = 0
    base_url = 'https://movie.douban.com/subject/{}/comments?start=300&limit=20&status=P&sort=new_score'.format(movie_id)
    review_base_url = 'https://movie.douban.com/subject/{}/reviews'.format(movie_id)

    def __init__(self):
        self._processor = Processor()
        self._processor2 = Processor()

    def short_comment_get(self, urls):
        number = 0
        # self.SimilarMovies() # 如果需要更新相关电影，再启动这个函数
        '''
        with open("document/breaking_point.txt", "r+", encoding = "utf-8") as b:
            temp = b.readline()
            if re.match(r"https://.*", temp):
                new_url = temp
                print("url修改为断点", new_url)
                urls[0] = new_url
            b.close()
        '''
        self._manager.append_new_urls(urls, self.base_url)

        print(urls)
        self._processor.cursor.execute("select count(*) from short_comments where ID='" + self.movie_id + "'")
        count = self._processor.cursor.fetchall()[0]
        count = int(int(count[0]) / 20)
        print(count)
        while self._manager.has_new_url() and count < 15:
            count += 1
            time.sleep(random.randint(1, 5))
            new_url = self._manager.get_new_url()
            print('开始下载第{:03}个URL：{}'.format(number, new_url))
            html = download(new_url)
            if html is None:
                # print('html is empty .')
                continue
            links, results = parse(html, new_url)
            print("下一页的url是", links)
            if len(links) > 0:
                self._manager.append_new_urls(links, self.base_url)
            if len(results) > 0:
                for result in results:
                    self._processor.Commment(user_name=result['author'],
                                             user_url=result['user_url'],
                                             user_ID=result['user_ID'],
                                             user_comment=result['comment'],
                                             user_score=result['star'],
                                             ID=self.movie_id) # user_name, user_url, user_ID, user_comment,user_score, ID
            number += 1

        return number

    def long_comment_get(self, urls):
        number = 0
        self._manager.append_new_urls(urls, self.review_base_url)

        print(urls)
        self._processor.cursor.execute("select count(*) from long_comments where ID='" + self.movie_id + "'")
        count = self._processor.cursor.fetchall()[0]
        count = int(int(count[0]) / 20)
        print(count)
        while self._manager.has_new_url() and count < 15:
            count += 1
            time.sleep(random.randint(1, 5))
            new_url = self._manager.get_new_url()
            print('开始下载第{:03}个URL：{}'.format(number, new_url))
            html = download(new_url)
            if html is None:
                print('html is empty .')
                continue
            links, results = Reviews(html, new_url, self.movie_id)
            print("下一页的url是", links, results)
            if links != 0:
                if len(links) > 0:
                    self._manager.append_new_urls(links, self.review_base_url)
                if len(results) > 0:
                    for result in results:
                        self._processor.ReviewComment(user_name=result['author'],
                                                      user_url=result['user_url'],
                                                      user_ID=result['user_ID'],
                                                      user_score=result['star'],
                                                      ID=self.movie_id)  # user_name, user_url, user_ID, user_comment,user_score, ID
                number += 1
        self._processor.cursor.execute("select user_score from long_comments")
        scores = self._processor.cursor.fetchall()
        avg_score = 0
        for score in scores:
            # print(score)
            score = float(score[0])
            avg_score += score
        return avg_score / len(scores)


    def DoubanHistoryMovie(self): # 从豆瓣获取电影的基本信息
        cursor = self._processor2.connect.cursor()
        cursor.execute("select ID, name from basic_info where score is null")
        similar_name = cursor.fetchall()
        print(len(similar_name))
        for i in similar_name:
            sleep(random.randint(1, 5))
            self.movie_id = i[0]
            movie_name = i[1]
            self.base_url = 'https://movie.douban.com/subject/{}/comments?start=300&limit=20&status=P&sort=new_score'.format(self.movie_id)
            self.review_base_url = 'https://movie.douban.com/subject/{}/reviews'.format(self.movie_id)
            print("当前要爬的电影是：", movie_name, self.movie_id)
            self._manager = Manager(self.review_base_url)
            root_urls = ['?'.join([self.review_base_url, 'start=0'])]
            href = "https://movie.douban.com/subject/" + self.movie_id + "/"
            print(href)
            temp_html = download(href, web='douban')

            score, comment_num, review, tags, language, runtime, date = Score(temp_html)
            if score == -1:
                continue
            actor1, actor2, actor3, leader = ActorInfo(temp_html)
            if actor2 == -1:
                continue
            self._processor2.BasicComment(comment_num=comment_num, score=score, long_comment_num=review, tags=tags,
                                         name=movie_name, ID=self.movie_id, runtime=runtime, language=language)
            self._processor2.Actor(actor3=actor3, actor2=actor2, actor1=actor1, leader=leader, movie_name=movie_name, ID=self.movie_id)



    def testrun(self):
        '''
        self.DoubanHistoryMovie()
        self.MaoyanBoxList()
        self._processor.temp_get()
        self._processor.enviroment_tags()
        # self.MaoyanHistoryBox2()
        '''
        from threading import Thread
        update = Thread(target=self.DailyUpdate)
        update.start()
        print("线程环节测试...")

    def GetTestData(self, movie_name):
        # 输入数据：第一行第一格输入豆瓣的编号，第二行第一格输入猫眼的编号
        self._processor.cursor.execute("select ID, name, datetime, allbox, firstweekbox,"
                                       " firstdaybox, watchcount, comment_number,"
             "long_comments_number, shortemotion, longscore, score, tagscore, enviroment, isChinese,"
             "runtime, actor, threeday1, threeday2, threeday3, threeday4, threeday5 from basic_info where name='"
                                       + movie_name + "'")
        info = self._processor.cursor.fetchall()
        if len(info) > 0:
            info = info[0]

            self.movie_id = info[0]
            self.base_url = 'https://movie.douban.com/subject/{}/comments?start=0&limit=20&status=P&sort=new_score'.format(
                self.movie_id)
            print(info[0])
            self._manager = Manager(self.base_url)
            root_urls = ['?'.join([self.base_url, 'start=0'])]
            self._processor.cursor.execute("select ID from short_comments where ID='" + self.movie_id + "'")
            size = self._processor.cursor.fetchall()
            self.UpdateInfo(movie_name)
            import os
            if len(size) <= 50:
                self.short_comment_get(root_urls)
            if os.path.exists("../Prediction/static/" + self.movie_id + "_comment.jpg") == False:
                SQLAnalyse([info[0]])

            if os.path.exists("../Prediction/static/" + movie_name + ".jpg") == False:
                post_url = "https://movie.douban.com/subject/" + info[0]
                html = download(post_url)
                soup = BeautifulSoup(html, 'lxml')
                img_link = soup.find_all('img', attrs={"rel": "v:image"})
                if len(img_link) > 0:
                    img_link = img_link[0].get('src')
                    print("照片：", img_link)
                    post = requests.get(img_link)
                    img_name = "../Prediction/static/" + movie_name + ".jpg"
                    with open(img_name, 'wb') as file:  # 以byte形式将图片数据写入
                        file.write(post.content)
                        file.flush()
                    file.close()  # 关
            print(info)
            worldCloudCreate(info[0])
            f = open("../crawler/document/predict_data.csv", 'w', encoding='utf-8', newline="")
            writer = csv.writer(f)
            writer.writerow(
                ['ID', 'name', 'datetime', 'allbox', 'firstweekbox', 'firstdaybox', 'watchcount', 'comment_number',
                 'long_comments_number', 'shortemotion', 'longscore', 'score', 'tagscore', 'enviroment', 'isChinese',
                 'runtime', 'actor', 'threeday1', 'threeday2', 'threeday3', 'threeday4', 'threeday5'])
            writer.writerow(info)
            f.close()
            predict = Predict_new_movie()
            return predict

        douban, maoyan = self.Baidu(movie_name)
        if douban == -1:
            return -1
        # douban, maoyan = IDs[0], IDs[1]
        self.movie_id = douban


if __name__ == "__main__":
    crawler = Crawler()
    # crawler.UpdateInfo("我的姐姐")
    # crawler.GetTestData('哥斯拉大战金刚')
    # crawler.DailyUpdate()
    # crawler.testrun(" ")
