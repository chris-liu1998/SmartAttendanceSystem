from utils.exts import db


class IndividualRecord(db.Model):
    """
    ivd
    """
    __tablename__ = "ivd_record"
    employee_id = db.Column(db.String(255), primary_key=True)
    record_id = db.Column(db.Integer)  # 最近一次未完成的打卡

    def __init__(self, employee_id, record_id):
        self.employee_id = employee_id
        self.record_id = record_id