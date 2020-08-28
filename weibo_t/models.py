from datetime import datetime
import random

from libs.orm import db
from libs.tools import random_zh_str
from libs.sqltools import session_add_all
from user.models import User


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
    
    @property
    def zan_list(self):
        thumbs = Thumb.query.filter_by(wid=self.id).all()
        z_list = [thumb.uid for thumb in thumbs]
        return z_list
    
    @property
    def fans_list(self):
        fans = Idol.query.filter_by(idol_id=self.uid).all()
        fen_list = [fen.fans_id for fen in fans]
        return fen_list
    
    @classmethod
    def make_weibo(cls, num, list):
        weibos = []
        for i in range(num):
            weibo = cls()
            y = random.randint(2010, 2018)
            m = random.randint(1, 12)
            d = random.randint(1, 28)
            
            weibo.uid = random.choice(list).id
            weibo.content = random_zh_str(random.randint(50, 140))
            weibo.cr_time = weibo.up_time = '%04d-%02d-%02d' % (y, m, d)
            
            weibos.append(weibo)
        if session_add_all(weibos):
            print('微博测试数据创建成功！！！')
        else:
            print('微博测试数据创建失败！！！')


class Message(db.Model):
    __tablename__ = 'message'
    
    id = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer)  # 微博id
    iid = db.Column(db.Integer)  # 当前评论人id
    yid = db.Column(db.Integer)  # 评论对象的id
    content = db.Column(db.Text, nullable=False)
    up_time = db.Column(db.DateTime, default=datetime.now())  # 评论时间
    
    @property
    def y_user(self):
        return User.query.get(self.yid)
    
    @property
    def i_user(self):
        return User.query.get(self.iid)
    
    @classmethod
    def by_wid(cls, fid):
        return Weibo.query.get(fid)


class Thumb(db.Model):
    __tablename__ = 'thumb'
    
    wid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, primary_key=True)


class Idol(db.Model):
    __tablename__ = 'idol'
    
    idol_id = db.Column(db.Integer, primary_key=True)
    fans_id = db.Column(db.Integer, primary_key=True)
    
    @classmethod
    def idol_list(cls, uid):
        idols = Idol.query.filter_by(fans_id=uid).all()
        idol_l = [idol.idol_id for idol in idols]
        return idol_l
    
    @classmethod
    def fans_list(cls, idol_id):
        fans = Idol.query.filter_by(idol_id=idol_id).all()
        fans_l = [fen.fans_id for fen in fans]
        fans_user_l = User.query.filter(User.id.in_(fans_l))
        return fans_user_l
    
    
