from utils.exts import db


class Account(db.Model):
    '''accounts 表'''
    __tablename__ = 'accounts'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    flag = db.Column(db.Integer)

    def __init__(self, account, pwd, flag):
        self.account = account
        self.password = pwd
        self.flag = flag