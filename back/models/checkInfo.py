from utils.exts import db


class CheckInfo(db.Model):
    """
    checkinfo
    """
    __tablename__ = 'checkinfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(255), unique=True)
    face_info = db.Column(db.Integer, nullable=False)

    def __init__(self, employee_id, face_info):
        self.employee_id = employee_id
        self.face_info = face_info 