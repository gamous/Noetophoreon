from http import server
from app import db

from datetime import datetime

class RolePlayFinder(db.Model):
    location = db.Column(db.String(12), primary_key=True, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_count = db.Column(db.Integer, default=1,nullable=True)
    server = db.Column(db.String(20),nullable=False)
    estate = db.Column(db.String(20),nullable=False)
    num1 = db.Column(db.Integer, nullable=False)
    num2 = db.Column(db.Integer, nullable=False)
    room = db.Column(db.Integer, nullable=True, default=0)
    
    recruit = db.Column(db.Boolean, nullable=True, default=False)
    #todo: many to many relationship
    name   = db.Column(db.String(20),nullable=True)
    tags = db.Column(db.String(100),nullable=True)
    content = db.Column(db.String(100))
    #todo: 1 to 1 => partyfinder
    def __repr__(self) -> str:
        return f"[{self.location}]{'[招]' if self.recruit else ''}[{self.tags}]"
