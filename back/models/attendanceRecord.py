from utils.exts import db


class AttendanceRecord(db.Model):
    """
    attendance_record
    """
    __tablename__ = "attendance_record"
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(255), unique=True)
    setting_id = db.Column(db.Integer, unique=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(7), nullable=False)

    def __init__(self, employee_id, setting_id, start_time, end_time, status):
        self.employee_id = employee_id
        self.setting_id = setting_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status