from models.account import Account
from utils.exts import db


class AccountService():
    def __init__(self):
        self.__fields__ = ['user_id', 'account', 'password', 'flag']

    # 新建帐户
    def add_one_account(self, account, pwd, flag):
        if self.find_count_by_account(account) == 0:
            try:
                account = Account(account, pwd, flag)
                db.session.add(account)
                db.session.commit()
                return {'code': 200, 'data': '添加成功'}
            except Exception as e:
                db.session.rollback()
                return {'code': 201, 'data': '添加失败'}
        else:
            return {'code': 202, 'data': '账户：' + account + '已存在'}

    # 删除账户
    def delete_account(self, account):
        if self.find_count_by_account(account) == 1:
            try:
                account = Account.query.filter_by(account=account).first()
                db.session.delete(account)
                db.session.commit()
                return {'code': 200, 'data': '删除成功'}
            except Exception as e:
                db.session.rollback()
                return {'code': 201, 'data': '删除失败'}
        else:
            return {'code': 202, 'data': '账户：' + account + '不存在'}

    # 修改密码
    def update_pwd(self, account, pwd):
        if self.find_count_by_account(account) == 1:
            try:
                account = Account.query.filter_by(account=account).first()
                account.password = pwd
                db.session.commit()
                return {'code': 200, 'data': '密码更新成功'}
            except Exception as e:
                db.session.rollback()
                return {'code': 201, 'data': '密码更新失败'}
        else:
            return {'code': 202, 'data': '账户：' + account + '不存在'}

    # 查询所有员工账户信息(过滤第一条)
    def find_all(self):
        return Account.query.order_by(Account.account).offset(1).all()

    # 查询指定权限的账户信息
    def find_by_flag(self, flag):
        return Account.query.filter_by(flag=flag).all()

    # 查询指定账户是否存在
    def find_count_by_account(self, account):
        return Account.query.filter_by(account=account).count()

    # 查询指定账户
    def find_by_account(self, account):
        return Account.query.filter_by(account=account).first()