from libs.orm import db


def session_add(user):
    """
    添加一条数据
    :param user:一个实例对象
    :return:Boolean
    """
    db.session.add(user)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
        return False


def session_add_all(users):
    """
    添加多条数据
    :param users:list
    :return:Boolean
    """
    db.session.add_all(users)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def session_deleter(user):
    """
    删除一条数据
    :param user:
    :return: Boolean
    """
    db.session.delete(user)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
