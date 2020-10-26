from utils.exts import db


class Todo(db.Model):
    '''Todo 表'''
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255))
    content = db.Column(db.String(255))
    deadline = db.Column(db.DateTime, nullable=False)
    starttime = db.Column(db.DateTime, nullable=False)
    state = db.Column(db.Boolean, nullable=False)
    checked = db.Column(db.Boolean, nullable=False)

    def __init__(self, employee_id, title, subtitle, content, deadline,
                 starttime, state, checked):
        self.employee_id = employee_id
        self.title = title
        self.subtitle = subtitle
        self.content = content
        self.deadline = deadline
        self.starttime = starttime
        self.state = state
        self.checked = checked