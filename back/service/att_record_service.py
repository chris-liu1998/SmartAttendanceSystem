from models.attendanceRecord import AttendanceRecord
from utils.exts import db
from sqlalchemy import extract, and_
import traceback


class AttendanceRecordService:
    def __init__(self):
        self.__fields__ = [
            'record_id', 'employee_id', 'setting_id', 'start_time', 'end_time',
            'status'
        ]

    def find_all(self):
        return AttendanceRecord.query.all()

    def add_record(self, employee_id, setting_id, start_time, end_time,
                   status):
        try:
            record = AttendanceRecord(employee_id, setting_id, start_time,
                                      end_time, status)
            db.session.add(record)
            db.session.commit()
            return record.record_id
        except Exception as e:
            db.rollback()
            return {"code": 1, "data": f"添加失败！{traceback.print_exc()}"}

    def update_record(self, record_id, setting_id, end_time, status):
        record_list = AttendanceRecord.query.filter_by(record_id=record_id)
        if record_list.count() == 1:
            try:
                record = record_list.first()
                if setting_id is not None:
                    record.setting_id = setting_id
                if end_time is not None:
                    record.end_time = end_time
                if status is not None:
                    record.is_leave = status
                db.session.commit()
                return {"code": 0, "data": "更新成功！"}
            except Exception as e:
                db.session.rollback()
                return {"code": 1, "data": f"更新失败！{traceback.print_exc()}"}
        else:
            return {"code": 2, "data": "更新失败！记录不存在！"}

    def delete_record(self, record_id):
        record_list = AttendanceRecord.query.filter_by(record_id=record_id)
        if record_list.count() == 1:
            try:
                record = record_list.first()
                db.session.delete(record)
                db.session.commit()
                return {"code": 0, "data": "删除成功！"}
            except Exception as e:
                return {"code": 1, "data": f"删除失败！\n{traceback.print_exc()}"}
        else:
            return {"code": 2, "data": f"删除失败！该记录不存在！"}

    def find_by_record_id(self, record_id):
        return AttendanceRecord.query.filter_by(record_id=record_id).first()

    def find_by_employee(self, employee_id):
        return AttendanceRecord.query.filter_by(employee_id=employee_id).all()

    def find_by_setting(self, setting_id):
        return AttendanceRecord.query.filter_by(setting_id=setting_id).all()

    def find_by_leave(self, status):
        return AttendanceRecord.query.filter_by(status=status).all()

    def find_by_range(self, start_date, end_date, employee_id=None):
        if employee_id is not None:
            return AttendanceRecord.query.filter(
                and_(AttendanceRecord.start_time.between(start_date,
                                                         end_date)),
                AttendanceRecord.employee_id == employee_id).all()
        else:
            return AttendanceRecord.query.filter(
                AttendanceRecord.start_time.between(start_date,
                                                    end_date)).all()

    def identify_status(self, status):
        status_list = status.split("/")
        list = []
        if '1' not in status_list:
            list.append('finished')

        else:
            if status_list[0] == '1':
                list.append('absent')
            if status_list[1] == '1':
                list.append('early_out')
            if status_list[2] == '1':
                list.append('late_in')
            if status_list[3] == '1':
                list.append('leave')
        return list

    def count_status(self, employee_id, end_date, start_date=None):
        items = self.find_by_employee(employee_id)
        if start_date is not None:
            items = self.find_by_range(start_date, end_date, employee_id)

        stats = {
            'total': 0,
            'finished': 0,
            'absent': 0,
            'early_out': 0,
            'late_in': 0,
            'leave': 0
        }
        if len(items) != 0:
            for item in items:
                list = self.identify_status(item.status)
                stats['total'] += 1
                if 'finished' in list:
                    stats['finished'] += 1
                if 'absent' in list:
                    stats['absent'] += 1
                if 'early_out' in list:
                    stats['early_out'] += 1
                if 'late_in' in list:
                    stats['late_in'] += 1
                if 'leave' in list:
                    stats['leave'] += 1

        return stats
