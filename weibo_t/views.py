from flask import Blueprint, render_template, redirect, request, flash, session
from datetime import datetime

from weibo_t.models import Weibo
from user.models import User
from libs.orm import db
from libs.tools import login_required, save_file
from libs.sqltools import session_add

weibo_bp = Blueprint('weibo', __name__, url_prefix='/weibo/')
weibo_bp.template_folder = './templates'
weibo_bp.static_folder = '../static'


@weibo_bp.route('/edit/', methods=('POST', 'GET'))
@login_required
def edit():
    try:
        user = User.query.filter_by(name=session.get('u_name')).one()
    except:
        flash('后台未检测到你的存在，请重新登录...')
        return redirect('/user/login/')
    if session.get('u_name'):
        if request.method == 'POST':
            uid = User.query.filter_by(name=session.get('u_name', '')).one().id
            content = request.form.get('content', '')
            if not content:
                flash('文章内容不能为空！')
                return render_template('edit.html', title='微博编辑', user=user)
            public = bool(int(request.form.get('public')))
            file = request.files.get('file')
            filename = save_file(file)
            cr_time = datetime.now()
            up_time = datetime.now()
            weibo = Weibo(
                uid=uid, content=content, public=public, filename=filename,
                up_time=up_time, cr_time=cr_time
            )
            if session_add(weibo):
                flash('文章发表成功！')
                return redirect('/user/main_my/')
            else:
                flash('文章发表失败！请检查是否遗漏重要信息...')
                return render_template('edit.html', title='微博编辑', user=user)
        else:
            return render_template('edit.html', title='微博编辑', user=user)
    else:
        flash('你还没有登录，请先登录...')
        return redirect('/user/login/')


@weibo_bp.route('/update/')
@login_required
def update():
    return '编辑'
