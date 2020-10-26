from utils.exts import db
from models.todo import Todo
import traceback


class TodoService:
    def __init__(self):
        self.__fields__ = [
            'id', 'employee_id', 'title', 'subtitle', 'content', 'deadline',
            'starttime', 'state', 'checked'
        ]

    def find_all(self):
        return Todo.query.all()

    def find_by_id(self, id):
        return Todo.query.filter_by(id=id).first()

    def find_by_eid(self, employee_id):
        return Todo.query.filter_by(employee_id=employee_id).all()

    def find_by_checked(self, checked):
        return Todo.query.filter_by(checked=checked).all()

    def add_todo(self, employee_id, title, subtitle, content, deadline,
                 starttime, state, checked):
        print("123456")
        try:
            print("123456")
            todo = Todo(employee_id, title, subtitle, content, deadline,
                        starttime, state, checked)
            print(todo)
            print(todo.deadline)
            db.session.add(todo)
            db.session.commit()
            return True
        except Exception as e:
            print(traceback.print_exc())
            db.session.rollback()
            return False

    def delete_by_eid(self, employee_id):
        try:
            for todo in Todo.query.filter_by(employee_id=employee_id).all():
                db.session.delete(todo)
                db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    def delete_by_id(self, id):
        try:
            todo = Todo.query.filter_by(id=id).first()
            db.session.delete(todo)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    def update(self, id, title, subtitle, content, state, deadline, checked):
        try:
            todo = Todo.query.filter_by(id=id).first()
            if title is not None:
                todo.title = title
            if state is not None:
                todo.state = state
            if deadline is not None:
                todo.deadline = deadline
            if subtitle is not None:
                todo.subtitle = subtitle
            if content is not None:
                todo.content = content
            if checked is not None:
                todo.checked = checked
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            return False
