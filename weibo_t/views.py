from math import ceil

from flask import Blueprint, render_template, redirect, request, flash, session
from datetime import datetime
from sqlalchemy import and_

from weibo_t.models import Weibo, Message, Thumb, Idol
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
    """
    发表编辑微博
    :return:
    """
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
    """
    修改微博
    :return:
    """
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
    """
    删除微博
    :return:
    """
    if not request.args.get('wid'):
        flash('缺少必要参数')
        return redirect('/user/main_my/')
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    session_deleter(weibo)
    flash('你的微博删除成功!')
    return redirect('/user/main_my/')


@weibo_bp.route('/send_message/', methods=('POST',))
@login_required
def send_message():
    """
    评论微博
    :return:
    """
    message = Message()
    
    message.fid = int(request.form.get('m_fid'))
    message.iid = int(request.form.get('m_iid'))
    message.yid = int(request.form.get('m_yid'))
    if not request.form.get('m_content'):
        return '评论内容不能为空'
    message.content = request.form.get('m_content')
    message.up_time = datetime.now()
    
    if session_add(message):
        flash('评论成功')
    else:
        flash('评论失败')
    return redirect('/user/main_my/')


@weibo_bp.route('/zan_add/', methods=('POST',))
@login_required
def zan_add():
    """点赞"""
    wid = request.form.get('wid')
    uid = request.form.get('uid')
    thumb = Thumb(uid=uid, wid=wid)
    if session_add(thumb):
        weibo = Weibo.query.get(wid)
        weibo.zan_num += 1
        session_update1(weibo)
    if int(request.form.get('is_main')):
        return redirect('/user/main_my/')
    else:
        return redirect('/weibo/idol/')


@weibo_bp.route('/zan_del/', methods=('POST',))
@login_required
def zan_del():
    """取消赞"""
    wid = request.form.get('wid')
    uid = request.form.get('uid')
    thumb = Thumb.query.filter(and_(Thumb.uid == uid, Thumb.wid == wid)).one()
    if session_deleter(thumb):
        weibo = Weibo.query.get(wid)
        weibo.zan_num -= 1
        session_update1(weibo)
    
    if int(request.form.get('is_main')):
        return redirect('/user/main_my/')
    else:
        return redirect('/weibo/idol/')


@weibo_bp.route('/fans_add/', methods=('POST',))
@login_required
def fans_add():
    """关注idol"""
    idol_id = request.form.get('idol_id')
    fans_id = request.form.get('fans_id')
    fans = Idol(idol_id=idol_id, fans_id=fans_id)
    if session_add(fans):
        user = User.query.get(idol_id)
        user.n_fans += 1
        session_update1(user)
    
    if int(request.form.get('is_main')):
        return redirect('/user/main_my/')
    else:
        return redirect('/weibo/idol/')


@weibo_bp.route('/fans_del/', methods=('POST',))
@login_required
def fans_del():
    """删除粉丝，取关"""
    idol_id = request.form.get('idol_id')
    fans_id = request.form.get('fans_id')
    print(idol_id, fans_id)
    fans = Idol.query.filter(and_(Idol.idol_id == idol_id, Idol.fans_id == fans_id)).one()
    if session_deleter(fans):
        user = User.query.get(idol_id)
        user.n_fans -= 1
        session_update1(user)
    
    if int(request.form.get('is_main')):
        return redirect('/user/main_my/')
    else:
        return redirect('/weibo/idol/')


@weibo_bp.route('/idol/')
@login_required
def idol():
    """关注人的微博展示"""
    try:
        user = User.query.filter_by(name=session.get('u_name')).one()
    except:
        flash('后台未检测到你的存在，请重新登录...')
        return redirect('/user/login/')
    
    page = int(request.args.get('page', 1))
    per_page = 30
    offset = per_page * (page - 1)
    # 联合User Weibo两个表
    quer = db.session().query(User, Weibo).join(Weibo, Weibo.uid == User.id)
    quer2 = quer.filter(User.id.in_(Idol.idol_list(user.id))).order_by(Weibo.up_time.desc())
    weibo_user = quer2.limit(per_page).offset(offset).all()
    max_page = ceil(quer2.count() / per_page)
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
    
    return render_template('idol.html', title='我关注的人', user=user, weibo_user=weibo_user, msgs=msgs,
                           pages=pages, page=page, start=start, end=end, max_page=max_page)


@weibo_bp.route('/fans/')
@login_required
def fans():
    """用户粉丝展示"""
    try:
        user = User.query.filter_by(name=session.get('u_name')).one()
    except:
        flash('后台未检测到你的存在，请重新登录...')
        return redirect('/user/login/')
    fans_list = Idol.fans_list(user.id)
    return render_template('fans_list.html', title='我的粉丝', user=user, fans_list=fans_list)
