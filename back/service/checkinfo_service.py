from models.checkInfo import CheckInfo
from utils.exts import db
import traceback


class CheckInfoService:
    def __init__(self):
        self.__fields__ = ['id', 'employee_id', 'face_info']

    def find_all(self):
        """

        """
        return CheckInfo.query.all()

    def find_by_id(self, info_id):
        return CheckInfo.query.filter_by(id=info_id).first()

    def find_by_employee_id(self, employee_id):
        return CheckInfo.query.filter_by(employee_id=employee_id).first()

    def delete_by_id(self, employee_id):
        info_list = CheckInfo.query.filter_by(id=employee_id)
        if info_list.count() == 1:
            try:
                info = info_list.first()
                db.session.delete(info)
                db.session.commit()
                return {"code": 0, "data": "删除成功！"}
            except Exception as e:
                return {"code": 1, "data": f"删除失败！\n{traceback.print_exc()}"}
        else:
            return {"code": 2, "data": f"删除失败！该记录不存在！"}

    def add_info(self, employee_id, face_info):
        try:
            info = CheckInfo(employee_id, face_info)
            db.session.add(info)
            db.session.commit()
            return {"code": 0, "data": "添加成功！"}
        except Exception as e:
            return {"code": 1, "data": f"添加失败！{traceback.print_exc()}"}

    def update_info(self, employee_id, face_info):
        info_list = CheckInfo.query.filter_by(employee_id=employee_id)
        if info_list.count() == 1:
            if face_info is not None:
                info = info_list.first()
                info.face_info = face_info
                db.session.commit()
                return {"code": 0, "data": "更新成功！"}
            else:
                return {"code": 1, "data": "更新失败！无可用于更新的数据"}
        else:
            db.session.rollback()
            return {"code": 2, "data": f"更新失败！该记录不存在！"}
