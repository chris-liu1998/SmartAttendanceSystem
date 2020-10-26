from models.attendanceSetting import AttendanceSetting
from utils.exts import db
import traceback


class AttendanceSettingService:
    def __init__(self):
        self.__fields__ = [
            'setting_id', 'start', 'end', 'elastic_time', 'date_start',
            'date_end', 'week_days'
        ]

    def find_all(self):
        return AttendanceSetting.query.all()

    def add_setting(self, start, end, elastic_time, date_start, date_end,
                    week_days):
        try:
            setting = AttendanceSetting(start, end, elastic_time, date_start,
                                        date_end, week_days)
            db.session.add(setting)
            db.session.commit()
            return {"code": 0, "data": "添加成功！"}
        except Exception as e:
            return {"code": 1, "data": f"添加失败！{traceback.print_exc()}"}

    def update_setting(self, setting_id, start, end, elastic_time, date_start,
                       date_end, week_days):
        setting_list = AttendanceSetting.query.filter_by(setting_id=setting_id)
        if setting_list.count() == 1:
            try:
                setting = setting_list.first()
                if start is not None:
                    setting.start = start
                if end is not None:
                    setting.end = end
                if elastic_time is not None:
                    setting.elastic_time = elastic_time
                if date_start is not None:
                    setting.date_start = date_start
                if date_end is not None:
                    setting.date_end = date_end
                if week_days is not None:
                    setting.week_days = week_days
                db.session.commit()
                return {"code": 0, "data": "添加成功！"}
            except Exception as e:
                db.session.rollback()
                return {"code": 1, "data": f"更新失败！{traceback.print_exc()}"}
        else:
            return {"code": 2, "data": "更新失败！记录不存在！"}

    def find_by_id(self, setting_id):
        return AttendanceSetting.query.filter_by(setting_id=setting_id).first()

    # 删除考勤设置
    def delete_setting(self, setting_id):
        setting_count = AttendanceSetting.query.filter_by(
            setting_id=setting_id).count()
        setting_list = AttendanceSetting.query.filter_by(
            setting_id=setting_id).first()
        print("--------------------")
        print(setting_list)
        if setting_count == 1:
            try:
                db.session.delete(setting_list)
                db.session.commit()
                return {'code': 200, 'data': '删除成功'}
            except Exception as e:
                db.session.rollback()
                return {'code': 201, 'data': '删除失败'}
        else:
            return {'code': 202, 'data': '账户：' + setting_id + '不存在'}
