from app import db

from datetime import datetime

class ChatLog(db.Model):
    id =   db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    type = db.Column(db.String(20))
    sender = db.Column(db.String(20))
    content = db.Column(db.String(100))
    def __repr__(self) -> str:
        return f"[{self.id}][{self.time}][{self.type}][{self.sender}]{self.content}"
