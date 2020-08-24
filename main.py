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
    return render_template('index.html', title='blog博客')


if __name__ == '__main__':
    manage.run()
