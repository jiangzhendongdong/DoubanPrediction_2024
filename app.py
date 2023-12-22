from flask import Flask, request, render_template, url_for, redirect  # request是请求前端数据相关的包，render_template是路由映射相关的包
from flask_migrate import Migrate  # 数据库迁移相关的包
from sqlalchemy.dialects import mysql
import config  # 数据库连接相关
from exts import db  # 导入数据库对象
from models import Movie  # 导入建立的检索表
from prediction.DoubanPrediction import get_prediction_result


app = Flask(__name__, template_folder='./templates')
app.config.from_object(config)

# 把app绑定到db上
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/", methods=["POST", "GET"])  # 设置访问的域名，默认5000端口的化，访问检索页面就是127.0.0.1:5000
def get_detail():


    if request.args.get('key_word', None) == None:  # 如果没有检测到关键字提交，就停留在检索页面
        print("未传参")
        return render_template("search.html")  # 映射到检索页面
    else:  # 如果有关键词提交
        key_words = request.args.get('key_word')  # 将传来的关键词赋给key_words
        print(key_words)
        key_words = Movie.query.filter_by(movie=key_words).all()  # 在表里查询符合条件的条目赋给key_words
        print(key_words)

        prediction_results = get_prediction_result()

        return render_template("search.html", key_words=key_words, data=
        "随机森林预测评分为： " + str(prediction_results))
        # + "--------" + "xgbboost预测评分为： " + str(prediction_results[-2])
        # + "--------" + "catboost预测评分为： " + str(round(prediction_results[-1], 3))
        # + "--------" + "lgbm预测评分为： " + str(prediction_results[-4])
        # 映射到类似与百度百科的页面，并将查询到的条目传过去



@app.route('/', methods=['POST'])  # 定义搜索结果路由
def save():
    # 获取用户输入的电影名称和豆瓣id
    movie = request.form['movie']

    # 查询数据库获取电影信息
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM douban_moviesdata WHERE movie = %s ", (movie))
    movie_info = cur.fetchone()
    cur.close()

    if movie_info:
        return render_template('search.html', movie=movie_info)
    else:
        # 调用爬虫模块爬取电影信息
        # ...

        # 保存电影信息至数据库
        # ...

        return redirect(url_for('error'))


@app.route('/', methods=['POST'])
def search():
    movie = request.form.get('movie')
    actors = request.form.get('actors')
    directors = request.form.get('directors')
    douban_score = request.form.get('douban_score')
    douban_votes = request.form.get('douban_votes')
    genre = request.form.get('genre')
    languages = request.form.get('languages')
    duration = request.form.get('duration')
    release_date = request.form.get('release_date')
    storyline = request.form.get('storyline')
    tags = request.form.get('tags')
    year = request.form.get('year')

    movie = Movie(movie=movie, actors=actors, directors=directors, douban_score=douban_score,
                  douban_votes=douban_votes, genre=genre, languages=languages, duration=duration,
                  release_date=release_date, storyline=storyline, year=year, tags=tags)
    db.session.add(movie)
    db.session.commit()

    return '保存成功'


# flask db init
#
# flask db migrate
#
# flask db upgrade
if __name__ == '__main__':
    app.run(debug=True)
