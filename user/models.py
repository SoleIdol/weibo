# author:Sole_idol
# filename: models.py
# datetime:2020/8/22 9:38
from datetime import datetime
import random

from libs.orm import db
from libs.tools import random_zh_str, make_password
from libs.sqltools import session_add_all


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    head = db.Column(db.String(128), default='default.jpg')
    gender = db.Column(db.Enum('男', '女', '保密'), default='保密')
    n_fans = db.Column(db.Integer, default=0)
    birthday = db.Column(db.Date, default='1997-2-10')
    city = db.Column(db.String(20), default='（暂未填写）')
    reg_time = db.Column(db.DateTime, default=datetime.now())
    
    @classmethod
    def make_users(cls, num):
        users = []
        for i in range(num):
            user = cls()
            y = random.randint(2000, 2018)
            m = random.randint(1, 12)
            d = random.randint(1, 28)
            user.reg_time = '%04d-%02d-%02d' % (y, m, d)
            user.name = random_zh_str(3)
            user.password = make_password('123456')
            users.append(user)
        if session_add_all(users):
            print('多条测试用户信息创建成功！！！')
        else:
            print('多条测试用户信息创建失败！！！')
        return users
