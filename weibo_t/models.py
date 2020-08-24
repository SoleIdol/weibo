from libs.orm import db
from datetime import datetime


class Weibo(db.Model):
    __tablename__ = 'weibo'
    
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    u_name = db.Column(db.String(10))
    title = db.Column(db.String(30))
    content = db.Column(db.Text, nullable=False)
    zan_num = db.Column(db.Integer)
    up_time = db.Column(db.DateTime, default=datetime.now())


class Message(db.Model):
    __tablename__ = 'message'
    
    id = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer)
    iid = db.Column(db.Integer)
    yid = db.Column(db.Integer)
    content = db.Column(db.Text, nullable=False)
    up_time = db.Column(db.DateTime, default=datetime.now())
