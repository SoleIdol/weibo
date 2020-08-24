from flask import Blueprint, render_template, redirect, request, flash, session

from weibo_t.models import Weibo
from user.models import User
from libs.orm import db

weibo_bp = Blueprint('weibo', __name__, url_prefix='/weibo/')
weibo_bp.template_folder = './templates'
weibo_bp.static_folder = '../static'


@weibo_bp.route('/edit/', methods=('POST', 'GET'))
def edit():
    if session.get('u_name'):
        if request.method == 'POST':
            """
            这里填写提交的一些文件
            """
            flash('文章发表成功！')
            return redirect('/user/main_my/')
        else:
            user = User.query.filter_by(name=session.get('u_name')).one()
            return render_template('edit.html', title='微博编辑', user=user)
    else:
        flash('你还没有登录，请先登录...')
        return redirect('/user/login/')
