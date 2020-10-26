from models.department import Department
from utils.exts import db


# 数据操作
class DepartmentService:
    def __init__(self):
        self.__fields__ = [
            'department_id', 'department_name', "attendance_setting"
        ]

    # 新建部门
    def add_one_department(self, name):
        if Department.query.filter_by(department_name=name).count() == 0:
            try:
                department = Department(name)
                db.session.add(department)
                db.session.commit()
                return {'code': 200, 'data': '添加成功'}
            except Exception as e:
                db.session.rollback()
                return {'code': 201, 'data': '添加失败'}
        else:
            return {'code': 202, 'data': '部门：' + name + '已存在'}

    # 查询所有部门信息
    def find_all(self):
        return Department.query.order_by(Department.department_id).all()

    # 查询指定部门信息
    def find_by_name(self, name):
        return Department.query.filter_by(department_name=name).all()

    # 查询指定部门是否存在
    def find_count_by_name(self, name):
        return Department.query.filter_by(department_name=name).count()

    # 查询部门编号
    def find_id_by_name(self, name):
        department = Department.query.filter_by(department_name=name).first()
        return department.department_id

    # 查询员工的部门名称
    def find_name_by_id(self, id):
        department = Department.query.filter_by(department_id=id)
        if department.count() == 1:
            return department.first().department_name
        else:
            return "部门编号为" + id + "的部门不存在"

    def update_setting(self, attendance_setting):
        is_successful = True

        try:
            for i in Department.query.all():
                i.attendance_setting = attendance_setting
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            is_successful = False

        return is_successful

    def find_setting_by_did(self, did):
        return Department.query.filter_by(
            department_id=did).first().attendance_setting
