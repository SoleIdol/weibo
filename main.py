#!/usr/bin/env python

# author:Sole_idol
# filename: main.py
# datetime:2020/8/24 15:06
from math import ceil

from flask import Flask, render_template, request, redirect, flash, session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from libs.orm import db
from user.views import user_bp
from weibo_t.views import weibo_bp
from user.models import User
from weibo_t.models import Weibo, Message

app = Flask(__name__)

app.secret_key = "!@#%SDFGDSF%$^adf3465dfsdsfg567#@$^_&DG4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://demon:123456@localhost:3306/weibo'
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
    """未登录首页"""
    
    page = int(request.args.get('page', 1))
    per_page = 30
    offset = per_page * (page - 1)
    # 联合User Weibo两个表
    weibo_user = db.session().query(User, Weibo).join(Weibo, Weibo.uid == User.id).filter().order_by(
        Weibo.up_time.desc()).limit(per_page).offset(offset).all()
    
    max_page = ceil(Weibo.query.count() / per_page)
    if max_page <= 7:
        start, end = 1, max_page
    elif page <= 3:
        start, end = 1, 7
    elif page > (max_page - 3):
        start, end = max_page - 6, max_page
    else:
        start, end = (page - 3), (page + 3)
    pages = range(start, end + 1)
    wb_list = [wu.Weibo.id for wu in weibo_user]
    # 注意，这里有个范围查询 in_()
    msgs = Message.query.filter(Message.fid.in_(wb_list)).order_by(Message.up_time.desc()).all()
    
    return render_template('index.html', title='迷你微博', weibo_user=weibo_user, msgs=msgs,
                           pages=pages, page=page, start=start, end=end, max_page=max_page)
    
    # # 联合User Weibo两个表
    # weibo_user = db.session().query(User, Weibo).join(Weibo, Weibo.uid == User.id).filter().order_by(
    #     Weibo.up_time.desc()).all()
    #
    # return render_template('index.html', title='迷你微博', weibo_user=weibo_user)


@manage.command
def create_test():
    """创建测试数据"""
    users = User.make_users(50)
    Weibo.make_weibo(2000, users)


if __name__ == '__main__':
    manage.run()
