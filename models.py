"""
放数据库相关的命令
"""
from exts import db  # 从exts.py里导入数据库对象


class Movie(db.Model):
    __tablename__ = 'douban_moviesdata'
    movie = db.Column(db.String(255), primary_key=True)
    douban_score = db.Column(db.String(255))
    actors = db.Column(db.String(255))
    directors = db.Column(db.String(255))
    douban_votes = db.Column(db.Integer)
    genre = db.Column(db.String(255))
    languages = db.Column(db.String(255))
    duration = db.Column(db.Integer)
    release_date = db.Column(db.String(255))
    storyline = db.Column(db.String(255))
    tags = db.Column(db.String(255))
    year = db.Column(db.Integer)




