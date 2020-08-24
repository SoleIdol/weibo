# author:Sole_idol
# filename: views.py
# datetime:2020/8/22 9:38
from flask import Blueprint, render_template, redirect, request, flash, session
from user.models import User
from libs.orm import db

user_bp = Blueprint('user', __name__, url_prefix='/user/')
user_bp.template_folder = './templates'


@user_bp.route('/login/', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        name = request.form.get('u_name')
        try:
            if request.form.get('password') == User.query.filter_by(name=name).one().password:
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
    if request.method == 'POST':
        user = User()
        user.name = request.form.get('u_name')
        if not user.name:
            flash('用户名不能为空')
            return redirect('/user/register/')
        if request.form.get('password') == request.form.get('re_password'):
            user.password = request.form.get('password')
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
def main_my():
    return render_template('main_my.html', title='用户博客界面', u_name=session.get('u_name'))


@user_bp.route('/logout/')
def logout():
    session.pop('u_name')
    return redirect('/login/')
