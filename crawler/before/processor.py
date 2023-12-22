import pymysql as py
import time
import csv
import random

class Processor(object):

    def __init__(self):
        py.install_as_MySQLdb()
        self.connect = py.connect(host="127.0.0.1",
                                 user="root",
                                 password="123456",
                                 port=3306,
                                 database="douban",
                                 charset='utf8mb4')
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.connect.close()

    def Commment(self, user_name, user_url, user_ID, user_comment, user_score, ID):
        info = str(ID) + "','" + user_name + "'," + str(user_score) \
               + ",'" + user_comment + "','" + user_url + "','" + user_ID + "')"
        print(info)
        user_time = 'null'#UserInfo(user_url)
        user_info = user_name + "','" + user_url + "','" + user_ID + "'," + user_time + ")"
        try:
            self.cursor.execute("insert ignore into short_comments(ID,user_name,user_score,user_comment, user_url, user_ID) values ('" + info)
            # self.cursor.execute("insert ignore into user_info "
            #                     "(user_name, user_url, user_ID, register_time) values ('" + user_info)
            self.connect.commit()
        except Exception as e:
            print("这次录入有点问题...")

    def BasicComment(self, ID, name, comment_num,  tags, language, runtime, score="0", long_comment_num=0):
        if score is None:
            score = "0"
        print(ID, name, comment_num,  tags, language, runtime, score, long_comment_num)
        # info = str(ID) + "','" + name + "'," + str(comment_num) + "," + str(score) + "," + str(long_comment_num) + "," + language + "," + str(runtime) + ")"
        # self.cursor.execute("insert ignore into basic_info (ID, name, "
         #                    "comment_number, score, long_comments_number, isChinese, runtime) values ('" + info)
        print("update basic_info set comment_number=" + str(comment_num) + " where ID='" + ID + "'")
        self.cursor.execute("update basic_info set comment_number=" + str(comment_num) + " where ID='" + ID + "'")
        self.cursor.execute("update basic_info set score=" + str(score) + " where ID='" + ID + "'")
        self.cursor.execute("update basic_info set long_comments_number=" + str(long_comment_num) + " where ID='" + ID + "'")
        self.cursor.execute("update basic_info set isChinese=" + str(language) + " where ID='" + ID + "'")
        self.cursor.execute("update basic_info set runtime=" + str(runtime) + " where ID='" + ID + "'")

        self.connect.commit()
        for i in tags:
            info = str(ID) + ",'" + str(i.string) + "')"
            print(info)
            self.cursor.execute("insert ignore into Tags(ID, tag) values (" + info)
            self.connect.commit()

    def ReviewComment(self, user_name, user_url, user_ID, user_score, ID):
        info = str(ID) + "','" + user_name + "'," + str(user_score) \
               + ",'" + user_url + "','" + user_ID + "')"
        print(info)
        user_time = "null"# UserInfo(user_url)
        user_info = user_name + "','" + user_url + "','" + user_ID + "'," + user_time + ")"
        try:
            self.cursor.execute("insert ignore into long_comments(ID,user_name,user_score, user_url, user_ID) values ('" + info)
            # self.cursor.execute("insert ignore into user_info "
            #                    "(user_name, user_url, user_ID, register_time) values ('" + user_info)
            self.connect.commit()
        except Exception as e:
            print("这次录入有问题...")

    def mBox(self, movie_name, mbox):
        self.cursor.execute("update basic_info set income=" + str(mbox) + " where name='"+str(movie_name)+"'")
        self.connect.commit()

    def mBoxList(self, movie_name, mbox, movie_ID, score):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(timestamp)
        info = str(movie_ID) + "','" + str(movie_name) + "','" + str(timestamp) + "'," + str(score) + "," + str(mbox) + ")"
        print(info)
        self.cursor.execute("insert into cur_income (ID, name, dates, scores, incomes) values('" + info)
        self.connect.commit()

    def Actor(self, movie_name, actor1, actor2, actor3, leader, ID):
        print(movie_name, actor1, actor2, actor3, leader, ID)
        if actor1 == -1:
            actor1 = "NULL"
        if actor2 == -1:
            actor2 = "NULL"
        if actor3 == -1:
            actor3 = "NULL"
        if leader == -1:
            leader = "NULL"
        info = ID + "','" + movie_name + "','" + actor1 + "','" + actor2 + "','" + actor3 + "','" + leader + "')"
        self.cursor.execute("insert ignore into actor(ID, name, actor1, actor2, actor3, leader) values('" + info)
        self.cursor.execute("insert ignore into actoreffect(name) values ('" + actor1 + "')")
        self.cursor.execute("insert ignore into actoreffect(name) values ('" + actor2 + "')")
        self.cursor.execute("insert ignore into actoreffect(name) values ('" + actor3 + "')")
        self.cursor.execute("insert ignore into actoreffect(name) values ('" + leader + "')")
        self.connect.commit()

    def IDChanges(self, moviename, douban, maoyan):
        info = moviename + "','" + douban + "','" + maoyan + "')"
        self.cursor.execute("insert ignore into IDchange(name, douban, maoyan) values ('" + info)
        self.connect.commit()

    def BoxList(self, name, ID, date, box):
        info = ID + "','" + name +"','" + date + "'," + box +")"
        self.cursor.execute("insert ignore into Boxdata(ID, name, date, box) values('" + info)
        self.connect.commit()

    def temp_get(self): # csv序列:ID, movie_name, score, short_comment_num, long_comment_num, short_comment_score, long_comment_score,
        # actor_score, leader_score, ,tags_score, firstday, firstweek, allbox, watch_count, datetime

        self.cursor.execute("select distinct ID from boxdata")
        IDs = self.cursor.fetchall()
        for id in IDs:
            # time.sleep(1)
            maoyan = id[0]
            self.cursor.execute("select douban, name from IDchange where maoyan='" + maoyan + "'")
            id = self.cursor.fetchall()
            if len(id) == 0:
                continue
            id = id[0]
            name = id[1]
            id = id[0]
            self.cursor.execute("select datetime from basic_info where ID='" + id + "' and threeday1 is null")
            print(name, id)
            date = self.cursor.fetchall()
            if len(date) == 0:
                continue
            date = date[0][0]
            self.cursor.execute("select box, date from boxdata where ID='" + maoyan + "' and date >= '" + date + "'")
            BOX = self.cursor.fetchall()

            count, sum = 0, 0.0
            # print(BOX)
            for i in range(len(BOX)):
                print(BOX[i][1], date, sum, float(BOX[i][0]))
                if count < 2:
                    sum += float(BOX[i][0])
                    count += 1
                else:
                    sum += float(BOX[i][0])
                    print("录入：", id, int(i/3), sum, name)
                    if int(i/3) == 0:
                        self.cursor.execute("update basic_info set threeday1 = " + str(sum) + " where ID='" + id + "'")
                    elif int(i/3) == 1:
                        self.cursor.execute("update basic_info set threeday2 = " + str(sum) + " where ID='" + id + "'")
                    elif int(i/3) == 2:
                        self.cursor.execute("update basic_info set threeday3 = " + str(sum) + " where ID='" + id + "'")
                    elif int(i/3) == 3:
                        self.cursor.execute("update basic_info set threeday4 = " + str(sum) + " where ID='" + id + "'")
                    elif int(i/3) == 4:
                        self.cursor.execute("update basic_info set threeday5 = " + str(sum) + " where ID='" + id + "'")
                    sum, count = 0.0, 0
                if i > 14:
                    break
            self.connect.commit()

    def ToCsv(self):
        self.cursor.execute("select ID, name, datetime, allbox, firstweekbox, firstdaybox, watchcount, comment_number, "
                            "long_comments_number, shortemotion, longscore, score, tagscore, enviroment, "
                            "isChinese, runtime, actor, threeday1, threeday2, threeday3, threeday4, "
                            "threeday5 from basic_info where istest is false")
        # self.cursor.execute(("select * from basic_info"))
        movies = self.cursor.fetchall()
        f = open("../crawler/document/all_data.csv", 'w', encoding='gbk', newline="")
        writer = csv.writer(f)
        writer.writerow(
            ['ID', 'name', 'datetime', 'allbox', 'firstweekbox', 'firstdaybox', 'watchcount', 'comment_number',
             'long_comments_number', 'shortemotion', 'longscore', 'score', 'tagscore', 'enviroment', 'isChinese',
             'runtime', 'actor', 'threeday1', 'threeday2', 'threeday3', 'threeday4', 'threeday5'])
        test = random.sample(movies, 20)
        for movie in movies:
            writer.writerow(movie)
        f.close()

        f = open("../crawler/document/test.csv", 'w', encoding='utf-8', newline="")
        writer = csv.writer(f)
        writer.writerow(
            ['ID', 'name', 'datetime', 'allbox', 'firstweekbox', 'firstdaybox', 'watchcount', 'comment_number',
             'long_comments_number', 'shortemotion', 'longscore', 'score', 'tagscore', 'enviroment', 'isChinese',
             'runtime', 'actor', 'threeday1', 'threeday2', 'threeday3', 'threeday4', 'threeday5'])
        for movie in test:
            writer.writerow(movie)
            # print(movie)
        f.close()


        self.cursor.execute("select ID from basic_info where tagscore = 0")
        IDs = self.cursor.fetchall()
        for id in IDs:
            self.cursor.execute("select score from tags where ID='" + id[0] + "'")
            scores = self.cursor.fetchall()
            count = 0
            for score in scores:
                count += int(score[0])
            self.cursor.execute("update basic_info set tagscore = " + str(count) + " where id = '" + id[0] + "'")
        self.connect.commit()


# temp = Processor()
#temp.enviroment_tags()