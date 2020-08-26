# author:Sole_idol
# filename: models.py
# datetime:2020/8/22 9:38
from libs.orm import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    head = db.Column(db.String(128), default='default.jpg')
    gender = db.Column(db.Enum('男', '女', '保密'), default='保密')
    birthday = db.Column(db.Date, default='1997-2-10')
    city = db.Column(db.String(20), default='（暂未填写）')
    reg_time = db.Column(db.DateTime, default=datetime.now())
