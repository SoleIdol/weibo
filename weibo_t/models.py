from libs.orm import db
from datetime import datetime


class Weibo(db.Model):
    __tablename__ = 'weibo'
    
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, index=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(256))
    zan_num = db.Column(db.Integer, default=0)
    public = db.Column(db.Boolean, default=True)  # 默认公开
    cr_time = db.Column(db.DateTime)
    up_time = db.Column(db.DateTime)


class Message(db.Model):
    __tablename__ = 'message'
    
    id = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer)
    iid = db.Column(db.Integer)
    yid = db.Column(db.Integer)
    content = db.Column(db.Text, nullable=False)
    up_time = db.Column(db.DateTime, default=datetime.now())
