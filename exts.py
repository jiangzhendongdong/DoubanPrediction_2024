"""
 存放数据库
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 在app.config里面设置好链接数据库的信息
# SQLAlchemy会自动读取app.config链接的数据库的信息
# db = SQLAlchemy(app)
# migrate = migrate(app,db)
#
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text("select 1"))
#         print(rs.fetchone())  # （1，）表示正常连接
