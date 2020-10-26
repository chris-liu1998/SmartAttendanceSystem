from utils.exts import db


class Leave(db.Model):
    __tablename__ = 'leave'
    leave_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)
    pushtime = db.Column(db.DateTime)
    handletime = db.Column(db.DateTime)
    employee_id = db.Column(db.String(255))
    reason = db.Column(db.String(255))
    handlemode = db.Column(db.String(255))
    processmode = db.Column(db.String(255))
    file = db.Column(db.String(255))
    issubmit = db.Column(db.String(1))

    def __init__(self,
                 starttime,
                 endtime,
                 pushtime,
                 employee_id,
                 reason,
                 handlemode,
                 processmode,
                 file,
                 issubmit=0):
        self.starttime = starttime
        self.endtime = endtime
        self.pushtime = pushtime

        self.employee_id = employee_id
        self.reason = reason
        self.handlemode = handlemode
        self.processmode = processmode
        self.file = file
        self.issubmit = issubmit

    def setHandletime(self, handletime):
        self.handletime = handletime