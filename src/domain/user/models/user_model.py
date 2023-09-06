from datetime import datetime
from sqlalchemy import DateTime, event
from common.constant import DATABASE_TABLE_NAME
from config.db import db
from uuid import uuid4

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = DATABASE_TABLE_NAME['user']
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Set up an event listener to automatically update the 'updated_at' field
@event.listens_for(User, 'before_update')
def set_updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()


