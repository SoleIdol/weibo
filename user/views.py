# author:Sole_idol
# filename: views.py
# datetime:2020/8/22 9:38
from flask import Blueprint, render_template, redirect, request, flash, session
from math import ceil

from user.models import User
from weibo_t.models import Weibo, Message, Idol
from libs.orm import db
from libs.tools import login_required, save_file, del_head, make_password, check_password
from libs.sqltools import session_add, session_update1

user_bp = Blueprint('user', __name__, url_prefix='/user/')
user_bp.template_folder = './templates'
user_bp.static_folder = '../static'


@user_bp.route('/login/', methods=('POST', 'GET'))
def login():
    """登录页面"""
    if request.method == 'POST':
        name = request.form.get('u_name')
        try:
            password = request.form.get('password')
            safe_password = User.query.filter_by(name=name).one().password
            if check_password(password, safe_password):
                session['u_name'] = name
                return redirect('/user/main_my/')
            else:
                flash('密码错误！')
                return redirect('/user/login/')
        except:
            flash('用户名不存在！')
            return redirect('/user/login/')
    else:
        return render_template('login.html', title='登录')


@user_bp.route('/register/', methods=('POST', 'GET'))
def register():
    """注册页面"""
    if request.method == 'POST':
        user = User()
        user.name = request.form.get('u_name')
        if not user.name:
            flash('用户名不能为空')
            return redirect('/user/register/')
        elif not 3 <= len(user.name) <= 12:
            flash('用户名长度应在3~12位之间')
            return redirect('/user/register/')
        
        password = request.form.get('password')
        if not password:
            flash('密码不能为空')
            return redirect('/user/register/')
        elif not 6 <= len(password) <= 18:
            flash('密码长度应在6~18位之间')
            return redirect('/user/register/')
        
        if request.form.get('password') == request.form.get('re_password'):
            user.password = make_password(password)
            db.session.add(user)
            try:
                db.session.commit()
                flash('注册成功！！！')
            except:
                db.session.rollback()
                flash('用户名已存在!')
                return redirect('/user/register/')
            else:
                return redirect('/user/login/')
        else:
            flash('两次输入密码不一致')
            return redirect('/user/register/')
    else:
        return render_template('register.html', title='注册')


@user_bp.route('/main_my/')
@login_required
def main_my():
    """首页所有微博展示"""
    try:
        user = User.query.filter_by(name=session.get('u_name')).one()
    except:
        flash('后台未检测到你的存在，请重新登录...')
        return redirect('/user/login/')
    
    page = int(request.args.get('page', 1))
    per_page = 30
    offset = per_page * (page - 1)
    # 联合User Weibo两个表
    weibo_user = db.session().query(User, Weibo).join(Weibo, Weibo.uid == User.id).filter().order_by(
        Weibo.up_time.desc()).limit(per_page).offset(offset).all()
    
    max_page = ceil(Weibo.query.count() / per_page)
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
    
    return render_template('main_my.html', title='迷你微博', user=user, weibo_user=weibo_user, msgs=msgs,
                           pages=pages, page=page, start=start, end=end, max_page=max_page)


@user_bp.route('/info/', methods=('POST', 'GET'))
@login_required
def user_info():
    """用户信息"""
    try:
        user = User.query.filter_by(name=session.get('u_name')).one()
    except:
        flash('后台未检测到你的存在，请重新登录...')
        return redirect('/user/login/')
    if request.method == 'POST':
        
        user.name = request.form.get('name')
        if not user.name:
            flash('用户名不能为空')
        elif not 3 <= len(user.name) <= 12:
            flash('用户名长度应在3~12位之间')
        else:
            file = request.files.get('head')
            if file:
                # # 删除原本头像 这里因为图片一样时，保存同一个，所以不能删除
                # del_head(user.head)
                #
                # 保存头像
                filename = save_file(file)
                user.head = filename
            user.gender = request.form.get('gender')
            user.city = request.form.get('city')
            user.birthday = request.form.get('birthday')
            if session_update1(user):
                flash('信息修改成功')
                session['u_name'] = user.name
            else:
                flash('信息修改失败')
        return render_template('user_info.html', title='用户信息', user=user)
    else:
        return render_template('user_info.html', title='用户信息', user=user)


@user_bp.route('/logout/')
def logout():
    """退出登录"""
    session.clear()
    return redirect('/user/login/')


@user_bp.route('/fans_info/')
@login_required
def fans_info():
    """不可编辑用户信息展示"""
    fans_id = request.args.get('fans_id')
    user = User.query.get(fans_id)
    if not user:
        flash('抱歉，此用户已不存在')
        return redirect(request.path)
    n_idol = Idol.query.filter_by(fans_id=fans_id).count()
    return render_template('fans_info.html', title='用户信息', user=user, n_idol=n_idol)
