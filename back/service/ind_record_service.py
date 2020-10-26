from utils.exts import db
from models.individualRecord import IndividualRecord
import traceback

class IndividualRecordService:
    def __init__(self):
        self.__fields__ = ['employee_id', 'record_id']

    def find_all(self):
        return IndividualRecord.find_all()

    def find_by_employee_id(self, employee_id):
        return IndividualRecord.query.filter_by(employee_id=employee_id).first()

    def add_record(self, employee_id, record_id):
        find = IndividualRecord.query.filter_by(employee_id=employee_id).count()
        if find == 0:
            try:
                record = IndividualRecord(employee_id, record_id)
                db.session.add(record)
                db.session.commit()
                return {"code": 0, "data": "添加成功！"}
            except Exception as e:
                db.session.rollback()
                return {"code": 1, "data": f"添加失败！{traceback.print_exc()}"}
        else:
            return {"code": 2, "data": "记录已存在！"}

    def update(self, employee_id, record_id):
        find = IndividualRecord.query.filter_by(employee_id=employee_id)
        if find.count() == 0:
            return {"code": 2, "data": "记录不存在！"}
        else:
            try:

                record = find.first()
                record.record_id = record_id
                db.session.commit()
                return {"code": 0, "data": "更新成功！"}
            except Exception as e:
                db.session.rollback()
                return {"code": 1, "data": f"更新失败！{traceback.print_exc()}"}

    def delete(self, employee_id):
        find = IndividualRecord.query.filter_by(employee_id=employee_id)
        if find.count() == 0:
            return {"code": 2, "data": "记录不存在！"}
        else:
            try:

                record = find.first()
                db.session.delete(record)
                db.session.commit()
                return {"code": 0, "data": "删除成功！"}
            except Exception as e:
                db.session.rollback()
                return {"code": 1, "data": f"删除失败！{traceback.print_exc()}"}