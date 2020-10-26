from utils.exts import db


class Employee(db.Model):
    '''employees 表'''
    __tablename__ = 'employees'
    employee_id = db.Column(db.String(255), primary_key=True)
    employee_name = db.Column(db.String(255))
    employee_title = db.Column(db.String(255))
    department_id = db.Column(db.Integer, nullable=True)
    leader_id = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    qq = db.Column(db.String(255), nullable=True)
    wechat = db.Column(db.String(255), nullable=True)

    def __init__(self, e_id, name, title, department_id, leader_id, phone, qq,
                 wechat):
        self.employee_id = e_id
        self.employee_name = name
        self.employee_title = title
        self.department_id = department_id
        self.leader_id = leader_id
        self.phone = phone
        self.qq = qq
        self.wechat = wechat