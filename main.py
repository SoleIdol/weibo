#!/usr/bin/env python

# author:Sole_idol
# filename: main.py
# datetime:2020/8/24 15:06
from flask import Flask, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from libs.orm import db
from user.views import user_bp
from weibo_t.views import weibo_bp
from user.models import User
from weibo_t.models import Weibo

app = Flask(__name__)

app.secret_key = "!@#%SDFGDSF%$^adf3465dfsdsfg567#@$^_&DG4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sole:000210wibt@localhost:3306/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
manage = Manager(app)
migrate = Migrate(app, db)
manage.add_command('db', MigrateCommand)

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(weibo_bp)


@app.route('/')
def main():
    # 联合User Weibo两个表
    weibo_user = db.session().query(User, Weibo).join(Weibo, Weibo.uid == User.id).filter().order_by(
        Weibo.up_time.desc()).all()
    
    return render_template('index.html', title='blog博客', weibo_user=weibo_user)


@manage.command
def create_test():
    """创建测试数据"""
    users = User.make_users(50)
    Weibo.make_weibo(2000, users)


if __name__ == '__main__':
    manage.run()
