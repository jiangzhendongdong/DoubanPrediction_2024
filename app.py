from flask import Flask, request, render_template, url_for, redirect, \
    abort, jsonify  # request是请求前端数据相关的包，render_template是路由映射相关的包
from flask_migrate import Migrate  # 数据库迁移相关的包
from sqlalchemy.dialects import mysql
import config  # 数据库连接相关
from datasql.get_paginated import get_paginated_results
from exts import db  # 导入数据库对象
from models import Movie  # 导入建立的检索表
from prediction.DoubanPrediction import get_prediction_result

app = Flask(__name__, template_folder='./templates')
app.config.from_object(config)

# 把app绑定到db上
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/", methods=["POST", "GET"])
def get_detail():
    if request.args.get('key_word', None) is None:
        print("未传参")
        return render_template("search.html")
    else:
        key_words = request.args.get('key_word')
        print(key_words)

        # 使用模糊搜索查询数据库中符合条件的电影条目
        key_words = Movie.query.filter(Movie.movie.like("%{}%".format(key_words))).all()
        print(key_words)

        # 获取分页参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))

        # 分页查询
        items, item_count, page_count = get_paginated_results(
            Movie.query.filter(Movie.movie.like("%{}%".format(key_words))), page, page_size)

        prediction_results = get_prediction_result()

        return render_template("search.html", key_words=key_words, items=items, item_count=item_count, page=page,
                               page_size=page_size, page_count=page_count ,
                               data="随机森林预测评分为： " + str(prediction_results))

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
    cur.execute("SELECT * FROM douban_moviesdata WHERE movie = %s ", movie)
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
