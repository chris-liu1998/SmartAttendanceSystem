from utils.exts import db


class Department(db.Model):
    '''departments 表'''
    __tablename__ = 'departments'
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(255), unique=True)
    attendance_setting = db.Column(db.Integer)

    # attendance_setting = db.Column(db.String(255))

    def __init__(self, name):
        # self.department_id = d_id
        self.department_name = name
        # self.department_setting = setting

    # 重写
    # def __repr__(self):
    #   pass