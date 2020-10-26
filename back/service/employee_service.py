from models.employee import Employee
from sqlalchemy import and_
from utils.exts import db
from utils.class2data import Class2Data
from utils.pinyin import pinyin
import json
from service.department_service import DepartmentService
from service.account_service import AccountService

# Service
department = DepartmentService()
account = AccountService()


class EmployeeService:
    def __init__(self):
        self.__fields__ = [
            'employee_id', 'employee_name', 'employee_title', 'department_id',
            'leader_id', 'phone', 'qq', 'wechat'
        ]

    # 新增员工(同时分发账户)
    def add_one_employee(self, e_id, name, title, department_name, leader_id,
                         phone, qq, wechat):
        if self.find_count_by_e_id(e_id) == 0:
            try:
                if department.find_count_by_name(department_name) == 0:
                    # 判断该部门是否存在——>不存在
                    # 在数据库中新增该部门
                    department.add_one_department(department_name)
                elif department.find_count_by_name(department_name) == 1:
                    # 判断该部门是否存在——>存在
                    pass
                else:
                    # error
                    return {'code': 201, 'data': '添加失败'}
                d_id = department.find_id_by_name(department_name)
                employee = Employee(e_id, name, title, d_id, leader_id, phone,
                                    qq, wechat)
                db.session.add(employee)
                db.session.commit()
                if title == '部长':
                    flag = 1
                else:
                    flag = 2
                newpassword = e_id + pinyin(name)
                account.add_one_account(e_id, newpassword, flag)
                accountdata = account.find_by_account(e_id)
                changedata = Class2Data(accountdata, account.__fields__, 1)
                return {'code': 200, 'data': changedata}
            except Exception as e:
                db.session.rollback()
                return {'code': 201, 'data': '添加失败'}
        else:
            return {'code': 202, 'data': '员工：' + e_id + '已存在'}

    # 删除员工(同时删除账户)
    def delete_employee(self, e_id):
        if self.find_count_by_e_id(e_id) == 1:
            try:
                employee = self.find_by_e_id(e_id)
                db.session.delete(employee)
                db.session.commit()
                deleteresult = account.delete_account(e_id)
                if deleteresult['code'] == 200:
                    return {'code': 200, 'data': '删除成功'}
                else:
                    return {'code': 201, 'data': '删除失败'}
            except Exception as e:
                db.session.rollback()
                return {'code': 201, 'data': '删除失败'}
        else:
            return {'code': 202, 'data': '员工' + e_id + '不存在'}

    # 更新员工基本信息
    def update_employee(self, e_id, name, title, department_name, leader_id,
                        phone, qq, wechat):
        if self.find_count_by_e_id(e_id) == 1:
            try:
                if department.find_count_by_name(department_name) == 0:
                    # 判断该部门是否存在——>不存在
                    # 在数据库中新增该部门
                    department.add_one_department(department_name)
                elif department.find_count_by_name(department_name) == 1:
                    # 判断该部门是否存在——>存在
                    pass
                else:
                    # error
                    return {'code': 201, 'data': '更新失败'}
                d_id = department.find_id_by_name(department_name)
                employee = self.find_by_e_id(e_id)
                employee.employee_id = e_id
                employee.employee_name = name
                employee.employee_title = title
                employee.department_id = d_id
                employee.leader_id = leader_id
                employee.phone = phone
                employee.qq = qq
                employee.wechat = wechat
                db.session.commit()
                return {'code': 200, 'data': '更新成功'}
            except Exception as e:
                db.session.rollback()
                return {'code': 201, 'data': '更新失败'}
        else:
            return {'code': 202, 'data': '员工' + e_id + '不存在'}

    # 用户登录
    # 200 登陆成功 返回该用户基本信息
    # 201 验证码错误
    # 202 密码错误
    # 203 账户不存在
    def user_login(self, loginaccount, pwd):
        if account.find_count_by_account(loginaccount) == 1:
            flag = account.find_by_account(loginaccount).flag
            if account.find_by_account(loginaccount).password == pwd:
                userid = account.find_by_account(loginaccount).account
                if loginaccount == "Admin":
                    data = {'userid': userid, 'flag': flag}
                    return {'code': 200, 'data': data}
                else:
                    departmentid = self.find_did_by_eid(userid)
                    data = {
                        'userid': userid,
                        'flag': flag,
                        'departmentid': departmentid
                    }
                    return {'code': 200, 'data': data}

            else:
                return {'code': 202, 'data': '密码错误'}
        else:
            return {'code': 203, 'data': '账户：' + loginaccount + '不存在'}

    # 查询所有员工信息
    def find_all(self):
        return Employee.query.order_by(Employee.employee_id).all()

    # 通过 employee_id 查询该员工是否存在
    def find_count_by_e_id(self, e_id):
        return Employee.query.filter_by(employee_id=e_id).count()

    # 通过 employee_id 查询该员工(修改部门编号为名称)
    def find_by_e_id(self, e_id):
        oneemployee = Employee.query.filter_by(employee_id=e_id).first()
        oneemployee.department_id = department.find_name_by_id(
            oneemployee.department_id)
        return oneemployee

    # 查询指定部门人数
    def find_count_by_d_id(self, d_id):
        return Employee.query.filter_by(department_id=d_id).count()

    # 查询指定部门的部长信息
    def find_minister_by_d_id(self, d_id):
        return Employee.query.filter(
            and_(Employee.department_id == d_id,
                 Employee.employee_title == '部长')).first()

    # 查询各部门人数
    def find_counts_in_department(self):
        list = []
        department_all = department.find_all()
        for item in department_all:
            temp = {}
            tempminister = {}
            d_id = getattr(item, 'department_id')
            minister = self.find_minister_by_d_id(d_id)
            if minister != None:
                tempminister['minister_name'] = getattr(
                    minister, 'employee_name')
                tempminister['minister_id'] = getattr(minister, 'employee_id')
            else:
                tempminister = None
            temp['department_name'] = getattr(item, 'department_name')
            temp['department_employees'] = self.find_count_by_d_id(d_id)
            temp['department_minister'] = tempminister
            list.append(temp)
        return {'code': 200, 'data': list}

    # 通过部长查询员工信息
    def find_employee_by_leader_id(self, leader_id):
        employee = Employee.query.filter_by(leader_id=leader_id).all()
        e_ids = []
        for item in employee:
            e_id = getattr(item, 'employee_id')
            e_ids.append(e_id)
        return e_ids

    # 通过员工id查询departmentid
    def find_did_by_eid(self, eid):
        employee = Employee.query.filter_by(employee_id=eid).first()
        did = getattr(employee, 'department_id')
        return did

    # 通过 employee_id 查询该员工
    def find_by_eid(self, e_id):
        return Employee.query.filter_by(employee_id=e_id).first()

