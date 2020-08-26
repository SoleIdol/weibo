import os
from hashlib import md5, sha256
from flask import session, flash, redirect
from functools import wraps


def make_password(password):
    """
    产生一个安全的密码
    :return: 加密后的password
    """
    if not isinstance(password, bytes):
        password = str(password).encode('utf8')
    
    # 计算哈希值
    hash_value = sha256(password).hexdigest()
    
    # 产生一个随机盐
    salt = os.urandom(16).hex()
    
    # 加盐，产生安全密码
    safe_password = salt + hash_value
    
    return safe_password


def check_password(password, safe_password):
    """
    密码验证
    :param password:页面输入的密码
    :param safe_password:数据库中的密码
    :return: Boolean
    """
    if not isinstance(password, bytes):
        password = str(password).encode('utf8')
    
    # 计算哈希值
    hash_value = sha256(password).hexdigest()
    
    return hash_value == safe_password[32:]


def save_file(file):
    """
    头像上传处理
    :return:文件名filename
    """
    # 获取文件后缀名
    pre = file.filename.rsplit('.', 1)[-1]
    
    # 读取文件二进制数据
    file_bin_data = file.stream.read()
    
    # 文件指针归零
    file.stream.seek(0)
    
    # 计算文件md5值
    filename = md5(file_bin_data).hexdigest() + '.' + pre
    
    # 获取项目文件的绝对路径
    bash_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 拼接文件绝对路径
    filepath = os.path.join(bash_dir, 'static', 'upload', 'img', filename)
    
    # 保存文件
    file.save(filepath)
    
    return filename


def del_head(filename):
    # 获取项目文件的绝对路径
    bash_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if filename == 'default.jpg':
        return '默认头像不删除'
    
    # 拼接文件绝对路径
    filepath = os.path.join(bash_dir, 'static', 'upload', 'img', filename)
    
    # 删除头像文件
    try:
        os.remove(filepath)
    except FileNotFoundError:
        return '要删除的文件不存在'


# 判断是否登录的装饰器
def login_required(fn):
    # 为了防止Python的链式调用，添加了@wraps()装饰器
    @wraps(fn)
    def check_session(*args, **kwargs):
        if session.get('u_name', ''):
            return fn(*args, **kwargs)
        else:
            flash('你还没有登录，请登录...')
            return redirect('/user/login/')
    
    return check_session
