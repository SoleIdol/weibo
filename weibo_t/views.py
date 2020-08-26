from flask import Blueprint, render_template, redirect, request, flash, session
from datetime import datetime

from weibo_t.models import Weibo
from user.models import User
from libs.orm import db
from libs.tools import login_required, save_file
from libs.sqltools import session_add, session_update1, session_deleter

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
            
            cr_time = datetime.now()
            up_time = datetime.now()
            weibo = Weibo(
                uid=uid, content=content, public=public,
                up_time=up_time, cr_time=cr_time
            )
            file = request.files.get('file')
            # 如果有文件就保存
            if file:
                weibo.filename = save_file(file)
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


@weibo_bp.route('/update/', methods=('POST', 'GET'))
@login_required
def update():
    if not request.args.get('wid'):
        flash('缺少必要参数')
        return redirect('/user/main_my/')
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    if not weibo:
        return redirect('/user/main_my/')
    try:
        user = User.query.filter_by(name=session.get('u_name')).one()
    except:
        flash('后台未检测到你的存在，请重新登录...')
        return redirect('/user/login/')
    if weibo.uid == user.id:
        # 你可以编辑
        if request.method == 'POST':
            weibo.content = request.form.get('content')
            weibo.up_time = datetime.now()
            weibo.public = bool(int(request.form.get('public')))
            file = request.files.get('file')
            # 如果有文件就保存
            if file:
                weibo.filename = save_file(file)
            
            if session_update1(weibo):
                flash('文章修改成功！')
            else:
                flash('文章发表失败！请检查是否遗漏重要信息...')
            return redirect('/user/main_my/')
        
        else:
            return render_template('update.html', user=user, weibo=weibo)
    else:
        flash('这不是你的文章，你不能编辑!')
        return redirect('/user/main_my/')


@weibo_bp.route('/delete/')
def delete():
    if not request.args.get('wid'):
        flash('缺少必要参数')
        return redirect('/user/main_my/')
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    session_deleter(weibo)
    flash('你的微博删除成功!')
    return redirect('/user/main_my/')
