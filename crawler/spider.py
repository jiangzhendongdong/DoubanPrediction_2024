# coding:utf-8
import argparse
import schedule
import threading
from douban_hot_spider import douban
import os
from sendEmail import sendEmail

# 创建一个参数解析器
ap = argparse.ArgumentParser()
# 添加参数，time的类型为float，默认值为24，help信息为“determin a run cycle”
ap.add_argument("-t", "--time", type=float, default=24,
                help="determin a run cycle")
# 添加参数，mail的类型为str，默认值为“Y”，help信息为“send Email?”
ap.add_argument("-m", "--mail", type=str, default="Y",
                help="send Email?")
# 添加参数，spider的类型为str，默认值为"douban"，help信息为"choose spider"
ap.add_argument("-s", "--spider", type=str, default="douban",
                help="choose spider")
# 解析参数
args = vars(ap.parse_args())



# 定义run函数
def run():
    # 如果args中的spider等于douban
    if args["spider"] == "douban":
        # 调用douban函数，获取数据
        data = Douban(
            "https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=500&page_start=")
        # 调用extract函数，获取文件路径
        filePath = data.extract()
        # 如果args中的mail等于Y
        if args["mail"] == "Y":
            # 如果文件路径存在
            if os.path.isfile(filePath):
                # 调用sendEmail函数，发送邮件
                Mail = sendEmail('418132390@qq.com', '418132390@qq.com', 'oiejpyknzivubhhb', 'smtp.qq.com', '每日豆瓣电影预测数据更新', 'ok',
                                 str('D:/2024毕业设计/代码/douban_prediction'))
                # 调用sendMail函数，发送邮件
                Mail.sendMail()
            else:
                # 如果文件路径不存在，打印提示信息
                print("%s does not exist!" % filePath)



# 定义主函数
def main():
    # 每隔args["time"]秒执行run函数
    schedule.every(1).minutes.do(run)
    # 无限循环
    while True:
        # 执行所有待执行的任务
        schedule.run_pending()



if __name__ == '__main__':
    main()
