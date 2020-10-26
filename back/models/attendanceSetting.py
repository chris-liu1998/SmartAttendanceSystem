from utils.exts import db

class AttendanceSetting(db.Model):
    """
    attendance_setting
    """
    __tablename__ = "attendance_setting"
    setting_id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Time, nullable=False)
    end = db.Column(db.Time, nullable=False)
    elastic_time = db.Column(db.Integer)
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date)
    week_days = db.Column(db.String(20))

    def __init__(self, start, end, elastic_time, date_start, date_end, week_days):
        self.start = start
        self.end = end
        self.elastic_time = elastic_time
        self.date_start = date_start
        self.date_end = date_end
        self.week_days = week_days